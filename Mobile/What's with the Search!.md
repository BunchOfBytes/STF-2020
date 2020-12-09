# Challenge: What's with the Search! (Mobile-3)
There is an admin dashboard in the Korovax mobile. There aren't many functions, but we definitely can search for something!

## Summary:
This application contains client-side checks for a flag which a user is required to access secret functionality. Players can easily bypass this authentication checks via analysing the APK for a password

Relevant CWE:

CWE-603: Use of Client-Side Authentication (https://cwe.mitre.org/data/definitions/603.html)

## Tools used:
OS - Kali Linux

jadx-gui - Decompile APK to Java programming language (mobile-challenge-4)

genymotion - Android emulator

apktool - disassemble our apk

adb - install apk on our android app.

BurpSuite - to test for any web requests

Ghidra - to decompile the native library

## Setup:
Install genymotion (https://docs.genymotion.com/desktop/3.0/01_Get_started/012_Installation.html). Be sure to install an SDK of 21 or higher as the minSdkVersion specified in AndroidManifest.xml is 21.
See here if you want to figure out how to configure BurpSuite with genymotion (Ignore part on Frida) - https://arben.sh/bugbounty/Configuring-Frida-with-Burp-and-GenyMotion-to-bypass-SSL-Pinning/

## Process:
### Step 1: Analysing authentication functionality
#### Dynamic Analysis:
To install the APK app use the following (Take note of the path executed from!):
``````
root@kali:/opt/genymobile/genymotion/tools# ./adb install /root/mobile-challenge.apk
``````
I performed dynamic analysis on the app first. Testing the admin search functionality, I noticed that there are no requests being made on BurpSuite. This is a big red flag for us that the code is performing checks on the client side! Additionally, a popup with the string "Flag is wrong!" appears, we can use this to confirm which block of code is executing when we perform the search functionality later!

#### Static Analysis:
We decompile the app on jadx-gui
``````
jadx-gui
``````
Select the downloaded apk.

Since we are after the admin search functionality, we visit the sg.gov.tech.ctf.mobile/Admin/AdminHome from the activity code, we see a few functions. However, the onClick() function seems to be the most interesting because it containg the "Flag is wrong!" string we identified earlier!

``````
public void onClick(View v) {
            AdminHome adminHome = AdminHome.this;
            adminHome.f2932e = (EditText) adminHome.findViewById(R.id.editText_enteredFlag);
            if (AdminHome.this.b(AdminHome.this.c(AdminHome.this.f2932e.getText().toString())).equalsIgnoreCase(AdminHome.this.f2929b)) {
                a.b.k.c.a builder = new a.b.k.c.a(AdminHome.this);
                View view = LayoutInflater.from(AdminHome.this).inflate(R.layout.custom_alert, null);
                TextView details = (TextView) view.findViewById(R.id.alert_detail);
                ((TextView) view.findViewById(R.id.title)).setText("Congrats!");
                details.setText("Add govtech-csg{} to what you found!");
                builder.h("Proceed", new a());
                builder.f("Close", new b());
                builder.k(view);
                builder.l();
                Toast.makeText(AdminHome.this.getApplicationContext(), "Flag is correct!", 0).show();
                return;
            }
            Toast.makeText(AdminHome.this.getApplicationContext(), "Flag is wrong!", 0).show();
        }
``````
The if() statement is checking if something AdminHome.this.b(AdminHome.this.c(AdminHome.this.f2932e.getText().toString())) is equal to AdminHome.this.f2929b. Viewing this variable in the Java code

Analysing AdminHome.this.c,
``````
    public final String c(String enteredFlagString) {
        String str = "govtech-csg{";
        if (!enteredFlagString.contains(str)) {
            return enteredFlagString;
        }
        String result = enteredFlagString.replace(str, BuildConfig.FLAVOR);
        return result.substring(0, result.length() - 1);
    }
``````
We see that if our entered string does not govtech-csg{, the entered string is returned, and if it does contain it, the beginning portion and the last character of the string will be removed before passing it into the next function. So for instance govtech-csg{qqww1122} will be passed as qqww1122 

Analysing AdminHome.this.b,
``````
    public String b(String toHash) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-1");
            byte[] bytes = toHash.getBytes(SQLiteDatabase.KEY_ENCODING);
            digest.update(bytes, 0, bytes.length);
            return bytesToHex(digest.digest());
        } catch (NoSuchAlgorithmException e2) {
            System.out.println("Algorithm not recognised");
            return null;
        } catch (UnsupportedEncodingException e3) {
            System.out.println("Something is wrong. Like really.");
            return null;
        }
    }

``````
The the entered string is then being hashed in SHA1 format.

Now we analyse AdminHome.this.f2929b.
``````
public String f2929b = getPasswordHash();
``````

So we analyse getPasswordHash(),
``````
    public native String getPasswordHash();

    static {
        System.loadLibrary("native-lib");
    }
``````
getPasswordHash() is a function in a native library. A native library is a library where functions can be written in C or C++ instead of normal Android programming languages such as Java/Kotlin.

To analyse this we can disassemble the APK using this apktool
``````
apktool d -f -r mobile-challenge.apk
``````

We can use Ghidra to analyse the function, since we there is a native library in x86 instructions, we can easily import into Ghidra. The file can be found in
./mobile-challenge/lib/x86/libnative-lib.so

When we analyse Ghidra we can search functions in the Symbol Tree. Go under Java_sg_gov_tech_ctf_mobile > Java_sg_gov_tech_ctf_mobile_Admin_AdminHome_getPasswordHash

void Java_sg_gov_tech_ctf_mobile_Admin_AdminHome_getPasswordHash(int *param_1)
``````
{
  int in_GS_OFFSET;
  undefined local_41 [41];
  int local_18;
  
  local_18 = *(int *)(in_GS_OFFSET + 0x14);
  FUN_00019c00(local_41,0x29,&DAT_00042029,"b7c1020edc5d4ab5ce059909f0a7bd73b3de005b");
  (**(code **)(*param_1 + 0x29c))(param_1,local_41);
  if (*(int *)(in_GS_OFFSET + 0x14) == local_18) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
``````
Oh look! There is a hash stored in there. We can search this hash online!
We will get the URL https://sha1.gromweb.com/?hash=b7c1020edc5d4ab5ce059909f0a7bd73b3de005b,
Click the link and we it says that this hash decrypts to qqww1122.

When we key in qqww1122 into the search function into our android emulator, we get a popup saying that we should add govtech-csg{} to the password! 

### Flag: govtech-csg{qqww1122}

## Mitigations
Sensitive passwords/flags should not be stored on the client

### Writeup by: Haxatron
