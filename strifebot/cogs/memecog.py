from discord.ext import commands
import sys
import logging
import discord
import random


memes = [
         {
           'trigger': "test1",
           'responses': ["test1 1"]
         },
         {
           'trigger': "both sides",
           'responses': ["Perfectly balanced, as all things should be. <@290374730991665154>"]
         },
         {
           'trigger': "test4",
           'responses': ["test4 1", "test4 2", "test4 3"]
         },
         {
           'trigger': "test5",
           'responses': ["test5 1"]
         },
         {
           'trigger': "test6",
           'responses': ["test6 1", "test6 2"]
         },
        ]

memes_case_insensitive = [
        {
           'trigger': "test3",
           'responses': ["test3 1", "test3 2", "test3 3"]
         },
        ]

#f = open("strife.conf", "r")
#for line in f:
    #if line[0] == "#":
        #continue
    #elif "commoners_roleid" in line:
        #commoners_roleid = int(line.split("=")[-1:][0].strip())
    #elif "owner_roleid" in line:
        #owner_roleid = int(line.split("=")[-1:][0].strip())
    #elif "admin_roleid" in line:
        #admin_roleid = int(line.split("=")[-1:][0].strip())
    #elif "seniorMod_roleid" in line:
        #seniorMod_roleid = int(line.split("=")[-1:][0].strip())
    #elif "moderator_roleid" in line:
        #moderator_roleid = int(line.split("=")[-1:][0].strip())
    #elif "clerk_roleid" in line:
        #clerk_roleid = int(line.split("=")[-1:][0].strip())
#
    #elif "cbbb" in line:
        #cbbb = int(line.split("=")[-1:][0].strip())
#
    #elif "rules_channelid" in line:
        #rules_channelid = int(line.split("=")[-1:][0].strip())
    #elif "roles_channelid" in line:
        #roles_channelid = int(line.split("=")[-1:][0].strip())
    #elif "general_channelid" in line:
        #general_channelid = int(line.split("=")[-1:][0].strip())

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author == self.bot.user:
                return
            for meme in memes:
                if meme["trigger"] in message.content:
                    await message.channel.send(random.choice(meme["responses"]))
                    return
            #Case insensitive trigger
            for meme in memes_case_insensitive:
                if meme["trigger"] in message.content.lower():
                    await message.channel.send(random.choice(meme["responses"]))
                    return
        except:
            await ctx.send('Error memery has failed. This is a cat-test-trophy')

    #__________________________________________________



def setup(bot):
    bot.add_cog(MemeCog(bot))
