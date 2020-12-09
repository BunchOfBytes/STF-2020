# Challenge: Unlock Me (Web-1)
Our agents discovered COViD's admin panel! They also stole the credentials minion:banana, but it seems that the user isn't allowed in. Can you find another way?

Website: http://yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg:41031/

## Summary:
The web application was vulnerable to CVE-2016-10555 where the algorithm type is not properly being checked. More can be found here: https://nvd.nist.gov/vuln/detail/CVE-2016-10555.

Relevant CWE:

CWE-287: Improper Authentication (https://cwe.mitre.org/data/definitions/287.html)

## Tools used:
OS - Kali Linux

BurpSuite - to inspect and modify web requests

JSON Web Attacker BurpSuite plugin - helps to automate the attack

## Process:
According to Wikipedia, a JSON Web Token is an Internet standard for creating data with optional signature and/or optional encryption whose payload holds JSON data such as roles and usernames. The tokens are signed either using a private secret or a public/private key, in other words, it is similar to a cookie which carries information about the user.
JSON Web tokens can be easily spotted using the following methods:

1) If the string starts with "eyJhbGci...", it is most likely a JWT token
2) If the string consists of two dots (.), it is most likely a JWT token

On the website I logged into the website using the provided credentials minion:banana. I proxied it forward through Burp Suite. I then get this following request I made 
```````
GET /unlock HTTP/1.1
Host: yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg:41031
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg:41031/
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1pbmlvbiIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjA3NTI5MTMxfQ.XZD1sFxPkkV9hHtttEwZm9GuY7zcIBeL3bNRq_QEzjXawGtrxUWKfiA4X_KA2Kyb7RCq4b6fjFBGsDCfY28g-WRw0-tRPOU3e1qmn_Uo8HRPS-2ZAR2ObJEGbU-bKiCVLZc9QyZb9UEIb_MBRDjk_w3lR4d1UYi_THx6obMFbqbijV9vRdZqp6NuzwnrE5_Br2XGXuD17w7s1WAQ6Y72yP4IVdKdUz7s-gJgnk8Y5Bed5tcEWwHtKGlLa_oyR6iskCWijHU1tp-p-xyNTbOzSjd_bNF3l59MF0ChwRqDP_wiGfhEEO5xWnVpsw3JMIghVJ6D77UkA19F-yI-KY8qGgKDI71dFgLjI0ITx6qpTB3N-65ow8NYzDpc3ytSQllcAVw_mFBPlaC0vm92al5YqXdDzdyALgFSvS-EpX0pf-QXgt7DhCsZU_aCXfmArC75oVtWwTRTBg_cT5GdPKoEAfOjsB9x7uR1tsKxsV06INoA83_yo9Wi9gGPYjHiMg7XDgSE_3KGq8CJMgIeFpoCSkvJy7C8tbWyA9KDWz9cBENy9ERF2DNggNjwpmx10yKP1IW4VR5nr6NTIMuUnuanfzOKmAVvTx44X-4pzDXnyYbXbu-5XASpPpNfdJh9qfmfysNX1axyzoKSp08kycz8hCnbgZ4t2CCKnLIXzzEgY9E
Connection: close
Cookie: __cfduid=d7dea684ee9d33772602f489a7f40dfca1607085880
If-None-Match: W/"2c-HIo8OazkINs/Y63UTfaXAuuMrWk"
```````
Aha! A JWT token can be found under the Authorization: Bearer component. Go ahead and copy the JWT token into https://jwt.io/ as shown.

![JWT.IO](
