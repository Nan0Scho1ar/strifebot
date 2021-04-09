import requests
import sys
import xmltodict
import random
import json
import logging
from discord.ext import commands

APPROVED_URL = 'http://localhost:5000/approved'
SUGGESTED_URL = 'http://localhost:5000/suggested'

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
# START TOPICS FUNCTIONS


#returns a codeblock containing all approved or suggested topics
async def getTopics(approved):
    if approved:
        r = requests.get(APPROVED_URL)
    else:
        r = requests.get(SUGGESTED_URL)
    topics = []
    chunk = "```"
    for topic in r.json():
        if (len(chunk) > 1800):
            chunk += "```"
            topics.append(chunk)
            chunk = "```"
        chunk += "{}: {} | {}\n".format(topic['id'], topic['TOPIC'], topic['CATEGORY'])
    chunk += "```"
    topics.append(chunk)
    if topics[0] == "``````":
        if approved:
            topics = "There are currently no approved topics"
        else:
            topics = "There are currently no suggested topics"
    return topics



#returns a codeblock containing a specific approved or suggested topic
async def getTopic(id, approved):
    if approved:
        r = requests.get(APPROVED_URL + '/' + id)
    else:
        r = requests.get(SUGGESTED_URL + '/' + id)
    topics = "```"
    for topic in r.json():
        topics += "{}: {} | {}\n".format(topic['id'], topic['TOPIC'], topic['CATEGORY'])
    topics += "```"
    if topics == "``````":
        if approved:
            topics = "Cannot find approved topic with id " + id
        else:
            topics = "Cannot find suggested topic with id " + id
    return topics



#deletes a specific approved or suggested topic
async def deleteTopic(id, approved):
    if approved:
        r = requests.delete(APPROVED_URL + '/' + id)
    else:
        r = requests.delete(SUGGESTED_URL + '/' + id)
    return



#deletes a all approved or suggested topics
async def deleteAllTopics(approved):
    if approved:
        r = requests.delete(APPROVED_URL)
    else:
        r = requests.delete(SUGGESTED_URL)
    return



#returns a random aproved topic
async def getRandomTopic():
    r = requests.get(APPROVED_URL).json()
    topic = r[random.randint(0, len(r))]
    return ":thinking:  ***Debate Topic:***  {} :thinking: ".format(topic['TOPIC'])



