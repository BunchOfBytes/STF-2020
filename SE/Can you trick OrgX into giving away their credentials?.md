# Challenge: Can you trick OrgX into giving away their credentials? (SE-1)

With the information gathered, figure out who has access to the key and contact the person.

## Summary:
Players have to figure out the email of IT support and mail them with a keyword.

## Process:
Logging into Sarah Millers account on http://fb.korovax.org/ with the following credentials from the previous challenge (Who are the possible kidnappers?)
We see the following information:

`````````
William Birkin
about 2 months. 

...
wasnt it ictadmin@korovax.org or something
`````````

On a reply
`````````
Amanda Lee looks like it, but they don't respond all the time, only when there's specific content - haven't figure out what it is yet
`````````

The challenge description asks us to figure out who has access to a key and contact the person. Presumably, the ICT admins have these key and we have to email them using ictadmin@korovax.org with a secret keyword
to obtain a key. Visiting this page we extracted from the sitemap back from the previous challenge (Who are the possible kidnappers?) - https://csgctf.wordpress.com/never-gonna/

`````````
NEVER GONNA
Guys, IT was created for your use. Please include the keywords when sending the email. Thanks.


Realize your potential

Identify your weaknesses

Confront your fears

Know the unknown

Remedy the wrongs

Observe your surroundings

Learn from your mistakes

Let no one down
`````````

There is a mention of keyword above, we see that there is a message encoded when we read every capital letter of each short sentence, we get RICKROLL, could that be our keyword?

So we email ictadmin@korovax.org with RICKROLL and it turns out we receive this message:

`````````
congrats

ouroboros@korovax.org
Tue, Dec 8, 5:53 PM (3 days ago)
to me

excellent artist, here's your code, govtech-csg{CE236F40A35E48F51E921AD5D28CF320265F33B3}
















 39bc4f5150511ee7c3a703bdd615ed70f79002473d7f61d2dccfc397f7292b5e
 `````````
 ### Flag: govtech-csg{CE236F40A35E48F51E921AD5D28CF320265F33B3}
 
In the end, my team did not solve this before the end of the competition, but I guessed if we backtracked a little bit we would have been able to solve it. I guess the important lesson here is to always re-evaluate our information when conducting and OSINT investigation and not to make any assumptions such as "this information can only be used for XYZ in an investigation."
