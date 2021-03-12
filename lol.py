'''
Created on Mar 11, 2021

@author: ssmup
'''

import discord
from discord.ext import commands

class LeagueOfLegends(commands.Cog):
    '''
    classdocs
    '''

    def __init__(self, bot):
        '''
        Constructor
        '''
        self.bot = bot
        
    @commands.command(name='opgg', help='!eba opgg <SummonerName (no spaces)> [NA/EU/KR/..] - Get the op.gg link to a certain summoner.')
    async def get_op_gg(self, ctx, summoner_name, region=None):
        '''
        Create an op.gg summoner search link from the given summoner name and region (defaults to NA) and sends it to the provided context.
        '''
        regions = ['kr', 'jp', 'na', 'euw', 'eune', 'oce', 'br', 'las', 'lan', 'ru', 'tr', 'sg', 'id', 'ph', 'tw', 'vn', 'th']
        
        #First, check if region is in the given list.
        #But also check if region is defined.
        if(region is None):
            #Region defaults to North America
            url_prefix = 'na'
            await ctx.send('Defaulting to North America.')
        elif(region in regions):
            #Check if the region is within the given list.
            url_prefix = region
            if(region == 'kr'):
                #The korean op.gg is actually www.op.gg, not kr.op.gg
                url_prefix = 'www'
            
        else:
            #Bad region given.
            await ctx.send('You entered a bad region, or maybe you entered the summoner name with spaces.')
            await ctx.send('Here are your region options:' + ('[%s]' % ', '.join(map(str, regions))).upper())
            await ctx.send('Try again.')
            return
            
        #Make sure summoner name is given
        if(summoner_name is None):
            await ctx.send('Error: Next time, enter a summoner name.')
        #Construct link
        link = 'https://' + url_prefix + '.op.gg/summoner/userName=' + summoner_name
        await ctx.send(link)
    
def setup(bot):
    '''
    Adds the LoL command Cog to the bot.
    '''
    bot.add_cog(LeagueOfLegends(bot))
        