#adds a new approved, or suggested topic
async def addTopic(topic, approved):
    d = topic.split('|')
    data = {'TOPIC': d[0].strip(), 'CATEGORY': d[1].strip()}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if approved:
        requests.post(APPROVED_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(SUGGESTED_URL, data=json.dumps(data), headers=headers)
    return



#edits an approved or suggested topic
#data format should be "id newTopicText, newDisciplineText"
async def editTopic(din, approved):
    data = din.split(' ', 1)
    data2 = data[1].split('|', 1)
    finalData = {'TOPIC': data2[0].strip(), 'CATEGORY': data2[2].strip()}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if approved:
                             #url + topicID
        requests.put(APPROVED_URL + data[0], data=json.dumps(finalData), headers=headers)
    else:
        requests.put(SUGGESTED_URL + data[0], data=json.dumps(finalData), headers=headers)



#approve suggested topic by topicID
async def approveTopic(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(SUGGESTED_URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'TOPIC': t['TOPIC'], 'CATEGORY': t['CATEGORY']}
    requests.post(APPROVED_URL, data=json.dumps(data), headers=headers)
    requests.delete(SUGGESTED_URL + '/' + id)


# END TOPICS FUNCTIONS



class TopicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    general_channelid = 477733476175708160

    @commands.command(pass_context=True, name='rtmain')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def rtmain(self, ctx):
        """Posts a random topic in main"""
        sys.stdout.write(f'{ctx.message.author} ran command "rtmain"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "rtmain"')
        main = self.bot.get_channel(general_channelid)
        await main.send(await getRandomTopic())

    @rtmain.error
    async def rtmain_error(self, ctx, error):
        logging.error('Command "rtmain" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='randomtopic', aliases=['rt'], help='Randomly selects an approved topic.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomtopic(self, ctx):
        """Posts a random topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomtopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomtopic"')
        await ctx.send(await getRandomTopic())

    @randomtopic.error
    async def randomtopic_error(self, ctx, error):
        logging.error('Command "randomtopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='topics', aliases=['at'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def topics(self, ctx):
        """Returns all topics"""
        sys.stdout.write(f'{ctx.message.author} ran command "topics"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "topics"')
        topics = await getTopics(True)
        for topic in topics:
            if topic=='T':
                await ctx.send('No Accepted topics')
                break
            else:
                await ctx.send(topic)

    @topics.error
    async def topics_error(self, ctx, error):
        logging.error('Command "topics" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='edittopic', aliases=['et'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def edittopic(self, ctx):
        """Edit a topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "edittopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "edittopic"')
        if ctx.message.content.lower().strip().startswith('edittopic '):
            await editTopic(ctx.message.content[len('edittopic '):].strip(), True)
        else:
            await editTopic(ctx.message.content[len('et '):].strip(), True)
        await ctx.send("Edited approved topic")

    @edittopic.error
    async def edittopic_error(self, ctx, error):
        logging.error('Command "edittopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



    @commands.command(pass_context=True, name='editsuggestedtopic', aliases=['est'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editsuggestedtopic(self, ctx):
        """Edit a suggested topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "editsuggestedtopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editsuggestedtopic"')
        if ctx.message.content.lower().strip().startswith('editsuggestedtopic '):
            await editTopic(ctx.message.content[len('editsuggestedtopic '):].strip(), False)
        else:
            await editTopic(ctx.message.content[len('est '):].strip(), False)
        await ctx.send("Edited suggested topic")

    @editsuggestedtopic.error
    async def editsuggestedtopic_error(self, ctx, error):
        logging.error('Command "editsuggestedtopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='suggestedtopics', aliases=['ats'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def suggestedtopics(self, ctx):
        """Returns all suggested topics"""
        sys.stdout.write(f'{ctx.message.author} ran command "suggestedtopics"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "suggestedtopics"')
        topics = await getTopics(False)
        for topic in topics:
            if topic=='T':
                await ctx.send('No Suggested topics')
                break
            else:
                await ctx.send(topic)

    @suggestedtopics.error
    async def suggestedtopics_error(self, ctx, error):
        logging.error('Command "suggestedtopics" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='suggestedtopic', aliases=['ts'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def suggestedtopic(self, ctx):
        """Returns a specific suggested topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "suggestedtopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "suggestedtopic"')
        if ctx.message.content.lower().strip().startswith('suggestedtopic '):
            topic = ctx.message.content[len('suggestedtopic '):].strip()
        else:
            topic = ctx.message.content[len('ts '):].strip()
        await ctx.send(await getTopic(topic, False))

    @suggestedtopic.error
    async def suggestedtopic_error(self, ctx, error):
        logging.error('Command "suggestedtopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deletesuggestedtopic', aliases=['rms'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletesuggestedtopics(self, ctx):
        """Delete a suggested topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletesuggestedtopics"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletesuggestedtopics"')
        if ctx.message.content.lower().strip().startswith('deletesuggestedtopic '):
            topic = ctx.message.content[len('deletesuggestedtopic '):]
        else:
            topic = ctx.message.content[len('rms '):]
        nums = topic.split(' ')
        for num in nums:
            await deleteTopic(num, False)
            await ctx.send("Deleted suggested topic")

    @deletesuggestedtopics.error
    async def deletesuggestedtopics_error(self, ctx, error):
        logging.error('Command "deletesuggestedtopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletetopic', aliases=['rm'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletetopic(self, ctx):
        """Delete a topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletetopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletetopic"')
        if ctx.message.content.lower().strip().startswith('deletetopic '):
            topic = ctx.message.content[len('deletetopic '):].strip()
        else:
            topic = ctx.message.content[len('rm '):].strip()
        nums = topic.split(' ')
        for num in nums:
            await deleteTopic(num, True)
            await ctx.send("Deleted approved topic")

    @deletetopic.error
    async def deletetopic_error(self, ctx, error):
        logging.error('Command "deletetopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallapprovedtopics COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletealltopicscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletealltopicscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletetopic"')
        await deleteAllTopics(True)
        await ctx.send("Deleted all approved topics")

    @deletealltopicscommit.error
    async def deletealltopicscommit_error(self, ctx, error):
        logging.error('Command "deletealltopicscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletealltopics')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deletealltopics(self, ctx):
        """Delete all topics"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletealltopics"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletealltopics"')
        await ctx.send("Are you sure you want to delete all approved topics?\nType ```|deleteallapprovedtopics COMMIT``` to continue")

    @deletealltopics.error
    async def deletealltopics_error(self, ctx, error):
        logging.error('Command "deletealltopics" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallsuggestedtopics COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallsuggestedtopicscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallsuggestedtopicscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallsuggestedtopicscommit"')
        await deleteAllTopics(False)
        await ctx.send("Deleted all suggested topics")

    @deleteallsuggestedtopicscommit.error
    async def deleteallsuggestedtopicscommit_error(self, ctx, error):
        logging.error('Command "deleteallsuggestedtopicscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallsuggestedtopics')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallsuggestedtopics(self, ctx):
        """Delete all suggested topics"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallsuggestedtopics"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallsuggestedtopics"')
        await ctx.send("Are you sure you want to delete all suggested topics?\nType ```|deleteallsuggestedtopics COMMIT``` to continue")

    @deleteallsuggestedtopics.error
    async def deleteallsuggestedtopics_error(self, ctx, error):
        logging.error('Command "deleteallsuggestedtopics" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newtopic', aliases=['nt'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newtopic(self, ctx):
        """Add a new debate topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "newtopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newtopic"')
        topic = ctx.message.content.split(' ', 1)[1]
        await addTopic(topic, True)
        await ctx.send("Added topic {}".format(topic))

    @newtopic.error
    async def newtopic_error(self, ctx, error):
        logging.error('Command "newtopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='suggesttopic', aliases=['nts'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def suggesttopic(self, ctx):
        """Suggest a new debate topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "suggesttopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "suggesttopic"')
        topic = ctx.message.content.split(' ', 1)[1]
        await addTopic(topic, False)
        await ctx.send("Suggested topic {}".format(topic))

    @suggesttopic.error
    async def suggesttopic_error(self, ctx, error):
        logging.error('Command "suggesttopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='approvetopic', aliases=['ap'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def approvetopic(self, ctx):
        """Approve a suggested topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "approvetopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "approvetopic"')
        if ctx.message.content.lower().strip().startswith('approvetopic '):
            topic = ctx.message.content[len('approvetopic '):].strip()
        else:
            topic = ctx.message.content[len('ap '):].strip()
        await approveTopic(topic)
        await ctx.send("Approved topic " + topic)

    @approvetopic.error
    async def approvetopic_error(self, ctx, error):
        logging.error('Command "approvetopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='topic', aliases=['t'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def topic(self, ctx):
        """Returns a topic"""
        sys.stdout.write(f'{ctx.message.author} ran command "topic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "topic"')
        if ctx.message.content.lower().strip().startswith('topic '):
            topic = ctx.message.content[len('topic '):].strip()
            #print(topic)
            if len(topic) == 0:
                await ctx.send("?topic id               ?t id           Returns a specific topic.")
        else:
            topic = ctx.message.content[len('t '):].strip()
            #print(topic)
            if len(topic) == 0:
                await ctx.send("topic id               ?t id           Returns a specific topic.")
        await ctx.send(await getTopic(topic, True))

    @topic.error
    async def topic_error(self, ctx, error):
        logging.error('Command "topic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________





    @commands.command(pass_context=True, name='newdebatetopic', aliases=['ndt'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newdebatetopic(self, ctx):
        """Creates a new debate topic from a third party database"""
        sys.stdout.write(f'{ctx.message.author} ran command "newdebatetopic"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newdebatetopic"')
        topic = ctx.message.content[len('ndt '):].strip()
        print(topic)
        theinput = topic.split()
        if len(theinput) > 0:
            categoryInput = int(theinput[0])
        else:
            categoryInput = 0
        if len(theinput) > 1:
            search = topic.split()[1]
            numRows = '96'
        else:
            search = 'all'
            numRows = 12


        if categoryInput == 0:
            category = "alltopics"
        elif categoryInput == 1:
            category = "politics"
        elif categoryInput == 2:
            category = "technology"
        elif categoryInput == 3:
            category = "shopping"
        elif categoryInput == 4:
            category = "travel"
        elif categoryInput == 5:
            category = "science"
        elif categoryInput == 6:
            category = "religion"
        elif categoryInput == 7:
            category = "world"
        elif categoryInput == 8:
            category = "sports"
        elif categoryInput == 9:
            category = "business"
        elif categoryInput == 10:
            category = "entertainment"
        elif categoryInput == 11:
            category = "comedy"

        sort = 'relevance'
        if search == "all":
            sort = "random"

        debates = []
        response = requests.get('http://www.createdebate.com/browse/debaterss/{0}/all/{1}/alltime/{2}/0/{3}/all/{4}/xml'.format(sort, 'alltypes', category, numRows, search))
        dbDict = xmltodict.parse(response.content)
        debateDict = dbDict['debates']['debate']
        for d in debateDict:
            debate = {}
            debate['title'] = d['title']
            debate['sides'] = []
            debate['stringname'] = d['title']
            if search == "all" or  search in debate['title']:    
                sides = d['sides']['side']
                for side in sides:
                    if not side == 'title' and not side == 'pointsVal' and not side == 'voteNum' and not side == 'arguments':
                        debate['sides'].append(side['title'])
                        debate['stringname'] += "\n" + side['title'] 
                        #debates.append(debate)
                #if len(debate['sides']) > 1:
                await ctx.send("```{}```".format(debate['stringname']))

    @newdebatetopic.error
    async def newdebatetopic_error(self, ctx, error):
        logging.error('Command "newdebatetopic" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


# # END TOPICS COMMANDS




def setup(bot):
    bot.add_cog(TopicCog(bot))
