import requests
import sys
import logging
import xmltodict
import random
import datetime
import json
from discord.ext import commands

NOMINATIONS_URL = 'http://localhost:5000/nominations'
ARCHIVED_NOMINATIONS_URL = 'http://localhost:5000/archivednominations'
VOTES_URL = 'http://localhost:5000/votes'
ARCHIVED_VOTES_URL = 'http://localhost:5000/archivedvotes'

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

    elif "general_channelid" in line:
        general_channelid = int(line.split("=")[-1:][0].strip())
# START NOMINATIONS FUNCTIONS


#returns a codeblock containing all archived or suggested nominations
async def getNominations(archived):
    if archived:
        r = requests.get(ARCHIVED_NOMINATIONS_URL)
    else:
        r = requests.get(NOMINATIONS_URL)
    nominations = []
    chunk = "```"
    for nomination in r.json():
        if (len(chunk) > 1800):
            chunk += "```"
            nominations.append(chunk)
            chunk = "```"
        chunk += "{}: {} | {}\n".format(nomination['id'], nomination['NOMINATION'], nomination['WEIGHT'])
    chunk += "```"
    nominations.append(chunk)
    if nominations[0] == "``````":
        if archived:
            nominations = "There are currently no archived nominations"
        else:
            nominations = "There are currently no suggested nominations"
    return nominations



#returns a codeblock containing a specific archived or suggested nomination
async def getNomination(id, archived):
    if archived:
        r = requests.get(ARCHIVED_NOMINATIONS_URL + '/' + id)
    else:
        r = requests.get(NOMINATIONS_URL + '/' + id)
    nominations = "```"
    for nomination in r.json():
        nominations += "{}: {} | {}\n".format(nomination['id'], nomination['NOMINATION'], nomination['WEIGHT'])
    nominations += "```"
    if nominations == "``````":
        if archived:
            nominations = "Cannot find archived nomination with id " + id
        else:
            nominations = "Cannot find suggested nomination with id " + id
    return nominations



#deletes a specific archived or suggested nomination
async def deleteNomination(id, archived):
    if archived:
        r = requests.delete(ARCHIVED_NOMINATIONS_URL + '/' + id)
    else:
        r = requests.delete(URL + '/' + id)
    return



#deletes a all archived or suggested nominations
async def deleteAllNominations(archived):
    if archived:
        r = requests.delete(ARCHIVED_NOMINATIONS_URL)
    else:
        r = requests.delete(NOMINATIONS_URL)
    return



#returns a random aproved nomination
async def getRandomNomination():
    r = requests.get(NOMINATIONS_URL).json()
    nomination = r[random.randint(0, len(r))]
    return "***Nomination:***  {}".format(nomination['NOMINATION'])



