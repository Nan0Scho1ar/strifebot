from discord.ext import commands
import logging
import discord
import sys
import asyncio

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
    elif "peasant_roleid" in line:
        peasant_roleid = int(line.split("=")[-1:][0].strip())
    elif "reading_roleid" in line:
        reading_roleid = int(line.split("=")[-1:][0].strip())
    elif "ghost_roleid" in line:
        ghost_roleid = int(line.split("=")[-1:][0].strip())

    elif "cbbb" in line:
        cbbb = int(line.split("=")[-1:][0].strip())

    elif "logs_channelid" in line:
        logs_channelid = int(line.split("=")[-1:][0].strip())

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# START ADMINISTRATION COMMANDS

    @commands.command(pass_context=True, name='say', aliases=['echo'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def say(self, ctx):
        """echos the user input"""
        sys.stdout.write(f'{ctx.message.author} ran command "say"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "say"')
        msg = ctx.message.content[len('say '):]
        await ctx.send(msg)
        await ctx.message.delete()

    @say.error
    async def say_error(self, ctx, error):
        logging.error('Command "say" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='boot')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def boot(self, ctx):
        """Boot a user from the VC"""
        sys.stdout.write(f'{ctx.message.author} ran command "boot"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "boot"')
        await ctx.message.guild.create_voice_channel("Temp Mute")
        channel = discord.utils.get(ctx.message.guild.voice_channels, name='Temp Mute')
        for member in ctx.message.mentions:
            await member.move_to(channel)
        await channel.delete()
        await ctx.message.channel.send("Booted {}".format(member))
        await ctx.message.delete()

    @boot.error
    async def boot_error(self, ctx, error):
        logging.error('Command "boot" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='warn')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def warn(self, ctx, user):
        """warn a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "warn"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "warn"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        msg = ctx.message.content.split(" ", 2)
        if len(msg) == 2:
            reason = "No reason provided"
        else:
            reason = msg[2].strip()
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        await member.send("Your conduct has been flagged by server staff for the following reasons:{}\n\nBe aware penalties apply for repeated transgressions!".format(reason))
        em = discord.Embed(title="Warned {}".format(member), description="Reason: {}".format(reason), colour=0xF2A013)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Warned {}".format(member))
        #await ctx.message.delete()

    @warn.error
    async def warn_error(self, ctx, error):
        logging.error('Command "warn" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='mute')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def mute(self, ctx, user, duration="1h"):
        """Mute a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "mute"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "mute"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        commoners_role = ctx.guild.get_role(commoners_roleid)
        peasant_role = ctx.guild.get_role(peasant_roleid)
        reading_role = ctx.guild.get_role(ghost_roleid)
        ghost_role = ctx.guild.get_role(ghost_roleid)

        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]

        msg = ctx.message.content.split(" ")
        reason = ""
        if len(msg) > 3:
            reason = " ".join(msg[3:])


        if duration[-1] == 's':
            num_seconds = int(duration[:-1])
        elif duration[-1] == 'm':
            num_seconds = int(duration[:-1]) * 60
        elif duration[-1] == 'h':
            num_seconds = int(duration[:-1]) * 60 * 60
        elif duration[-1] == 'd':
            num_seconds = int(duration[:-1]) * 60 * 60 * 24
        elif duration[-1] == 'w':
            num_seconds = int(duration[:-1]) * 60 * 60 * 24 * 7
        elif duration[-1] == 'y':
            num_seconds = int(duration[:-1]) * 60 * 60 * 24 * 7 * 52
        else:
            await ctx.message.channel.send("Invalid time format")
            return;

        #Apply mute
        await member.remove_roles(commoners_role)
        await member.remove_roles(ghost_role)
        await member.remove_roles(reading_role)
        await member.add_roles(peasant_role)

        #Rejoin to apply VC mute
        if member.voice is not None:
            current_vc = member.voice.channel
            await ctx.message.guild.create_voice_channel("Temp Mute")
            temp_vc = discord.utils.get(ctx.message.guild.voice_channels, name='Temp Mute')
            await member.move_to(temp_vc)
            await asyncio.sleep(0.5)
            await member.move_to(current_vc)
            await asyncio.sleep(0.5)
            await temp_vc.delete()

        if reason == "":
            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel
            try:
                await ctx.message.channel.send("Please respond with a reason for this mute")
                response = await self.bot.wait_for('message', timeout=60.0, check=check)
                reason = response.content
            except asyncio.TimeoutError:
                await ctx.message.channel.send('No reason provided')
                reason = "No reason provided"
        await ctx.message.channel.send("muted {} for {}\nReason `{}`".format(member, duration, reason))

        em = discord.Embed(title="Muted {}".format(member), description="Duration: {}\n\nReason: {}".format(duration, reason), colour=0xF2A013)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)

        #Apply unmute
        await asyncio.sleep(num_seconds)
        await member.remove_roles(peasant_role)
        await member.remove_roles(ghost_role)
        await member.remove_roles(reading_role)
        await member.add_roles(commoners_role)
        #Rejoin to apply VC unmute
        current_vc = member.voice.channel
        if current_vc is not None:
            await ctx.message.guild.create_voice_channel("Temp Mute")
            temp_vc = discord.utils.get(ctx.message.guild.voice_channels, name='Temp Mute')
            await member.move_to(temp_vc)
            await asyncio.sleep(0.5)
            await member.move_to(current_vc)
            await asyncio.sleep(0.5)
            await temp_vc.delete()

        em = discord.Embed(title="Unmuted {}".format(member), description="Reason: Mute duration expired", colour=0x7eff00)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)


    @mute.error
    async def mute_error(self, ctx, error):
        logging.error('Command "mute" failed due to the following error: {}'.format(error))
        logging.error(error)
        print(type(error))
        print(type(discord.ext.commands.errors.MissingAnyRole))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='unmute')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def unmute(self, ctx, user, reason="No reason provided"):
        """Unmute a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "unmute"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "unmute"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        commoners_role = ctx.guild.get_role(commoners_roleid)
        peasant_role = ctx.guild.get_role(peasant_roleid)
        reading_role = ctx.guild.get_role(ghost_roleid)
        ghost_role = ctx.guild.get_role(ghost_roleid)
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        await member.remove_roles(peasant_role)
        await member.remove_roles(ghost_role)
        await member.remove_roles(reading_role)
        await member.add_roles(commoners_role)
        #Rejoin to apply VC unmute
        if member.voice is not None:
            current_vc = member.voice.channel
            await ctx.message.guild.create_voice_channel("Temp Mute")
            temp_vc = discord.utils.get(ctx.message.guild.voice_channels, name='Temp Mute')
            await member.move_to(temp_vc)
            await asyncio.sleep(0.5)
            await member.move_to(current_vc)
            await asyncio.sleep(0.5)
            await temp_vc.delete()
        em = discord.Embed(title="Unmuted {}".format(member), description="Reason: {}".format(reason), colour=0x7eff00)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Unmuted {}\nReason `{}`".format(member, reason))
        await ctx.message.delete()

    @unmute.error
    async def unmute_error(self, ctx, error):
        logging.error('Command "unmute" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='kick')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def kick(self, ctx, user):
        """Kick a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "kick"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "kick"')
        reason = ctx.message.content.split(">")[-1].strip()
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        await ctx.guild.kick(member)
        em = discord.Embed(title="Kicked {}".format(member), description="Reason: {}".format(reason), colour=0xF2A013)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Kicked {}\nReason `{}`".format(member, reason))
        await ctx.message.delete()

    @kick.error
    async def kick_error(self, ctx, error):
        logging.error('Command "kick" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='unban')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def unban(self, ctx, user, reason="No reason provided"):
        """unban a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "unban"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "unban"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        user = await ctx.bot.fetch_user(user)
        await ctx.guild.unban(user)
        em = discord.Embed(title="Unbanned {}".format(user), description="Reason: {}".format(reason), colour=0xD64848)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Unbanned {}\nReason `{}`".format(user, reason))
        await ctx.message.delete()

    @unban.error
    async def unban_error(self, ctx, error):
        logging.error('Command "unban" failed due to the following error: {}'.format(error))
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='ban')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def ban(self, ctx, user, reason="No reason provided"):
        """Ban a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "ban"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "ban"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        if user.isdigit():
            user = await ctx.bot.fetch_user(user)
        else:
            user = ctx.message.mentions[0]
        await ctx.guild.ban(user, reason=reason, delete_message_days=0)
        em = discord.Embed(title="Banned {}".format(user), description="Reason: {}".format(reason), colour=0xD64848)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(user))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Banned {}\nReason `{}`".format(user, reason))
        await ctx.message.delete()

    @ban.error
    async def ban_error(self, ctx, error):
        logging.error('Command "ban" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='purgeban')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def purgeban(self, ctx, user):
        """Ban a user an delete their messages"""
        sys.stdout.write(f'{ctx.message.author} ran command "purgeban"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "purgeban"')
        reason = ctx.message.content.split(">")[-1].strip()
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        await ctx.guild.ban(member, reason=reason, delete_message_days=7)
        em = discord.Embed(title="Banned {}".format(member), description="Reason: {}".format(reason), colour=0xD64848)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Banned {}\nReason `{}`".format(member, reason))
        await ctx.message.delete()

    @purgeban.error
    async def purgeban_error(self, ctx, error):
        logging.error('Command "purgeban" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='commend')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def commend(self, ctx, user):
        """Commend a user"""
        sys.stdout.write(f'{ctx.message.author} ran command "commend"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "commend"')
        reason = ctx.message.content.split(">")[-1].strip()
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        await member.send("Your conduct has been commended by server staff for the following reasons:{}\n\nKeep up the good work!".format(reason))
        em = discord.Embed(title="Commended {}".format(member), description="Reason: {}".format(reason), colour=0x7eff00)
        em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
        await namelessLogs.send(embed=em)
        await ctx.message.channel.send("Commended {}\nReason `{}`".format(member, reason))
        await ctx.message.delete()

    @commend.error
    async def commend_error(self, ctx, error):
        logging.error('Command "commend" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='read')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def read(self, ctx):
        """Send a user to the reading room"""
        sys.stdout.write(f'{ctx.message.author} ran command "read"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "read"')
        reason = ctx.message.content.split(">")[-1].strip()
        commoners_role = ctx.guild.get_role(commoners_roleid)
        peasant_role = ctx.guild.get_role(peasant_roleid)
        reading_role = ctx.guild.get_role(ghost_roleid)
        ghost_role = ctx.guild.get_role(ghost_roleid)

        namelessLogs = ctx.bot.get_channel(logs_channelid)
        for mention in ctx.message.mentions:
            #Do this multiple times because bad internet
            for i in range(1,5):
                await mention.add_roles(reading_role)
                await mention.remove_roles(peasant_role)
                await mention.remove_roles(ghost_role)
                await mention.remove_roles(commoners_role)
            em = discord.Embed(title="Sent {} to reading".format(mention), description="Reason: {}".format(reason), colour=0xD64848)
            em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(mention))
            em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
            await namelessLogs.send(embed=em)
        await ctx.message.delete()

    @read.error
    async def read_error(self, ctx, error):
        logging.error('Command "read" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='unread')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def unread(self, ctx):
        """Remove user from reading room"""
        sys.stdout.write(f'{ctx.message.author} ran command "unread"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "unread"')
        reason = ctx.message.content.split(">")[-1].strip()
        commoners_role = ctx.guild.get_role(commoners_roleid)
        peasant_role = ctx.guild.get_role(peasant_roleid)
        reading_role = ctx.guild.get_role(ghost_roleid)
        ghost_role = ctx.guild.get_role(ghost_roleid)

        namelessLogs = ctx.bot.get_channel(logs_channelid)
        for mention in ctx.message.mentions:
            #Do this multiple times because bad internet
            for i in range(1,5):
                await mention.add_roles(commoners_role)
                await mention.remove_roles(peasant_role)
                await mention.remove_roles(ghost_role)
                await mention.remove_roles(reading_role)
            em = discord.Embed(title="Removed {} from reading".format(mention), description="Reason: {}".format(reason), colour=0x7eff00)
            em.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(mention))
            em.set_author(name=ctx.message.author, icon_url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.message.author))
            await namelessLogs.send(embed=em)
        await ctx.message.delete()

    @unread.error
    async def unread_error(self, ctx, error):
        gogging.error('Command "unread" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='logs')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def logs(self, ctx, user):
        """Post logs"""
        sys.stdout.write(f'{ctx.message.author} ran command "logs"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "logs"')
        namelessLogs = ctx.bot.get_channel(logs_channelid)
        if user.isdigit():
            member = await ctx.message.guild.fetch_member(int(user))
        else:
            member = ctx.message.mentions[0]
        warnCounter = 0
        muteCounter = 0
        commendCounter = 0
        readCounter = 0
        kickCounter = 0
        banCounter = 0

        async for msg in namelessLogs.history():
            for embed in msg.embeds:
                if embed.title == "Warned {}".format(member):
                    warnCounter += 1
                elif embed.title == "Muted {}".format(member):
                    muteCounter += 1
                elif embed.title == "Commended {}".format(member):
                    commendCounter += 1
                elif embed.title == "Sent {} to reading".format(member):
                    readCounter += 1
                elif embed.title == "Kicked {}".format(member):
                    kickCounter += 1
                elif embed.title == "Banned {}".format(member):
                    banCounter += 1
        em = discord.Embed(title="Log for {}".format(member), description="Warnings: {}\nMutes: {}\nCommendations: {}\nReadings: {}\nKicks: {}\nBans: {}".format(warnCounter, muteCounter, commendCounter, readCounter, kickCounter, banCounter), colour=0x7eff00)
        em.set_thumbnail(url="httpdds://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
        await ctx.message.channel.send("```Log for {}\n\nWarnings: {}\nMutes: {}\nCommendations: {}\nReadings: {}\nKicks: {}\nBans: {}```".format(member, warnCounter, muteCounter, commendCounter, readCounter, kickCounter, banCounter))
        await ctx.message.delete()

    @logs.error
    async def logs_error(self, ctx, error):
        logging.error('Command "logs" failed due to the following error:')
        logging.error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("Insufficient permissions")
        else:
            await ctx.send('Error processing that request')

    #__________________________________________________



# END ADMINISTRATION COMMANDS
def setup(bot):
    bot.add_cog(AdminCog(bot))
