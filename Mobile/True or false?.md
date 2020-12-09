# Challenge: True or false? (Mobile-4)
True or false, we can log in as admin easily.

## Summary:
This application contains client-side checks in order for a user to access admin functionality. Players can easily bypass this authentication checks via modifying the Smali code contained in the APK file.

Relevant CWE:

CWE-603: Use of Client-Side Authentication (https://cwe.mitre.org/data/definitions/603.html)

## Tools used:
OS - Kali Linux

jadx-gui - Decompile APK to Java programming language (mobile-challenge-4)

apktool - Disassemble APK to Smali files and build APK from Smali files

jarsigner - sign our modified Android app

genymotion - Android emulator

adb - install apk on our android app.

BurpSuite - to test for any web requests

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
I performed dynamic analysis on the app first. Testing the admin authentication functionality, I noticed that there are no requests being made on BurpSuite. This is a big red flag for us that the code is performing checks on the client side!

#### Static Analysis:
We decompile the app on jadx-gui
``````
jadx-gui
``````
Select the downloaded apk.

Since we are after the admin authentication functionality, we visit the AdminAuthenticationActivity from the activity code, we see a function and 2 classes, OnCreate(), class a and class b. Since OnCreate() looks like it is creating the UI of the app and class a has little code being performed we zoom into class b. 
``````
        public Fragment getItem(int position) {
            if (position == 0) {
                return new f.a.a.a.a.a.a();
            }
            if (position != 1) {
                return null;
            }
            return new f.a.a.a.a.e.c();
        }
``````
This means that the authentication code can be performed in either f.a.a.a.a.a.a() or f.a.a.a.a.e.c().

Examining f.a.a.a.a.a.a(),
``````
 public void onClick(View v) {
            if (a.this.f2851c.getText().toString().contains(c.a.a.a.a(-891818782648L))) {
                a.b.k.c.a builder = new a.b.k.c.a(this.f2855b.getContext());
                View view = LayoutInflater.from(this.f2855b.getContext()).inflate(R.layout.custom_alert, null);
                TextView details = (TextView) view.findViewById(R.id.alert_detail);
                ((TextView) view.findViewById(R.id.title)).setText(c.a.a.a.a(-1033552703416L));
                details.setText(c.a.a.a.a(-1076502376376L));
                builder.h(c.a.a.a.a(-1252596035512L), new C0061a());
                builder.f(c.a.a.a.a(-1286955773880L), new C0062b());
                builder.k(view);
                builder.l();
                return;
            }
            try {
                new Thread(new c(new Handler())).start();
            } catch (Exception e2) {
                Toast.makeText(this.f2855b.getContext(), c.a.a.a.a(-1312725577656L), 0).show();
            }
        }
``````
As seen above there is a if statement which is checking if a string containing something, presumably, this is the admin authentication check.

To access this file we need to find the full path to the function and class, we already know the full path as f/a/a/a/a/a/a, the class can be identified from the class which the authentication function is nested in, which is class b.

### Step 2: Modifying authentication functionality
We can disassemble the APK using this apktool
``````
apktool d -f -r mobile-challenge.apk
``````
Go ahead and modify the target file using nano or your preferred file editor
``````
nano ./mobile-challenge/smali/f/a/a/a/a/a/'a$b.smali'
``````

The code block we need to modify can be found for search for 'if' in the Smali code
``````
.line 75
    .local v0, "password":Ljava/lang/String;
    const-wide v1, -0xcfa48aafb8L

    invoke-static {v1, v2}, Lc/a/a/a;->a(J)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z

    move-result v1

    if-eqz v1, :cond_0
``````

The code we want to modify is if-eqz v1, :cond_0 and we want to make it such that the authentication passes if the checked string does not contain the string. So we can simply modify the line contained the if code to:
``````
if-nez v1, :cond_0
``````
### Step 3: Bypassing authentication,
Now we utilise apktool to rebuild the modified APK.
``````
apktool b mobile-challenge -o modifiedAPK.apk
``````
Now we need to sign our APK
``````
keytool -genkey -v -keystore my-release-key.keystore -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore my-release-key.keystore modifiedAPK.apk mykey
``````
And reinstall the modified APK.
``````
root@kali:/opt/genymobile/genymotion/tools# ./adb uninstall sg.gov.tech.ctf.mobile
root@kali:/opt/genymobile/genymotion/tools# ./adb install /root/modifiedAPK.apk
``````
And now when we visit the admin login page even without a password, we can login!

### Flag: govtech-csg{It5_N0T_Ez_2_L0G_1n_S_AdM1n}

## Mitigations
Authentication should be performed on server-side. 

### Writeup by: Haxatron