#adds a new archived, or suggested nomination
async def addNomination(nomination, weight, archived):
    data = {'NOMINATION': nomination, 'WEIGHT': weight}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
        requests.post(ARCHIVED_NOMINATIONS_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(NOMINATIONS_URL, data=json.dumps(data), headers=headers)
    return



#edits an archived or suggested nomination
#data format should be "id newNominationText, newDisciplineText"
async def editNomination(din, archived):
    nominationId = din.split(' ', 1)[0]
    nomination = din.split(' ', 1)[1]
    data = {'NOMINATION': nomination, 'WEIGHT': 1}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
                             #url + nominationID
        requests.put(ARCHIVED_NOMINATIONS_URL + '/' + nominationId, data=json.dumps(data), headers=headers)
    else:
        requests.put(NOMINATIONS_URL + '/' + nominationId, data=json.dumps(data), headers=headers)



#archive suggested nomination by nominationID
async def archiveNomination(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(NOMINATIONS_URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'NOMINATION': t['NOMINATION'], 'WEIGHT': t['WEIGHT']}
    requests.post(ARCHIVED_NOMINATIONS_URL, data=json.dumps(data), headers=headers)
    requests.delete(NOMINATIONS_URL + '/' + id)


async def getNominationCount(archived):
    if archived:
        r = requests.get(ARCHIVED_NOMINATIONS_URL)
    else:
        r = requests.get(NOMINATIONS_URL)
    weights = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    result = {}
    for vote in r.json():
        result[vote['NOMINATION']] = {}
        for weight in weights:
            result[vote['NOMINATION']][weight] = 0
    for vote in r.json():
        result[vote['NOMINATION']][vote['WEIGHT']] += 1
    return result


# END NOMINATIONS FUNCTIONS


#returns a codeblock containing all archived or suggested votes
async def getVotes(archived):
    if archived:
        r = requests.get(ARCHIVED_VOTES_URL)
    else:
        r = requests.get(VOTES_URL)
    votes = []
    chunk = "```"
    for vote in r.json():
        if (len(chunk) > 1800):
            chunk += "```"
            votes.append(chunk)
            chunk = "```"
        chunk += "{}: {} | {}\n".format(vote['id'], vote['VOTE'], vote['DATELODGED'])
    chunk += "```"
    votes.append(chunk)
    if votes[0] == "``````":
        if archived:
            votes = "There are currently no archived votes"
        else:
            votes = "There are currently no votes"
    return votes

async def hasVoted(voterId):
    r = requests.get(VOTES_URL)
    for vote in r.json():
        if str(vote['VOTE']) == str(voterId):
            return True
    return False

#returns a codeblock containing a specific archived or suggested vote
async def getVote(id, archived):
    if archived:
        r = requests.get(ARCHIVED_VOTES_URL + '/' + id)
    else:
        r = requests.get(VOTES_URL + '/' + id)
    votes = "```"
    for vote in r.json():
        votes += "{}: {} | {}\n".format(vote['id'], vote['VOTE'], vote['DATELODGED'])
    votes += "```"
    if votes == "``````":
        if archived:
            votes = "Cannot find archived vote with id " + id
        else:
            votes = "Cannot find suggested vote with id " + id
    return votes



#deletes a specific archived or suggested vote
async def deleteVote(id, archived):
    if archived:
        r = requests.delete(ARCHIVED_VOTES_URL + '/' + id)
    else:
        r = requests.delete(VOTES_URL + '/' + id)
    return



#deletes a all archived or suggested votes
async def deleteAllVotes(archived):
    if archived:
        r = requests.delete(ARCHIVED_VOTES_URL)
    else:
        r = requests.delete(VOTES_URL)
    return



#returns a random aproved vote
async def getRandomVote():
    r = requests.get(VOTES_URL).json()
    vote = r[random.randint(0, len(r))]
    return "***Vote:***  {}".format(vote['VOTE'])



#adds a new archived, or suggested vote
async def addVote(vote, archived):
    data = {'VOTE': vote, 'DATELODGED': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
        requests.post(ARCHIVED_VOTES_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(VOTES_URL, data=json.dumps(data), headers=headers)
    return



#edits an archived or suggested vote
#data format should be "id newVoteText, newDisciplineText"
async def editVote(din, archived):
    voteId = din.split(' ', 1)[0]
    vote = din.split(' ', 1)[1]
    data = {'VOTE': vote, 'DATELODGED': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
                             #url + voteID
        requests.put(ARCHIVED_VOTES_URL + '/' + voteId, data=json.dumps(data), headers=headers)
    else:
        requests.put(VOTES_URL + '/' + voteId, data=json.dumps(data), headers=headers)



#archive suggested vote by voteID
async def archiveVote(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'VOTE': t['VOTE'], 'DATELODGED': t['DATELODGED']}
    requests.post(ARCHIVED_VOTES_URL, data=json.dumps(data), headers=headers)
    requests.delete(VOTES_URL + '/' + id)


# END VOTES FUNCTIONS



class NominationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='randomnomination', help='Randomly selects an archived nomination.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomnomination(self, ctx):
        """Returns a random suggested nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomnomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomnomination"')
        await ctx.send(await getRandomNomination())

    @randomnomination.error
    async def randomnomination_error(self, ctx, error):
        logging.error('Command "randomnomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivednominations')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archivednominations(self, ctx):
        """Returns all archived nominations"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivednominations"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivednominations"')
        nominations = await getNominations(True)
        for nomination in nominations:
            if nomination=='T':
                await ctx.send('No Archived nominations')
                break
            else:
                await ctx.send(nomination)

    @archivednominations.error
    async def archivednominations_error(self, ctx, error):
        logging.error('Command "archivednominations" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='editarchivednomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def editarchivednomination(self, ctx):
        """Edit an archived nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "editarchivednomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editarchivednomination"')
        await editNomination(ctx.message.content[len('editarchivednomination '):].strip(), True)
        await ctx.send("Edited archived nomination")

    @editarchivednomination.error
    async def editarchivednomination_error(self, ctx, error):
        logging.error('Command "editarchivednomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='editnomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def editnomination(self, ctx):
        """edit a nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "editnomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editnomination"')
        await editNomination(ctx.message.content[len('editnomination '):].strip(), False)
        await ctx.send("Edited nomination")

    @editnomination.error
    async def editnomination_error(self, ctx, error):
        logging.error('Command "editnomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='nominations')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def nominations(self, ctx):
        """return all nominations"""
        sys.stdout.write(f'{ctx.message.author} ran command "nominations"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "nominations"')
        nominations = await getNominations(False)
        for nomination in nominations:
            if nomination=='T':
                await ctx.send('No nominations')
                break
            else:
                await ctx.send(nomination)

    @nominations.error
    async def nominations_error(self, ctx, error):
        logging.error('Command "nominations" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='nomination')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def nomination(self, ctx):
        """Return a specific nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "nomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "nomination"')
        nomination = ctx.message.content[len('nomination '):].strip()
        await ctx.send(await getNomination(nomination, False))

    @nomination.error
    async def nomination_error(self, ctx, error):
        logging.error('Command "nomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletenomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletenomination(self, ctx):
        """Delete a nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletenomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletenomination"')
        nomination = ctx.message.content[len('deletenomination '):]
        nums = nomination.split(' ')
        for num in nums:
            await deleteNomination(num, False)
            await ctx.send("Deleted nomination")

    @deletenomination.error
    async def deletenomination_error(self, ctx, error):
        logging.error('Command "deletenomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletearchivednomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletearchivednomination(self, ctx):
        """Delete an archived nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchivednomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchivednomination"')
        nomination = ctx.message.content[len('deletearchivednomination '):].strip()
        nums = nomination.split(' ')
        for num in nums:
            await deleteNomination(num, True)
            await ctx.send("Deleted archived nomination")

    @deletearchivednomination.error
    async def deletearchivednomination_error(self, ctx, error):
        logging.error('Command "deletearchivednomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    #TODO finish implementing lock
    @commands.command(pass_context=True, name='deleteallarchivednominationscommit')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivednominationscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivednominationscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivednominationscommit"')
        await deleteAllNominations(True)
        await ctx.send("Deleted all archived nominations")

    @deleteallarchivednominationscommit.error
    async def deleteallarchivednominationscommit_error(self, ctx, error):
        logging.error('Command "deleteallarchivednominationscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallarchivednominations')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivednominations(self, ctx):
        """Delete all archived nominations"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivednominations"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivednominations"')
        await ctx.send("Are you sure you want to delete all archived nominations?\nType ```|deleteallarchivednominationscommit``` to continue")

    @deleteallarchivednominations.error
    async def deleteallarchivednominations_error(self, ctx, error):
        logging.error('Command "deleteallarchivednominations" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallnominationscommit')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallnominationscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallnominationscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallnominationscommit"')
        await deleteAllNominations(False)
        await ctx.send("Deleted all nominations")

    @deleteallnominationscommit.error
    async def deleteallnominationscommit_error(self, ctx, error):
        logging.error('Command "deleteallnominationscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallnominations')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallnominations(self, ctx):
        """Delete all nominations"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallnominations"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallnominations"')
        await ctx.send("Are you sure you want to delete all nominations?\nType ```|deleteallnominationscommit``` to continue")

    @deleteallnominations.error
    async def deleteallnominations_error(self, ctx, error):
        logging.error('Command "deleteallnominations" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newarchivednomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def newarchivednomination(self, ctx):
        """Create a new archived nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "newarchivednomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newarchivednomination"')
        nomination = ctx.message.content[len('|newarchivednomination '):].strip()
        await addNomination(nomination, 1, True)
        await ctx.send("Added nomination {}".format(nomination))

    @newarchivednomination.error
    async def newarchivednomination_error(self, ctx, error):
        logging.error('Command "newarchivednomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivenomination')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def archivenomination(self, ctx):
        """Archive a nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivenomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivenomination"')
        nomination = ctx.message.content[len('archivenomination '):].strip()
        await archiveNomination(nomination)
        await ctx.send("Archived nomination " + nomination)

    @archivenomination.error
    async def archivenomination_error(self, ctx, error):
        logging.error('Command "archivednomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='nomination')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def nomination(self, ctx):
        """Return a specific nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "nomination"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "nomination"')
        nomination = ctx.message.content[len('nomination '):].strip()
        if len(nomination) == 0:
            await ctx.send("?nomination id               ?t id           Returns a specific nomination.")
        await ctx.send(await getNomination(nomination, True))

    @nomination.error
    async def nomination_error(self, ctx, error):
        logging.error('Command "nomination" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='randomvote', help='Randomly selects an archived vote.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomvote(self, ctx):
        """Returns a random suggested vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomvote"')
        await ctx.send(await getRandomVote())

    @randomvote.error
    async def randomvote_error(self, ctx, error):
        logging.error('Command "randomvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivedvotes')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archivedvotes(self, ctx):
        """Returns all archived votes"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivedvotes"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivedvotes"')
        votes = await getVotes(True)
        for vote in votes:
            if vote=='T':
                await ctx.send('No Archived votes')
                break
            else:
                await ctx.send(vote)

    @archivedvotes.error
    async def archivedvotes_error(self, ctx, error):
        logging.error('Command "archivedvotes" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='editarchivedvote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def editarchivedvote(self, ctx):
        """Edit an archived vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "editarchivedvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editarchivedvote"')
        await editVote(ctx.message.content[len('editarchivedvote '):].strip(), True)
        await ctx.send("Edited archived vote")

    @editarchivedvote.error
    async def editarchivedvote_error(self, ctx, error):
        logging.error('Command "editarchivedvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



    @commands.command(pass_context=True, name='editvote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def editvote(self, ctx):
        """edit a vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "editvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editvote"')
        await editVote(ctx.message.content[len('editvote '):].strip(), False)
        await ctx.send("Edited vote")

    @editvote.error
    async def editvote_error(self, ctx, error):
        logging.error('Command "editvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='votes')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def votes(self, ctx):
        """return all votes"""
        sys.stdout.write(f'{ctx.message.author} ran command "votes"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "votes"')
        votes = await getVotes(False)
        for vote in votes:
            if vote=='T':
                await ctx.send('No votes')
                break
            else:
                await ctx.send(vote)

    @votes.error
    async def votes_error(self, ctx, error):
        logging.error('Command "votes" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='vote')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def vote(self, ctx):
        """Adds a new vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "vote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "vote"')
        if str(await getVotes(False)).split().count(str(ctx.message.author.id)) > 0:
            await ctx.message.channel.send("You have already voted")
            return
        nominees = ["a15eteRnal15", "Terrance", "Longtail", "dionaea", "V i m s u", "Doc", "Certified Argentine Nationalist", "Brian", "Jun", "cam", "Precoital Torture of the Spirit", "Midnight", "Zark", "tims head dweller"]
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        await ctx.message.author.send("Ballot")
        for user in nominees:
            msg = await ctx.message.author.send(user)
            for react in reactions:
                await msg.add_reaction(react)
            msg = await msg.channel.fetch_message(msg.id)
            #Validate all reacts were added correctly
            hasAllReacts = False
            while not hasAllReacts:
                hasAllReacts = True
                emoji = []
                for r in msg.reactions:
                    emoji.append(r.emoji)
                for react in emoji:
                    if not react in reactions:
                        hasAllReacts = False
                        await msg.add_reaction(react)
        await ctx.message.author.send("End Ballot")
        await ctx.message.author.send("Type '|submit' to lodge your vote")
        
    @vote.error
    async def vote_error(self, ctx, error):
        logging.error('Command "vote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')


    #__________________________________________________


    @commands.command(pass_context=True, name='submit')
    #@commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def submit(self, ctx):
        """Submits a vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "submit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "submit"')
        if str(await getVotes(False)).split().count(str(ctx.message.author.id)) > 0:
            await ctx.message.channel.send("You have already voted")
            return
        votes = {}
        invalid = False
        checkingBallot = False
        async for msg in ctx.message.channel.history(limit=200):
            if msg.content == "End Ballot":
                checkingBallot = True
                continue
            if checkingBallot and msg.content == "Ballot":
               break
            if checkingBallot:
                votes[msg.content] = ""
                for react in msg.reactions:
                    if react.count > 1:
                        if votes[msg.content] != "":
                            invalid = True
                            break
                        else:
                            votes[msg.content] = react.emoji
                if invalid:
                    break
        if invalid:
            result = await msg.channel.send("Invalid vote. Voted for the same person more than once")
        else:
            vals = list(filter(None, votes.values()))
            if len(set(vals))!= len(vals): 
                result = await msg.channel.send("Invalid vote. Number occured more than once")
            else:
                r = []
                for k, v in votes.items():
                    if v != "":
                        await addNomination(k, v, False)
                    r.append(k + " " + v)
                await addVote(ctx.message.author.id, False)
                await msg.channel.send("\n".join(r[::-1]))
                checkingBallot = False
                async for msg in ctx.message.channel.history(limit=200):
                    if msg.content == "Type '|submit' to lodge your vote":
                        print("Beginning Delete")
                        checkingBallot = True
                        await msg.delete()
                        continue
                    if msg.content == "Ballot":
                        await msg.delete()
                        break
                    if checkingBallot:
                        await msg.delete()

    @submit.error
    async def submit_error(self, ctx, error):
        logging.error('Command "submit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')


    #__________________________________________________


    @commands.command(pass_context=True, name='results')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, cbbb)
    async def results(self, ctx):
        """Return results"""
        sys.stdout.write(f'{ctx.message.author} ran command "results"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "results"')
        result = await getNominationCount(False)
        r = []
        for candidate, votes in result.items():
            r.append("> " + str(votes) + " " + str(candidate))
        for res in r[::-1]:
            await ctx.send(res)

    @results.error
    async def getvote_error(self, ctx, error):
        logging.error('Command "results" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')


    #__________________________________________________


    @commands.command(pass_context=True, name='getvote')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def getvote(self, ctx):
        """Return a specific vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "getvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "getvote"')
        vote = ctx.message.content[len('vote '):].strip()
        await ctx.send(await getVote(vote, False))

    @getvote.error
    async def getvote_error(self, ctx, error):
        logging.error('Command "getvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletevote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletevote(self, ctx):
        """Delete a vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletevote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletevote"')
        vote = ctx.message.content[len('deletevote '):]
        nums = vote.split(' ')
        for num in nums:
            await deleteVote(num, False)
            await ctx.send("Deleted vote")

    @deletevote.error
    async def deletevote_error(self, ctx, error):
        logging.error('Command "deletevote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletearchivedvote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletearchivedvote(self, ctx):
        """Delete an archived vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchivedvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchivedvote"')
        vote = ctx.message.content[len('deletearchivedvote '):].strip()
        nums = vote.split(' ')
        for num in nums:
            await deleteVote(num, True)
            await ctx.send("Deleted archived vote")

    @deletearchivedvote.error
    async def deletearchivedvote_error(self, ctx, error):
        logging.error('Command "deletearchivedvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    #TODO finish implementing lock
    @commands.command(pass_context=True, name='deleteallarchivedvotescommit')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedvotescommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedvotescommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedvotescommit"')
        await deleteAllVotes(True)
        await ctx.send("Deleted all archived votes")

    @deleteallarchivedvotescommit.error
    async def deleteallarchivedvotescommit_error(self, ctx, error):
        logging.error('Command "deleteallarchivedvotescommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallarchivedvotes')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedvotes(self, ctx):
        """Delete all archived votes"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedvotes"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedvotes"')
        await ctx.send("Are you sure you want to delete all archived votes?\nType ```|deleteallarchivedvotescommit``` to continue")

    @deleteallarchivedvotes.error
    async def deleteallarchivedvotes_error(self, ctx, error):
        logging.error('Command "deleteallarchivedvotes" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallvotescommit')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallvotescommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallvotescommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallvotescommit"')
        await deleteAllVotes(False)
        await ctx.send("Deleted all votes")

    @deleteallvotescommit.error
    async def deleteallvotescommit_error(self, ctx, error):
        logging.error('Command "deleteallvotescommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallvotes')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallvotes(self, ctx):
        """Delete all votes"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallvotes"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallvotes"')
        await ctx.send("Are you sure you want to delete all votes?\nType ```|deleteallvotescommit``` to continue")

    @deleteallvotes.error
    async def deleteallvotes_error(self, ctx, error):
        logging.error('Command "deleteallvotes" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newarchivedvote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def newarchivedvote(self, ctx):
        """Create a new archived vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "newarchivedvote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newarchivedvote"')
        vote = ctx.message.content[len('|newarchivedvote '):].strip()
        await addVote(vote, True)
        await ctx.send("Added vote {}".format(vote))

    @newarchivedvote.error
    async def newarchivedvote_error(self, ctx, error):
        logging.error('Command "newarchivedvote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivevote')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def archivevote(self, ctx):
        """Archive a vote"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivevote"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivevote"')
        vote = ctx.message.content[len('archivevote '):].strip()
        await archiveVote(vote)
        await ctx.send("Archived vote " + vote)

    @archivevote.error
    async def archivevote_error(self, ctx, error):
        logging.error('Command "archivevote" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


#    @commands.command(pass_context=True, name='nominate')
#    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
#    async def nominate(self, ctx):
#        """Create a new vote"""
#        sys.stdout.write(f'{ctx.message.author} ran command "nominate"\n')
#        sys.stdout.flush()
#        logging.info(f'{ctx.message.author} ran command "nominate"')
#        vote = ctx.message.content[len('nominate '):].strip()
#        await addVote(vote, False)
#        await ctx.send("Added vote {}".format(vote))
#
#    @nominate.error
#    async def nominate_error(self, ctx, error):
#        logging.error('Command "nominate" failed due to the following error:')
#        logging.error(error)
#        await ctx.send('Error processing that request')

    @commands.command(pass_context=True, name='nominate')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def nominate(self, ctx):
        """Create a new nomination"""
        sys.stdout.write(f'{ctx.message.author} ran command "nominate"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "nominate"')
        if await hasVoted(ctx.message.author.id):
            await ctx.send("You have already voted")
        else:
            await addNomination(ctx.message.mentions[0].id, 1, False)
            await addVote(ctx.message.author.id, False)
            await ctx.message.delete()
            await ctx.send("Added nomination {}".format(ctx.message.mentions[0]))

    @nominate.error
    async def nominate_error(self, ctx, error):
        logging.error('Command "nominate" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



def setup(bot):
    bot.add_cog(NominationCog(bot))
