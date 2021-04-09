import requests
import sys
import logging
import xmltodict
import random
import datetime
import json
from discord.ext import commands

ARCHIVED_URL = 'http://localhost:5000/archivedcomplaints'
SUGGESTED_URL = 'http://localhost:5000/complaints'

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
# START COMPLAINTS FUNCTIONS


#returns a codeblock containing all archived or suggested complaints
async def getComplaints(archived):
    if archived:
        r = requests.get(ARCHIVED_URL)
    else:
        r = requests.get(SUGGESTED_URL)
    complaints = []
    chunk = "```"
    for complaint in r.json():
        if (len(chunk) > 1800):
            chunk += "```"
            complaints.append(chunk)
            chunk = "```"
        chunk += "{}: {} | {}\n".format(complaint['id'], complaint['COMPLAINT'], complaint['DATELODGED'])
    chunk += "```"
    complaints.append(chunk)
    if complaints[0] == "``````":
        if archived:
            complaints = "There are currently no archived complaints"
        else:
            complaints = "There are currently no suggested complaints"
    return complaints



#returns a codeblock containing a specific archived or suggested complaint
async def getComplaint(id, archived):
    if archived:
        r = requests.get(ARCHIVED_URL + '/' + id)
    else:
        r = requests.get(SUGGESTED_URL + '/' + id)
    complaints = "```"
    for complaint in r.json():
        complaints += "{}: {} | {}\n".format(complaint['id'], complaint['COMPLAINT'], complaint['DATELODGED'])
    complaints += "```"
    if complaints == "``````":
        if archived:
            complaints = "Cannot find archived complaint with id " + id
        else:
            complaints = "Cannot find suggested complaint with id " + id
    return complaints



#deletes a specific archived or suggested complaint
async def deleteComplaint(id, archived):
    if archived:
        r = requests.delete(ARCHIVED_URL + '/' + id)
    else:
        r = requests.delete(SUGGESTED_URL + '/' + id)
    return



#deletes a all archived or suggested complaints
async def deleteAllComplaints(archived):
    if archived:
        r = requests.delete(ARCHIVED_URL)
    else:
        r = requests.delete(SUGGESTED_URL)
    return



#returns a random aproved complaint
async def getRandomComplaint():
    r = requests.get(SUGGESTED_URL).json()
    complaint = r[random.randint(0, len(r))]
    return "***Complaint:***  {}".format(complaint['COMPLAINT'])



