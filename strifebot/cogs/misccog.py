from discord.ext import commands
import sys
import logging
import discord
import random
import json



f = open("nan0.playlist", "r")
nan0 = []
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
    elif "raid_roleid" in line:
        raid_roleid = int(line.split("=")[-1:][0].strip())

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

    elif "logs_channelid" in line:
        logs_channelid = int(line.split("=")[-1:][0].strip())


async def getRulesEmbed():
    embedtext = '''
    Rule 1
Follow the Discord ToS and Community Guidelines
The guidelines specifically mention harassment, threats of violence, attacks based on race or sex, etc. Follow these to avoid endangering the server.
https://discord.com/terms
https://discord.com/guidelines


Rule 2
Keep content and discussion in their appropriate channels.
Channel names indicate what the channels are meant for, and channel descriptions elaborate on what specifically belongs in each channel.
Rule 3
Don't be excessively toxic towards members.
Inflammatory and toxic behavior towards other members will be moderated. Insults aren't necessarily moderated, but severe ones or continued mild toxicity over a prolonged period of time will be addressed. Examples of severe insults include attacks based on personal traits, unjustified accusations meant to defame, etc.


Rule 4
Don't be disruptive towards serious conversations.
Trolling, shitposting, LARPing and spamming that stifles, interrupts or prevents serious discussion will be moderated. Serious conversation refers to conversation that does not fall into any of the categories mentioned above.


Rule 5
Argue honestly, genuinely and charitably for claims you make and when objecting to others.
A refusal to defend claims put forth, evading objections, soapboxing

Do not simply use the server as a platform to preach your beliefs without any intent to engage in honest and critical discussion of them. Represent your beliefs honestly and engage in debates genuinely. Soapboxing, repeating beliefs you refuse to defend, and evasive behavior will be moderated.
Rule 6
Cases that fall just outside of the other rules can also be moderated if they are deemed undesirable by staff.
Some behaviours can be deemed unacceptable by staff even if the rules don't explicitly mention them. This is especially common if the behaviours come close to those condemned by the rules or are subject to interpretation. Whether the member is intentionally skirting around the rules to toe the line of what is acceptable or is doing it completely accidentally, staff will inform the member that that their behaviour is undesirable when it occurs and attempt to reach an agreement. Continuation of the behaviour after having been informed of the staff team's stance on it will lead to moderation.


Rule 7
Complaints and contentions regarding moderation belong in one of the two complaints channels.
The exception to this is when a staff member is ok with discussing the moderation in a normal channel. In all other cases, complaints about moderation should happen in the dedicated channels to avoid disrupting the main channels, as the purpose of moderation is to curb disruptive behaviour.
'''
    embed=discord.Embed(title="***Strife***", description=embedtext, colour=0x7eff00)

    return embed

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("member joined")
        print(raid_roleid)
        with open("state.json", "r") as state_file:
            state = json.load(state_file)
        try:
            if state['raidmode']:
                print("raid mode enabled")
                raid_role = member.guild.get_role(raid_roleid)
                print(raid_role)
                await member.add_roles(raid_role)
            #elif not state['raidmode']:
                #rules = self.bot.get_channel(rules_channelid)
                #roles = self.bot.get_channel(roles_channelid)
                #main = self.bot.get_channel(general_channelid)
                #if main is not None and rules is not None and roles is not None and member.mention is not None:
                    #await main.send("Hello {}, welcome to Strife. Please read {} and {} text channels before participating in the server (or else)!".format(member.mention, rules.mention, roles.mention))
        except:
             print("On_join error")

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
        await ctx.send("```" + open("./../logs/strife.log", "r").read()[-1994:] + "```")

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
        await ctx.send("```" + open("./../logs/strife_error.log", "r").read()[-1994:] + "```")

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

    #@commands.command(pass_context=True, name='ndjt')
    #@commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    #async def ndjt(self, ctx):
        #"""posts some of nan0scho1ar's music"""
        #sys.stdout.write(f'{ctx.message.author} ran command "ndjt"\n')
        #sys.stdout.flush()
        #logging.info(f'{ctx.message.author} ran command "ndjt"')
        #count = int(ctx.message.content[len('|ndjt '):])
        #bump_channel = self.bot.get_channel(bump_channelid)
        #for i in range(0,count):
            #song = random.choice(nan0)
            #await bump_channel.send(song)
