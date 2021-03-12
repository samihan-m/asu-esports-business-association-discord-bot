# asu-esports-business-association-discord-bot
 A Discord bot built by me for the Arizona State University Esports Business Association. 
 
 Currently has several different types of features:
 
 <b>Hitmarker</b>
 
 When requested, scans the website Hitmarker for new internship and volunteering listings and posts them into the Discord channel.
 
 Built specifically for the Esports Business Association club at Arizona State University, and as a result, does not work as intended when invited to multiple servers, as the list that tracks which listings have already been displayed is not unique for each server.
 
 Uses Selenium to render the Hitmarker page before passing it to a BeautifulSoup object to parse it for listing information.
 Calculates hash values for each job listing (using title, employer, and link to the job listing page) and uses that to see if the job listing is unique or has already been read by the bot. New hashes are stored in a list so as to provide the bot with a list of already-read listings to compare freshly-read data from the webpage.
 
 The advantage of using hashes that incorporate the job listing page link is that a new job listing with the same title and employer will result in a new hash because it will have a new URL.

<b>League of Legends</b>

When commanded, it generated an op.gg link for a given League of Legends account by taking the username and region of the account.
