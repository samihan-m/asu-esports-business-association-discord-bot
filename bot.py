'''
Created on Mar 11, 2021

@author: ssmup
'''
#for navigating through file system + checking if on heroku or not
import os

#for doing discord bot things
from discord.ext import commands
import discord

#for connecting to the right discord bot
from creds import TEST_TOKEN

initial_extensions = ['hitmarker',
                      'lol']

bot = commands.Bot(command_prefix='!eba ')

if __name__ == '__main__':
    #Load all extensions
    for extension in initial_extensions:
        bot.load_extension(extension)
        
def heroku_check():
    '''
    Check if the program is currently running on the Heroku deployment or in debug (coding) mode.
    '''
    #Check if on Heroku
    on_heroku = False
    if 'ON_HEROKU' in os.environ:
        on_heroku = True
        
    return on_heroku

DISCORD_TOKEN = ''
#Initialize different things based on if Heroku or not.
if(heroku_check()):
    #Use heroku environment value
    #grab discord token from configvars
    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
else:
    #grab discord token from creds
    DISCORD_TOKEN = TEST_TOKEN

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    await bot.change_presence(activity=discord.Game(name='!eba help'))
#invite link with proper perms:
#Prod
#https://discord.com/api/oauth2/authorize?client_id=816860985859375144&permissions=93184&scope=bot    

#TESTING
#https://discord.com/api/oauth2/authorize?client_id=819735028736851990&permissions=93184&scope=bot
    
    
bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
        