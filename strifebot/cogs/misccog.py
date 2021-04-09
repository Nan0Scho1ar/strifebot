from discord.ext import commands
import sys
import logging
import discord
import random



f = open("nan0.playlist", "r")
nan0 = []
logs_channelid = "577806825844506625"
for line in f:
    nan0.append(line)
f = open("strife.conf", "r")
for line in f:
    if line[0] == "#":
        continue
    elif "commoners_roleid" in line:
        commoners_roleid = int(line.split("=")[-1:][0].strip())
    elif "owner_roleid" in line:
        owner_roleid = int(line.split("=")[-1:][0].strip())
    elif "admin_roleid" in line:
        admin_roleid = int(line.split("=")[-1:][0].strip())
    elif "seniorMod_roleid" in line:
        seniorMod_roleid = int(line.split("=")[-1:][0].strip())
    elif "moderator_roleid" in line:
        moderator_roleid = int(line.split("=")[-1:][0].strip())
    elif "clerk_roleid" in line:
        clerk_roleid = int(line.split("=")[-1:][0].strip())

    elif "cbbb" in line:
        cbbb = int(line.split("=")[-1:][0].strip())

    elif "rules_channelid" in line:
        rules_channelid = int(line.split("=")[-1:][0].strip())
    elif "roles_channelid" in line:
        roles_channelid = int(line.split("=")[-1:][0].strip())
    elif "general_channelid" in line:
        general_channelid = int(line.split("=")[-1:][0].strip())
    elif "bump_channelid" in line:
        bump_channelid = int(line.split("=")[-1:][0].strip())

async def getRulesEmbed():
    embedtext = '''
1. Do not violate the Discord terms of service, which includes posting indecent or illegal material. (https://discordapp.com/terms)  


2. Always attempt to engage politely and charitably wherever possible, especially when interacting with newcomers. Do ***NOT*** locally mute a user, report them to a member of staff.  


3. Doxing, or the dissemination of personal information via the internet, is not permitted in any way.  


4. Please try to keep all discussions within their appropriate channels - shitposting, trolling and memes belong in their respective channels.  


5. Do not engage in toxic or disingenuous conduct, especially that conduct which is contrary to either the *implicit* or *explicit* social contract of this server.  


6. Refrain from using our community only as a platform for self-promotion - this includes DM advertising.  


7. We reserve the right to record, at all times, any conversations that we deem of a sufficient quality to promote intellectual engagement on this platform.  


8. Follow the instructions of our staff - the rules are enforced according to their discretion, and any complaints are to be handled after the fact by a different member of staff; hence, argumentation regarding who has or has not broken the rules is largely out of order, though it may be tolerated by some of our staff.


***Failure to abide by these rules will result in moderation. "I didn't know" isn't a valid excuse.***

If you get banned, reflect on your actions, then apologize honestly and you'll probably be allowed back.

'''
    embed=discord.Embed(title="***Nameless Debates II***", description=embedtext, colour=0x7eff00)
    embed.add_field(name="Server Guidelines", value="http://bit.ly/NDIIGuidelines", inline=True)
    embed.add_field(name="TLDR Guidelines", value="http://bit.ly/NDTLDR", inline=True)
    embed.add_field(name="Role Reification", value="http://bit.ly/ReactionRoles", inline=True)
    embed.add_field(name="Ranking Rationale", value="http://bit.ly/RankingRationale", inline=True)
    embed.add_field(name="Mediation Manual", value="http://bit.ly/NDMediationManual", inline=True)
    embed.add_field(name="Fallacy Finder", value="http://bit.ly/FallacyFinder", inline=True)
    embed.add_field(name="YouTube", value="https://www.youtube.com/namelessdebatesradio", inline=True)

    return embed

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            rules = self.bot.get_channel(rules_channelid)
            roles = self.bot.get_channel(roles_channelid)
            main = self.bot.get_channel(general_channelid)
            if main is not None and rules is not None and roles is not None and member.mention is not None:
                await main.send("Hello {}, welcome to Nameless Debates II. Please read {} and {} text channels before participating in the server (or else)!".format(member.mention, rules.mention, roles.mention))
        except:
          print("Error posting greeter message")

    #__________________________________________________

