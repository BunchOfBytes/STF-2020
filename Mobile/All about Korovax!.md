# Challenge: All about Korovax! (Mobile-6)
As a user and member of Korovax mobile, you will be treated with a lot of information about COViD and a few in-app functions that should help you understand more about COViD and Korovax! Members should be glad that they even have a notepad in there, to create notes as they learn more about Korovax's mission!

## Summary:
This application contains hidden functionality in ViewActivity which can be accessed via a deep link. The hidden functionality has a client-side string validation which can be 
easily bypassed via modification of Smali code.

Relevant CWE:

CWE-603: Use of Client-Side Authentication (https://cwe.mitre.org/data/definitions/603.html)

CWE-912: Hidden Functionality (https://cwe.mitre.org/data/definitions/912.html)

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
I performed dynamic analysis on the app first. Testing the text editor activity, there are no web requests. That means that the text editor is not communicating with any server which is normal behaviour. Continuing on I did some static analysis,

#### Static Analysis:
We decompile the app on jadx-gui
``````
jadx-gui
``````
Select the downloaded apk.

Static analysis revealed that there is an activity called ViewActivity which is under the sg.gov.tech.ctf.mobile.User. Checking the AndroidManifest.xml,
``````
        <activity android:name="sg.gov.tech.ctf.mobile.User.ViewActivity" android:exported="true" android:configChanges="keyboardHidden|orientation|screenSize">
            <intent-filter android:label="flag_view">
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.BROWSABLE"/>
                <data android:scheme="gov.tech.sg" android:host="ctf" android:pathPrefix="/howtogetthisflag"/>
            </intent-filter>
        </activity>
``````
We see that this activity can be activated via a deep link as it includes the BROWSABLE category. A deep link is a link which takes you to directly to a functionality within an app. In this case, we can craft the special deep link from the above manifest. The deep link can be crafted in the format <scheme>://<host>/<path>, from the above manifest, we see the data <data android:scheme="gov.tech.sg" android:host="ctf" android:pathPrefix="/howtogetthisflag"/>, this gives us the deeplink gov.tech.sg://ctf/howtogetthisflag which we can access to activate ViewActivity. We can do this via adb with sg.gov.tech.ctf.mobile as the package name of the application.
        
``````
root@kali:/opt/genymobile/genymotion/tools# ./adb shell am start -W -a "android.intent.action.VIEW" -d "gov.tech.sg://ctf/howtogetthisflag" sg.gov.tech.ctf.mobile
``````

We should arrive on a SECRET VAULT page.

![ViewActivity](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(6).png)

#### Dynamic Analysis: 
Back to dynamic analysis, I clicked on the "CLICK ME" button, we get a popup that says "Something's happening...", this can help us identify which part of the code is occuring when the button is clicked. BurpSuite did not log any web requests, which means that a client-side check must be happening.

#### Static Analysis: 
Back to static analysis I analysed the OnClick() function in ViewActivity

``````
public void onClick(View v) {
            if (ViewActivity.this.a() == 1720543) {
                a.b.k.c.a builder = new a.b.k.c.a(ViewActivity.this);
                View view = LayoutInflater.from(ViewActivity.this).inflate(R.layout.custom_alert, null);
                TextView details = (TextView) view.findViewById(R.id.alert_detail);
                ((TextView) view.findViewById(R.id.title)).setText("Congrats!");
                details.setText(R.string.test);
                f.a.a.a.a.e.b.a().d(Boolean.valueOf(true));
                builder.h("Proceed", new C0075a());
                builder.f("Close", new b());
                builder.k(view);
                builder.l();
                return;
            }
            Toast.makeText(ViewActivity.this, "Something's happening...", 0).show();
            Toast.makeText(ViewActivity.this, "Maybe not.", 0).show();
        }
``````
The function, ViewActivity.this.a() is being executed and the resulted and it is being checked if it equals to 1720543.

Let's further examine ViewActivity.this.a(),

``````
public int a() {
        int retVal = new Random().nextInt();
        if (retVal < 0) {
            return retVal * -1;
        }
        return retVal;
    }
``````
It seems that a random integer is being generated and the next integer will be stored in the variable retval, if retVal is negative, it will be multiplied by -1 to become positive and retVal is returned.

Since a random number is generated, it is difficult to obtain the exact value of 1720543. Hence, we have to modify the code in Smali to bypass the check

### Step 2: Modifying authentication functionality
We can disassemble the APK using this apktool
``````
apktool d -f -r mobile-challenge.apk
``````
We can easily modify the if check just as we did for True or false?, but that would be no fun. Instead we could modify the function ViewActivity.this.a() such that it will always return 1720543.

To do this we find the code
``````
nano ./mobile-challenge/smali/sg/gov/tech/ctf/mobile/User/'ViewActivity.smali'
``````

The code block for the function we can modify is shown below
``````
# virtual methods
.method public a()I
    .locals 2

    .line 79
    new-instance v0, Ljava/util/Random;

    invoke-direct {v0}, Ljava/util/Random;-><init>()V

    .line 80
    .local v0, "random":Ljava/util/Random;
    invoke-virtual {v0}, Ljava/util/Random;->nextInt()I

    move-result v1

    .line 81
    .local v1, "retVal":I
    if-gez v1, :cond_0

    .line 82
    mul-int/lit8 v1, v1, -0x1

    .line 84
    :cond_0
    return v1
.end method
``````

To make sure we always return the value of 1720543, we can introduce the code at the start of the function. We first need to initialise a register with the constant 1720543 and then return this value of this register. We can add these two instructions just below .line 79 shown below.
`````
...
    .line 79
    const v1, 1720543

    return v1

    new-instance v0, Ljava/util/Random;

    invoke-direct {v0}, Ljava/util/Random;-><init>()V
...
`````` 

### Step 3: Bypassing the check,
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

And now when we visit the hidden functionality again,
``````
root@kali:/opt/genymobile/genymotion/tools# ./adb shell am start -W -a "android.intent.action.VIEW" -d "gov.tech.sg://ctf/howtogetthisflag" sg.gov.tech.ctf.mobile
``````

Clicking the button gives us a Base64 encoded flag as there is a trailing = sign at the end - Z292dGVjaC1jc2d7SV9oMFAzX3VfRDFEX04wVF9DbDFjS19VUl9XQHlfSDNyM30= 
which can be decoded here - https://www.base64decode.org/, into the real flag.

### Flag: govtech-csg{I_h0P3_u_D1D_N0T_Cl1cK_UR_W@y_H3r3}

## Mitigations
Checks should be performed on server-side. All intentional functionality of the application should be documented. Constant checks on the code should be carried out such that there is no hidden functionality which is not documented.

### Writeup by: Haxatron

