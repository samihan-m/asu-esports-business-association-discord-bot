'''
Created on Mar 3, 2021

@author: ssmup
'''
#for parsing the page easily
from bs4 import BeautifulSoup

#for rendering a page's javascript before parsing with beautifulsoup
from selenium import webdriver

#for calculating hashes of job listing pages when checking if a posting is new
import hashlib

#for using time.sleep to give selenium-loaded pages time to load
import time

#importing discord bot token
from creds import DISCORD_TOKEN

if __name__ == '__main__':
    
    #information for making selenium work on heroku
    import os

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #this code and the code above needs to be toggled to make things work on Heroku vs localhost
    '''
    #initialize selenium webdriver
    #pointing to chromedriver file
    path_to_webdriver = r'./chromedriver.exe'
    #pointing to chrome exe
    options = webdriver.ChromeOptions()
    options.binary_location = "D:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    #initializing driver
    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=options)
    '''
    
    def readListings(driver):
        '''
        Read all job listings from the hitmarker URL found at the top of this function with the passed selenium webdriver.
        '''
        #Hitmarker job search: Parameters: paid internship, unpaid internship, volunteer
        URL = "https://hitmarker.net/jobs?location=usa&contract=internship+internshipUnpaid+volunteer&industry=esports"
        
        #get page via a browser, thus executing javascript
        driver.get(URL)
        '''
        TODO
        Add a condition for time.sleep to run until (maybe until 'Nothing more to see' isn't visible on the page?)
        '''
        #give the page 5 seconds to load parameters properly
        time.sleep(5)
        page = driver.page_source
        
        #create beautifulsoup object from rendered page
        soup = BeautifulSoup(page, "html.parser")
        
        #get all of the job listing divs
        job_listings = soup.find_all(class_="border-t border-charlie pt-4 mb-4")
        
        try:
            #for each job listing, grab the information, create an object, and add it to a list
            job_listings_list = []
            for listing in job_listings:
                job_title = listing.find(class_="font-bold truncate").text
                job_location = listing.find(class_="text-echo truncate ml-2").text
                job_employer = listing.find(class_="text-foxtrot font-bold truncate").text
                listing_link = listing.find('a', class_="flex-auto flex items-start min-w-0 hover:text-brand")['href']
                
                employer_image = listing.find(class_="w-full h-full rounded-full")['src']
                
                #create dict for the job listing
                job_listing = {'title': job_title, 'location': job_location, 'employer': job_employer, 'image': employer_image, 'link': listing_link}
                
                #add it to the job listings list
                job_listings_list.append(job_listing)
                
                #output to console the read data, if desired
                #print(job_title, job_location, job_employer, listing_link, sep="\n")
                #print('')
            
            #close the opened webpage when done
            #driver.close()
            
            #return all of the read jobs
            return job_listings_list
        except:
            #even if there is an error in reading from the page, the webpage closes
            #driver.close()
            
            #create an error listing and return that so when it's posted via the bot there is an indication it is broken
            error_listing = {'title': 'ERROR', 'location': 'READING LISTING FROM SITE', 'employer': 'CHECK CODE', 'link': 'www.github.com/samihan-m'}
            return [error_listing]
    
    def saveNewListings(job_listings_list):
        '''
        Take a list of job_listings objects (see readListings), 
        checks if any are new (via using a hash function on all of the information in the job_listing dict concatenated),
        and saves the new ones to a file.
        Returns a list of all new job_listings.
        '''
        
        #debug print
        #for listing in job_listings_list:
        #    print(listing['title'])
        
        
        for job_listing in job_listings_list:
            #check if the listing is the ERROR listing
            if(job_listing['title'] != 'ERROR'):
                #calculate the hash of the HTML document found at the link to determine if the listing got updated
                '''
                #fetch the job posting information document
                listing_info_page = requests.get(job_listing['link'])
                #get the hash of the document
                hash_input = bytes(listing_info_page.text, 'utf-8')
                '''
                #get the hash of the concatenation of all of the job_listing information
                string_to_hash = job_listing['title']+job_listing['location']+job_listing['employer']+job_listing['link']
                hash_result = getHash(string_to_hash)
                #debug print
                #print('Hash for', job_listing['title'] + ':', hash_result)
                #add the hash value to the listing, for additional processing later
                job_listing['hash'] = hash_result
            else:
                #do error processing
                print('please implement error handling for the error listing at saveNewListings()')
                #exit the function because without hashes i can not check if the listings are new or not
                break
                
        #now check which, if any, listings in job_listings_list are new and need to be saved to the text file
        
        #read all of the old listings hash values
        previous_listing_hashes = []
        #open the file with all of the saved listings
        with open(r'./listings.txt', 'r') as saved_listings_file:
            #read each line (each line is a hash)
            for line in saved_listings_file:
                #remove the final character of each line (the newline character) before adding it to the previous hash list
                previous_listing_hashes.append(line[:-1])
                
        #DEBUG PRINT
        #print(previous_listing_hashes)
        
        #a list containing new listings that will be returned
        new_listings = []
        #now compare the just-read hashes to the saved hashes to see which are new   
        for job_listing in job_listings_list:
            #check if the hash is in the list of saved hashes
            listing_hash = job_listing['hash']
            if(listing_hash not in previous_listing_hashes):
                print("New listing found:", job_listing['title'])
                #this particular listing is new, so add it to the list of new listings, and add the hash to the file holding old hashes
                new_listings.append(job_listing)
                previous_listing_hashes.append(listing_hash)
                
        #DEBUG PRINT
        #print(previous_listing_hashes)
                
        #write the list of old hashes to the saved listings file again
        with open(r'./listings.txt', 'w') as saved_listings_file:
            for listing_hash in previous_listing_hashes:
                #save each hash on it's own line (that is what the newline char is doing)
                saved_listings_file.write(listing_hash+'\n')
        
        #return the list of listings that are new/updated
        return new_listings
    
    def getHash(hash_input):
        '''
        Calculates and returns the hexadecimal hash value of the passed string.
        '''
        #converting input into encoded, hash-safe bytes
        input_as_bytes = bytes(hash_input, 'utf-8')
        hasher = hashlib.md5(input_as_bytes)
        hash_result = hasher.hexdigest()
        #return hash value
        return hash_result
    
    def createPosts(new_listings):
        '''
        Takes a list of new listings for which to create Discord posts and send them to the channel.
        '''
        #internships channel ID: 752417364938850434
    '''
    new_listings = saveNewListings(readListings(driver))
    for listing in new_listings:
        print(listing['title'])
    '''
          
    # bot.py
    import os
    from dotenv import load_dotenv
    
    # 1
    from discord.ext import commands
    import discord
    
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    # 2
    bot = commands.Bot(command_prefix='!hitmarkerbot ')
    
    
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name='!hitmarkerbot help'))
        print(f'{bot.user.name} has connected to Discord!')
    #invite link with proper perms:
    #https://discord.com/api/oauth2/authorize?client_id=816860985859375144&permissions=93184&scope=bot
    
    @bot.command(name='update', help='Have the bot search hitmarker.com for any new listings, and post them to this channel.')
    async def updateListings(ctx):
        await ctx.send("Searching...\nPlease wait...")
        new_listings = saveNewListings(readListings(driver))
        print(new_listings)
        #set the response embed settings based on whether or not new listings exist
        if len(new_listings) == 0:
            #No new listings
            #Show an embed stating there is nothing new
            embed = discord.Embed(
            color = discord.Color.red(),
            description = "Check back later!",
            title = "No New Listings"
                )
            
            await displayEmbed(ctx, embed)
        else:
            #New listings!
            #Show an embed stating there is something new
            embed = discord.Embed(
            color = discord.Color.green(),
            description = "Check out these opportunities:",
            title = "New Listings!"
                )
            await displayEmbed(ctx,embed)
            
            #Show embeds with information for each listing
            for listing in new_listings:
                embed = discord.Embed(
                    color = discord.Color.green(),
                    description = listing['location'],
                    title = listing['title'] + '\n' + listing['link']
                    )
                embed.set_thumbnail(url=listing['image'])
                embed.set_author(name = listing['employer'])
                await displayEmbed(ctx, embed)
            
            #Show a 'finished' embed
            embed = discord.Embed(
                color = discord.Color.green(),
                description = "Done listing all new Hitmarker job postings",
                title = "All Done"
                )
            await displayEmbed(ctx, embed)
    
    async def displayEmbed(ctx, embed):
        await ctx.send(embed = embed)
    
    @bot.command(name='clear', help='Clear the bot\'s memory so it will repost old listings it\'s already seen')
    async def clearMemory(ctx):
        '''
        Opens the file that holds old listing hash values in write mode, clearing it.
        '''
        await ctx.send('Clearing memory...\nPlease wait...')
        
        #Open the file for writitng (overwriting) then close it
        open(r'./listings.txt', 'w').close()
            
        await ctx.send('Memory cleared.')
        
    def getEmbedLink(text, link):
        '''
        Returns the formatted string required for a Discord embed to have the given text link to the given link.
        '''
        return '[' + text + '](' + link + ')'
    
    bot.run(DISCORD_TOKEN)
    pass