# START MISC COMMANDS

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def hello(self, ctx):
        """Display a friendly greeting"""
        sys.stdout.write(f'{ctx.message.author} ran command "hello"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "hello"')
        await ctx.send('Hello {}'.format(ctx.message.author.mention))

    @hello.error
    async def hello_error(self, ctx, error):
        logging.error('Command "hello" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def dump(self, ctx):
        """Dumps the logs"""
        sys.stdout.write(f'{ctx.message.author} ran command "dump"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "dump"')
        await ctx.send("```" + open("./../logs/nameless.log", "r").read()[-1994:] + "```")

    @dump.error
    async def dump_error(self, ctx, error):
        logging.error('Command "dump" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def dumpe(self, ctx):
        """Dumps the error logs"""
        sys.stdout.write(f'{ctx.message.author} ran command "dumpe"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "dumpe"')
        await ctx.send("```" + open("./../logs/nameless_error.log", "r").read()[-1994:] + "```")

    @dump.error
    async def dumpe_error(self, ctx, error):
        logging.error('Command "dumpe" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def greet(self, ctx):
        """Hiya"""
        sys.stdout.write(f'{ctx.message.author} ran command "greet"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "greet"')
        channel = ctx.message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await self.bot.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

    @greet.error
    async def greet_error(self, ctx, error):
        logging.error('Command "greet" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def thumbsup(self, ctx):
        """Thumbs up bruh"""
        sys.stdout.write(f'{ctx.message.author} ran command "thumbsup"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "thumbsup"')
        channel = ctx.message.channel
        await channel.send('Send me that 👍 reaction, mate')

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')

    @thumbsup.error
    async def thumbsup_error(self, ctx, error):
        logging.error('Command "thumbsup" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='ndjt')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def ndjt(self, ctx):
        """posts some of nan0scho1ar's music"""
        sys.stdout.write(f'{ctx.message.author} ran command "ndjt"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "ndjt"')
        count = int(ctx.message.content[len('|ndjt '):])
        bump_channel = self.bot.get_channel(bump_channelid)
        for i in range(0,count):
            song = random.choice(nan0)
            await bump_channel.send(song)

    @ndjt.error
    async def ndjt_error(self, ctx, error):
        logging.error('Command "ndjt" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='rules')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def rules(self, ctx):
        """Tells the mentioned member to read the rules"""
        sys.stdout.write(f'{ctx.message.author} ran command "rules"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "rules"')
        rules = self.bot.get_channel(rules_channelid)
        for member in ctx.message.mentions:
            await ctx.message.channel.send("{}, please read the rules and guidelines in the {} text chat.".format(member.mention, rules.mention))
            logs_channel = self.bot.get_channel(logs_channelid)
            logs_channel.send("Warned " + member.mention + " to read the rules.")
            await ctx.message.send(ctx.message.content)
        await ctx.message.delete()

    @rules.error
    async def rules_error(self, ctx, error):
        logging.error('Command "rules" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='postrules')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def postrules(self, ctx):
        """Posts the rules embed"""
        sys.stdout.write(f'{ctx.message.author} ran command "postrules"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "postrules"')
        em = await getRulesEmbed()
        await ctx.send(ctx.message.channel, embed=em)
        await ctx.message.delete()

    @postrules.error
    async def postrules_error(self, ctx, error):
        logging.error('Command "postrules" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='embed')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def embed(self, ctx):
        """Creates an embed and sets the title"""
        sys.stdout.write(f'{ctx.message.author} ran command "embed"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "embed"')
        await ctx.message.delete()
        ctx.message.content = ctx.message.content[len('|embed'):]
        em = discord.Embed(title=ctx.message.content, description="", colour=0x36393F)
        em.set_author(name=ctx.message.author.display_name, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        mentions = ""
        for member in ctx.message.mentions:
            mentions += member.mention + " "
        await ctx.message.channel.send(mentions, embed=em)

    @embed.error
    async def embed_error(self, ctx, error):
        logging.error('Command "embed" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='embedfield')  
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb) 
    async def embedfield(self, ctx):  
        """Adds a field to the embed"""
        sys.stdout.write(f'{ctx.message.author} ran command "embedfield"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "embedfield"')
        ctx.message.content = ctx.message.content[len('|embedfield'):]  
        await ctx.message.delete()  
        edited = False  
        async for history in ctx.message.channel.history(limit=20):  
            if edited == False:  
                msg = await ctx.message.channel.fetch_message(history.id)  
                if history.author == ctx.bot.user:  
                    for embed in msg.embeds:  
                        if embed.author.name == ctx.message.author.display_name:  
                            data = ctx.message.content.split("|")  
                            embed.add_field(name=data[0], value=data[1], inline=True)  
                            await msg.edit(embed=embed)  
                            edited = True  
                            mentions = ""  
                            for member in ctx.message.mentions:  
                                mentions += member.mention + " "  
                                if not mentions == "":  
                                    await ctx.message.channel.send(mentions) 

    @embedfield.error
    async def embedfield_error(self, ctx, error):
        logging.error('Command "embedfield" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='embedbody')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def embedbody(self, ctx):
        """Adds to the body of the embed"""
        sys.stdout.write(f'{ctx.message.author} ran command "embedbody"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "embedbody"')
        ctx.message.content = ctx.message.content[len('|embedbody'):]
        await ctx.message.delete()
        edited = False
        async for history in ctx.message.channel.history(limit=20):
            if edited == False:
                msg = await ctx.message.channel.fetch_message(history.id)
                if history.author == ctx.bot.user:
                    for embed in msg.embeds:
                        if embed.author.name == ctx.message.author.display_name:
                            if embed.description == discord.Embed.Empty:
                                embed.description = ""
                            desc = "{}\n{}".format(embed.description, ctx.message.content)
                            if len(desc) < 2000:
                                embed.description = desc
                                await msg.edit(embed=embed)
                                edited = True
                                mentions = ""
                                for member in ctx.message.mentions:
                                    mentions += member.mention + " "
                                if not mentions == "":
                                    await ctx.message.channel.send(mentions)

    @embedbody.error
    async def embedbody_error(self, ctx, error):
        logging.error('Command "embedbody" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='purge')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def purge(self, ctx, arg1):
        """Purges a number of messages"""
        sys.stdout.write(f'{ctx.message.author} ran command "purge"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "purge"')
        async for history in ctx.message.channel.history(limit=int(arg1)):
            msg = await ctx.message.channel.fetch_message(history.id)
            await msg.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        logging.error('Command "purge" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='chat')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def chat(self, ctx, arg1):
        """Work in progress"""
        sys.stdout.write(f'{ctx.message.author} ran command "chat"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "chat"')
        ctx.message.content = ctx.message.content[len('|chat'):]
        cb = cleverbotfree.cbfree.Cleverbot()
        response = cb.single_exchange(ctx.message.content)
        await ctx.message.channel.send(response)
        cb.browser.close()

    @chat.error
    async def chat_error(self, ctx, error):
        logging.error('Command "chat" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


# END MISC COMMANDS

def setup(bot):
    bot.add_cog(MiscCog(bot))
