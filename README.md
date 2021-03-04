# Hitmarker-Post-Discord-Notifier
 A Discord bot that when requested scans the website Hitmarker for new internship and volunteering listings and posts them into the Discord channel.
 
 Uses Selenium to render the Hitmarker page before passing it to a BeautifulSoup object to parse it for listing information.
 Calculates hash values for each job listing (using title, employer, and link to the job listing page) and uses that to see if the job listing is unique or has already been read by the bot. New hashes are stored in a list so as to provide the bot with a list of already-read listings to compare freshly-read data from the webpage.
 
 The advantage of using hashes that incorporate the job listing page link is that a new job listing with the same title and employer will result in a new hash because it will have a new URL.
