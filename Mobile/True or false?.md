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

burpsuite - to test for any web requests

## Setup:
Install genymotion (https://docs.genymotion.com/desktop/3.0/01_Get_started/012_Installation.html). Be sure to install an SDK of 21 or higher as the minSdkVersion specified in AndroidManifest.xml is 21.
See here if you want to figure out how to configure BurpSuite with genymotion (Ignore part on Frida) - https://arben.sh/bugbounty/Configuring-Frida-with-Burp-and-GenyMotion-to-bypass-SSL-Pinning/

## Process:
### Step 1: Analysing authentication functionality
#### Dynamic Analysis:
I performed dynamic analysis on the app first. Testing the app functionality, I noticed that there are no requests being made on BurpSuite. This is a big red flag for us that the code is performing checks on the client side!

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


### Flag: govtech-csg{}


## Mitigations
Authentication should be performed on server-side. 

### Writeup by: Haxatron