#
    #@ndjt.error
    #async def ndjt_error(self, ctx, error):
        #logging.error('Command "ndjt" failed due to the following error:')
        #logging.error(error)
        #await ctx.send('Error processing that request')

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
            em = await getRulesEmbed()
            await member.send("", embed=em)
        await ctx.message.delete()

    @rules.error
    async def rules_error(self, ctx, error):
        logging.error('Command "rules" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________
    @commands.command(pass_context=True, name='rule')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def rule(self, ctx, num):
        """Tells the mentioned member to read a rule"""
        sys.stdout.write(f'{ctx.message.author} ran command "rule"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "rule"')
        rules = self.bot.get_channel(rules_channelid)
        found = False
        num = int(num)
        async for history in rules.history(limit=100):
            msg = await rules.fetch_message(history.id)
            rule = msg.content
            if "Rule {}".format(num) in rule:
                index1 = rule.find("Rule {}".format(num))
                index2 = rule.find("Rule {}".format(num + 1))
                if index2 > index1:
                    rule = rule[index1-2:index2 - 4]
                else:
                    rule = rule[index1-2:]
                await ctx.message.channel.send(rule)
                found = True
        if not found:
            if num == 34:
                await ctx.message.channel.send("Nice try...")
            else:
                await ctx.message.channel.send("I can't find that rule")

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

    @commands.command(pass_context=True, name='mock')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def mock(self, ctx):
        """Creates an embed and sets the title"""
        sys.stdout.write(f'{ctx.message.author} ran command "mock"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "mock"')
        if ctx.message.reference is not None:
            print(ctx.message.reference)
            message_id = ctx.message.reference.message_id
            print(message_id)
            msg = str((await ctx.fetch_message(message_id)).content)
        else:
            msg = ctx.message.content[len('|mock'):]
        for i in range(0, len(msg) - 1):
            if i > 1 and msg[i-2:i].upper() == msg[i-2:i]:
                msg = msg[:i] + msg[i].lower() + msg[i+1:]
            elif i > 1 and msg[i-2:i].lower() == msg[i-2:i]:
                msg = msg[:i] + msg[i].upper() + msg[i+1:]
            else:
                choices = [msg[i].lower(), msg[i].upper()]
                msg = msg[:i] + random.choice(choices) + msg[i+1:]
        em = discord.Embed(title=msg, description="", colour=0x36393F)
        await ctx.message.delete()
        await ctx.message.channel.send("", embed=em)

    @mock.error
    async def embed_error(self, ctx, error):
        logging.error('Command "mock" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='bold')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def bold(self, ctx):
        """Creates an embed and sets the title"""
        sys.stdout.write(f'{ctx.message.author} ran command "bold"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "bold"')
        await ctx.message.delete()
        ctx.message.content = ctx.message.content[len('|bold'):]
        em = discord.Embed(title=ctx.message.content.upper(), description="", colour=0x36393F)
        await ctx.message.channel.send("", embed=em)

    @bold.error
    async def embed_error(self, ctx, error):
        logging.error('Command "bold" failed due to the following error:')
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
    async def purge(self, ctx, num):
        """Purges a number of messages"""
        sys.stdout.write(f'{ctx.message.author} ran command "purge"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "purge"')
        async for history in ctx.message.channel.history(limit=int(num)+1):
            msg = await ctx.message.channel.fetch_message(history.id)
            await msg.delete()
        em = discord.Embed(title="", description=f'Purged {num} messages.', colour=0x36393F)
        em.set_author(name=ctx.message.author.display_name, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await ctx.message.channel.send("", embed=em)

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
