# Challenge: Find the leaking bucket!
It was made known to us that agents of COViD are exfiltrating data to a hidden S3 bucket in AWS! We do not know the bucket name! One tip from our experienced officers is that bucket naming often uses common words related to the company’s business.
Do what you can! Find that hidden S3 bucket (in the format “word1-word2-s4fet3ch”) and find out what was exfiltrated!

Company Website: https://d1ynvzedp0o7ys.cloudfront.net/

## Summary
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

## Process
From the website we see that there are words that are shown.
