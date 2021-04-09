from discord.ext import commands
import sys
import logging

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

class DebateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# START DEBATE COMMANDS

    #Give speaking role
    @commands.command(pass_context=True, name='debate  add', aliases=['dba'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def debateadd(self, ctx):
        """Add a user to the debate"""
        sys.stdout.write(f'{ctx.message.author} ran command "debateadd"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "debateadd"')
        for member in ctx.message.mentions:
            #await client.add_roles(member, gladiator_role) TODO
            await ctx.send(ctx.message.channel, "{} can now speak".format(member.mention))

    @debateadd.error
    async def debateadd_error(self, ctx, error):
        logging.error('Command "debateadd" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    #Remove speaking role
    @commands.command(pass_context=True, name='debate  remove', aliases=['dbr'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def debateremove(self, ctx):
        """Remove a user from the debate"""
        sys.stdout.write(f'{ctx.message.author} ran command "debateremove"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "debateremove"')
        for member in ctx.message.mentions:
            #await client.remove_roles(member, gladiator_role) TODO
            await ctx.send(ctx.message.channel, "{} can no longer speak".format(member.mention))

    @debateremove.error
    async def debateremove_error(self, ctx, error):
        logging.error('Command "debateremove" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #End the debate
    @commands.command(pass_context=True, name='debate  end', aliases=['dbe'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def debateend(self, ctx):
        """End a debate"""
        sys.stdout.write(f'{ctx.message.author} ran command "debateend"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "debateend"')
        if ctx.message.content.lower().strip().startswith("debate end "):
            terms = ctx.message.content[len("debate end "):].strip()
        else:
            terms = ctx.message.content[len("dbe "):].strip()
        authorChannel = ctx.message.author.voice_channel
        debateChannel = discord.utils.get(ctx.message.server.channels, name=terms, type=discord.ChannelType.voice)
        #do it 6 times because bad internet
        for i in range(0,6):
            members = authorChannel.voice_members
#            for member in members:
 #               if not member.bot:
                    #await client.move_member(member, debateChannel) TODO
                    #await client.remove_roles(member, gladiator_role) TODO
        await ctx.send(ctx.message.channel, "Finishing debate in {}".format(authorChannel.name))

    @debateend.error
    async def debateend_error(self, ctx, error):
        logging.error('Command "debateend" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #Start a debate
    @commands.command(pass_context=True, name='debate', aliases=['db'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def debate(self, ctx):
        """Start a debate"""
        sys.stdout.write(f'{ctx.message.author} ran command "debate"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "debate"')
        if ctx.message.content.lower().strip().startswith("debate "):
            terms = ctx.message.content[len("debate "):].strip()
        else:
            terms = ctx.message.content[len("db "):].strip()
        t = str(terms).split(',')
        dbChannel = t[0]
        topic = t[1]
        authorChannel = ctx.message.author.voice_channel
        debateChannel = discord.utils.get(ctx.message.server.channels, name=dbChannel, type=discord.ChannelType.voice)
        #do it 6 times because bad internet
        for i in range(0,6):
            members = authorChannel.voice_members
 #           for member in members:
                #await client.move_member(member, debateChannel) TODO
  #          for member in ctx.message.mentions:
                #await client.add_roles(member, gladiator_role) TODO
        await ctx.send(ctx.message.channel, "Starting debate")
        participants = ""
        for member in ctx.message.mentions:
            participants += member.mention + ", "
        await ctx.send(client.get_channel(general_channelid), ":green_apple: {} are debating about {} in {} join Now! :green_apple:".format(participants, topic, debateChannel.mention))

    @debate.error
    async def debate_error(self, ctx, error):
        logging.error('Command "debate" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

# END DEBATE COMMANDS
def setup(bot):
    bot.add_cog(DebateCog(bot))