#adds a new archived, or suggested complaint
async def addComplaint(complaint, archived):
    data = {'COMPLAINT': complaint, 'DATELODGED': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
        requests.post(ARCHIVED_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(SUGGESTED_URL, data=json.dumps(data), headers=headers)
    return



#edits an archived or suggested complaint
#data format should be "id newComplaintText, newDisciplineText"
async def editComplaint(din, archived):
    complaintId = din.split(' ', 1)[0]
    complaint = din.split(' ', 1)[1]
    data = {'COMPLAINT': complaint, 'DATELODGED': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
                             #url + complaintID
        requests.put(ARCHIVED_URL + '/' + complaintId, data=json.dumps(data), headers=headers)
    else:
        requests.put(SUGGESTED_URL + '/' + complaintId, data=json.dumps(data), headers=headers)



#archive suggested complaint by complaintID
async def archiveComplaint(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(SUGGESTED_URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'COMPLAINT': t['COMPLAINT'], 'DATELODGED': t['DATELODGED']}
    requests.post(ARCHIVED_URL, data=json.dumps(data), headers=headers)
    requests.delete(SUGGESTED_URL + '/' + id)


# END COMPLAINTS FUNCTIONS



class ComplaintCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='randomcomplaint', help='Randomly selects an archived complaint.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomcomplaint(self, ctx):
        """Returns a random suggested complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomcomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomcomplaint"')
        await ctx.send(await getRandomComplaint())

    @randomcomplaint.error
    async def randomcomplaint_error(self, ctx, error):
        logging.error('Command "randomcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivedcomplaints')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archivedcomplaints(self, ctx):
        """Returns all archived complaints"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivedcomplaints"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivedcomplaints"')
        complaints = await getComplaints(True)
        for complaint in complaints:
            if complaint=='T':
                await ctx.send('No Archived complaints')
                break
            else:
                await ctx.send(complaint)

    @archivedcomplaints.error
    async def archivedcomplaints_error(self, ctx, error):
        logging.error('Command "archivedcomplaints" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='editarchivedcomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editarchivedcomplaint(self, ctx):
        """Edit an archived complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "editarchivedcomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editarchivedcomplaint"')
        await editComplaint(ctx.message.content[len('editarchivedcomplaint '):].strip(), True)
        await ctx.send("Edited archived complaint")

    @editarchivedcomplaint.error
    async def editarchivedcomplaint_error(self, ctx, error):
        logging.error('Command "editarchivedcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



    @commands.command(pass_context=True, name='editcomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editcomplaint(self, ctx):
        """edit a complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "editcomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editcomplaint"')
        await editComplaint(ctx.message.content[len('editcomplaint '):].strip(), False)
        await ctx.send("Edited complaint")

    @editcomplaint.error
    async def editcomplaint_error(self, ctx, error):
        logging.error('Command "editcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='complaints')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def complaints(self, ctx):
        """return all complaints"""
        sys.stdout.write(f'{ctx.message.author} ran command "complaints"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "complaints"')
        complaints = await getComplaints(False)
        for complaint in complaints:
            if complaint=='T':
                await ctx.send('No complaints')
                break
            else:
                await ctx.send(complaint)

    @complaints.error
    async def complaints_error(self, ctx, error):
        logging.error('Command "complaints" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='complaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def complaint(self, ctx):
        """Return a specific complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "complaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "complaint"')
        complaint = ctx.message.content[len('complaint '):].strip()
        await ctx.send(await getComplaint(complaint, False))

    @complaint.error
    async def complaint_error(self, ctx, error):
        logging.error('Command "complaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deletecomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletecomplaint(self, ctx):
        """Delete a complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletecomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletecomplaint"')
        complaint = ctx.message.content[len('deletecomplaint '):]
        nums = complaint.split(' ')
        for num in nums:
            await deleteComplaint(num, False)
            await ctx.send("Deleted complaint")

    @deletecomplaint.error
    async def deletecomplaint_error(self, ctx, error):
        logging.error('Command "deletecomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletearchivedcomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletearchivedcomplaint(self, ctx):
        """Delete an archived complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchivedcomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchivedcomplaint"')
        complaint = ctx.message.content[len('deletearchivedcomplaint '):].strip()
        nums = complaint.split(' ')
        for num in nums:
            await deleteComplaint(num, True)
            await ctx.send("Deleted archived complaint")

    @deletearchivedcomplaint.error
    async def deletearchivedcomplaint_error(self, ctx, error):
        logging.error('Command "deletearchivedcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #TODO finish implementing lock
    @commands.command(pass_context=True, name='deleteallarchivedcomplaints COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedcomplaintscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedcomplaintscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedcomplaintscommit"')
        await deleteAllComplaints(True)
        await ctx.send("Deleted all archived complaints")

    @deleteallarchivedcomplaintscommit.error
    async def deleteallarchivedcomplaintscommit_error(self, ctx, error):
        logging.error('Command "deleteallarchivedcomplaintscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallarchivedcomplaints')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedcomplaints(self, ctx):
        """Delete all archived complaints"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedcomplaints"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedcomplaints"')
        await ctx.send("Are you sure you want to delete all archived complaints?\nType ```?deleteallarchivedcomplaints COMMIT``` to continue")

    @deleteallarchivedcomplaints.error
    async def deleteallarchivedcomplaints_error(self, ctx, error):
        logging.error('Command "deleteallarchivedcomplaints" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallcomplaints COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallcomplaintscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallcomplaintscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallcomplaintscommit"')
        await deleteAllComplaints(False)
        await ctx.send("Deleted all complaints")

    @deleteallcomplaintscommit.error
    async def deleteallcomplaintscommit_error(self, ctx, error):
        logging.error('Command "deleteallcomplaintscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallcomplaints')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallcomplaints(self, ctx):
        """Delete all complaints"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallcomplaints"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallcomplaints"')
        await ctx.send("Are you sure you want to delete all complaints?\nType ```?deleteallcomplaints COMMIT``` to continue")

    @deleteallcomplaints.error
    async def deleteallcomplaints_error(self, ctx, error):
        logging.error('Command "deleteallcomplaints" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newarchivedcomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newarchivedcomplaint(self, ctx):
        """Create a new archived complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "newarchivedcomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newarchivedcomplaint"')
        complaint = ctx.message.content[len('|newarchivedcomplaint '):].strip()
        await addComplaint(complaint, True)
        await ctx.send("Added complaint {}".format(complaint))

    @newarchivedcomplaint.error
    async def newarchivedcomplaint_error(self, ctx, error):
        logging.error('Command "newarchivedcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='complain')
    async def complain(self, ctx):
        """Create a new complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "complain"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "complain"')
        complaint = ctx.message.content[len('complain '):].strip()
        await addComplaint(complaint, False)
        await ctx.send("Added complaint {}".format(complaint))

    @complain.error
    async def complain_error(self, ctx, error):
        logging.error('Command "complain" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivecomplaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archivecomplaint(self, ctx):
        """Archive a complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivecomplaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivecomplaint"')
        complaint = ctx.message.content[len('archivecomplaint '):].strip()
        await archiveComplaint(complaint)
        await ctx.send("Archived complaint " + complaint)

    @archivecomplaint.error
    async def archivecomplaint_error(self, ctx, error):
        logging.error('Command "archivedcomplaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='complaint')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def complaint(self, ctx):
        """Return a specific complaint"""
        sys.stdout.write(f'{ctx.message.author} ran command "complaint"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "complaint"')
        complaint = ctx.message.content[len('complaint '):].strip()
        if len(complaint) == 0:
            await ctx.send("?complaint id               ?t id           Returns a specific complaint.")
        await ctx.send(await getComplaint(complaint, True))

    @complaint.error
    async def complaint_error(self, ctx, error):
        logging.error('Command "complaint" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


def setup(bot):
    bot.add_cog(ComplaintCog(bot))
