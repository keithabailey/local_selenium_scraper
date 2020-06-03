# Local Python Selenium Scraper

For many of us, getting meaningful data for our analyses is one of the more difficult parts of our jobs and one that does not always appear automatable. As someone who strives to elevate myself and my teams away from the production of data sets, this is particularly frustrating. Luckily, many companies provide APIs to make it easier to fetch the data you need and there are great tools such as ACL Robotics from Galvanize that make it even easier to do this, with connectors for a wide variety of systems, both cloud and on premise.

Sadly, this is not the case with all providers and so we are left to our manual efforts to fetch what we need, especially when the provider generates downloadable reports. Using three tools we can automate away the entire data-fetch process. Fair warning, there is some setup required first, but its worth it. Be careful which sites you scrape (don&#39;t hammer small guys sites for example), review their fair use policies and be a good citizen.

One of the reasons for using Selenium to do this has been to allow download of files of page scraping where user login is required. For simple sites this is not an issue, but this does not handle captcha or 2fa.

## Setup

Before you use run_scrape.py, check that /bin/chromedriver.exe matches your instance of chrome. As chrome auto-updates, you will likely be forced to repeat this step periodically. You can find the latest version here and replace as needed:

https://chromedriver.chromium.org/downloads

Dependencies can be found in the requirements.txt as normal.

### run_scrape.py

The main script fires reads in the xlsx file in docs, converts it to a dictionary for processing, triggers all noted commands in Selenium and ultimately returns the status of that effort, detailing each attempt with any supporting files and where they have been saved (into a temp folder).

As this project was initially being used to download reports from Concur that otherwise have to be done manually, I have also included very specific steps to fetch the donlaoded report, unzip and overwrite and retain the Concur output needed, ready for processing by whichever application needs it.

For most use cases you will want to separate the processing of the results from the manipulation of downloaded reports / page source which I have not done here. 
