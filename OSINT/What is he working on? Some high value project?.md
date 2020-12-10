# Challenge: What is he working on? Some high value project? (OSINT-1)

The lead Smart Nation engineer is missing! He has not responded to our calls for 3 days and is suspected to be kidnapped! Can you find out some of the projects he has been working on? Perhaps this will give us some insights on why he was kidnapped…maybe some high-value projects! This is one of the latest work, maybe it serves as a good starting point to start hunting.

Flag is the repository name!

Link: https://www.developer.tech.gov.sg/communities/events/stack-the-flags-2020

## Summary:

Players had to find the name of the repository of a high-valued project the employee was working on. They had to pivot from one information to another to gather more repositories and eventually find the correct one.

## Process:

We are given a link to a GovTech event page for Stack The Flags! Since there was no information that stood out, perhaps the required information was buried somewhere in the HTML, so the first thing we did was to Inspect Element,
We found this:

``````
<!-- Will fork to our gitlab - @joshhky -->
``````
Two keywords stand out here - @joshhky which is probably the username of the employee we are looking for and GitLab, which is probably the name of the site where the repository is stored.

To find joshhky, we googled how to search for users on Gitlab, we come across this - https://docs.gitlab.com/ee/user/project/pages/getting_started_part_one.html

``````
You created a project called blog under your username john, therefore your project URL is https://gitlab.com/john/blog/. Once you enable GitLab Pages for this project, and build your site, it will be available under https://john.gitlab.io/blog/.
``````
So we tried to visit https://gitlab.com/joshhky/ to see if we are able to obtain his profile page which it did. From his profile page we see two repos, 
myownwebsite and curriculum-vitae. It is important in OSINT investigations that we note down all the information we can extract to keep a profile of our target, these information can be used for later. So we note the two possible repository names down

Going under Groups, we see he is part of the KoroVax group. - https://gitlab.com/korovax

On the Korovax page we see 3 repositories, korovax-employee-wiki, korovax-swap-test-registry-backend-api-docs and manuka. 

Next, we checked all the repositories we've gathered so far to see if we are able to obtain anymore information 

Under korovax-employee-wiki - https://gitlab.com/korovax/korovax-employee-wiki, we see the following 
``````
Todo:
- The employee wiki will list what each employee is responsible for, eg, Josh will be in charge of the krs-admin-portal
- Please note that not all repository should be made public, relevant ones with business data should be made private
``````
Which means that another possible repository is krs-admin-portal

Putting together all the possible repositories,
``````
krs-admin-portal
korovax-employee-wiki
korovax-swap-test-registry-backend-api-docs
manuka
myownwebsite
curriculum-vitae
``````
We tried all 6 repositories and we found that krs-admin-portal is the correct high-valued project he is working on.
### Flag: govtech-csg{krs-admin-portal}
