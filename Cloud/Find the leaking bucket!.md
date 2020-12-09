# Challenge: Find the leaking bucket!
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

Gobuster - URL Fuzzer (https://github.com/OJ/gobuster)

Amazon EC2 Instance (Optional) - as a proxy (

Proxychains (Optional) - to force Gobuster to pivot through the EC2 instance 

## Process:
From the website we see that there are words that are shown, from the challenge description we see that we have to use the common words related to the company's business.

### Step 1: Building the Wordlist
One tool we can use to extract the words is CeWL, CeWL is a tool that helps us generate wordlists from a website based on the words shown there

``````
cewl https://d1ynvzedp0o7ys.cloudfront.net/ > wordlist.txt
``````
This tool however does not work on pictures and it looks like we have to manually extract keywords from the Steve Jobs quote, to be safe I just extracted the entire Steve Jobs quote. I cleaned up the wordlist by removing capital letters as S3 buckets cannot consist of capital letters (https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) as well as the CeWL header which generates everytime CeWL is loaded. The final wordlist can be found here - https://github.com/BunchOfBytes/STF-2020/blob/main/Cloud/wordlist.txt.


