# Challenge: Who are the possible kidnappers? (OSINT-6)
Perform OSINT to gather information on the organisation’s online presence. Start by identifying a related employee and obtain more information. Information are often posted online to build the organization's or the individual's online presence (i.e. blog post). Flag format is the name of the employee and the credentials, separated by an underscore. For example, the name is Tina Lee and the credentials is MyPassword is s3cure. The flag will be govtech-csg{TinaLee_MyPassword is s3cure}

Addendum:
- Look through the content! Have you looked through ALL the pages? If you believe that you have all the information required, take a step back and analyse what you have.
- In Red Team operations, it is common for Red Team operators to target the human element of an organisation. Social medias such as "Twitter" often have information which Red Team operators can use to pivot into the organisation. Also, there might be hidden portal(s) that can be discovered through "sitemap(s)"?

## Summary: 
We had to find a password of an employee of Korovax from Twitter using advanced search functions.

## Process:
From the OSINT-1 the organisation we have identified is Korovax, doing a simple Google search would lead us to their website, if we want to we can perform some Google Dorking magic
to reveal their website.

![](https://github.com/BunchOfBytes/STF-2020/blob/main/Screenshot%20(20).png)

The query above just searches for indexed URLs with the word "korovax" on it,  this is a great way to search for company websites and internal company websites! For more recipes for queries you can check here! - https://www.exploit-db.com/google-hacking-database

From this we can identify two websites with korovax in the domain - korovax.org and fb.korovax.org!

Visiting korovax.org, we see that it is just a blog site. We checked all the blogposts, in particular the blogpost "New Tool I Found" -https://csgctf.wordpress.com/2020/10/21/new-tool-i-found/, we see that Sarah Miller is the author of the blogpost. In the team page (https://csgctf.wordpress.com/team/), we identify a few emails which we can use later. In the post, we can extract a few pieces of information,
1) Sarah uses a tool called Twitter Archiver and 2) There is a secret social media that they share, presumably, fb.korovax.org.

We can check the robots.txt file to enumerate more pages, http://korovax.org/robots.txt.

````````
# If you are regularly crawling WordPress.com sites, please use our firehose to receive real-time push updates instead.
# Please see https://developer.wordpress.com/docs/firehose/ for more details.

Sitemap: https://csgctf.wordpress.com/sitemap.xml
Sitemap: https://csgctf.wordpress.com/news-sitemap.xml

User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-login.php
Disallow: /wp-signup.php
Disallow: /press-this.php
Disallow: /remote-login.php
Disallow: /activate/
Disallow: /cgi-bin/
Disallow: /mshots/v1/
Disallow: /next/
Disallow: /public.api/

# This file was generated on Sat, 28 Nov 2020 19:14:50 +0000
````````

Seems that korovax.org is just a domain which points to csgctf.wordpress.com. 

It also can be seen that there is a sitemap, which we can visit, https://csgctf.wordpress.com/sitemap.xml as detailed above. A sitemap contains a map of all the documented pages stored in the website! We can visit all the URLs found in the website, in particular, https://csgctf.wordpress.com/oh-ho/. sitemap.xml and robots.txt is incredibly useful for revealing more attack surface in real life!

````````
you found me!

I forgot my password to our KoroVax social media page.

I think it’s stored on our corporate page with …blue…something….communication…

Cant remember now. Would have to look through my archived tweets!
````````

We remember Sarah Miller talking about archived tweets, going to this URL - https://csgctf.wordpress.com/2020/10/01/example-post-3/ we identify at the bottom

````````
For more information, visit http://www.KoroVax.org and connect with us on Twitter @scba and LinkedIn
````````

We get a Twitter handle which when we search on Twitter, belongs to a real user named Sarah Miller! - https://twitter.com/scba

So putting the information we have, we are search for a password which has the pattern …blue[...]communication… on @scba's account on Twitter.

We used the Twitter advanced search function. We can access the Twitter advanced search here with the keywords "blue" and " communication" - https://twitter.com/search-advanced. We tried multiple searches with this function. The one that actually worked was the one with communications instead of communication. Input the following:
````````
"All of these words": blue communications (from:scba)
"Mentioning these accounts": scba
````````

Which will lead us to this tweet
````````
That's exactly it. Blue sky communications vs grey sky communications. #smemchat
````````
Bingo! That means that the password is Blue sky communications. We can try testing this on the internal social media they mentioned here - http://fb.korovax.org. Going back to the team page - https://csgctf.wordpress.com/team/. We can identify Sarah's email as sarah.miller@korovax.org and use it to login
````````
Email: sarah.miller@korovax.org
Password: Blue sky communications
````````
And we managed to login.

### Flag: govtech-csg{SarahMiller_Blue sky communications}

### Writeup by: Haxatron

