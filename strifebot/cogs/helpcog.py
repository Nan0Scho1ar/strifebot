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

# START TEXT AND EMBED RESPONSE FUNCTIONS

#returns a codeblock containing the help text
help1text = '''
```
                     -===<           Topics           >===-

|randomtopic                          |rt             Randomly selects an approved topic.

|topics                               |at             Returns a list of all topics.
|categories                           |ac             Returns a list of all categories.
|suggestedtopics                      |ats            Returns a list of all suggested topics.
|suggestedcategories                  |acs            Returns a list of all suggested categories.

|topic id                             |t id           Returns a specific topic. 
|suggestedtopic id                    |ts id          Returns a specific suggested topic.

|category cat                         |c c            Returns a list of topics for category.
|suggestedcategory cat                |cs c           Returns a list of topics for suggested category.

|newtopic topic | cat                 |nt t | c       Adds topic to one of the two list (depending on moderator status).
|suggesttopic topic | cat             |nts t | c      Adds topic to the suggested list.

|edittopic id topic | cat             |et id t | c    Updates an approved topic.
|editsuggestedtopic id topic | cat    |ets id t | c   Updates an suggested topic.

|deletetopics id id id...             |rm id          Deletes one or more topics.
|deletesuggestedtopics id id          |rms id id      Deletes an suggested topic.
|deleteallTopics                                      CAREFUL!!! deletes all approved topics|
|deleteallsuggestedtopics                             CAREFUL!!! deletes all suggested topics|

|approvetopic id                      |ap id          Approves a topic on the suggested list.

                   -=See Also     |help2    |h2       See Also=-
```
'''

help1commontext = '''
```
|categories                           Returns a list of approved categories.\n
|category cat                         Returns a list of topics for chosen catagory.\n
|suggesttopic topic | category        Adds topic to the suggested list.\n

|wiki search                          Search for a wiki article.\n
|wikip id                             Continue from disambiguation.\n

|ud search                            Search Urban Dictionary.\n
|udrandom                             Random Urban Dictionary factoid.\n

|help                                 Displays this help dialog\n
|hello                                Displays a friendly greeting
```
'''

help3text = '''

```
!!!Remember!!! Emoji must be used when refering to a vc !!!Remember!!!   TODO:delete messages on response
_____________________________________________________________________________________________________________________
                                -=Debate=-

|debate                           |db             Displays a help text.
|debate vc, topic, @mentions      |db v, t, @     Start debate, move everyone to vc, (n0s1) trigger craig start, assign roles, post announcement.
|debate end vc                    |dbe v          End debate, move everyone to vc, (n0s1) trigger craig stop, remove roles.

|debate add @mentions             |dba @          Allow User/s to speak.
|debate remove @mentions          |dbr @          Disallow User/s to speak.
```
'''

#|cmu      (TODO pronounciation to be implemented) Search Carnegie Mellon University Pronouncing Dictionary
help4text = '''
```
________________________________________________________________________________________________
                                -=Search=-

|wiki search                                      Search for a wiki article.
|wikip id                                         Continue from disambiguation.
____________                                      ________________________________________________
|ud search                                        Search Urban Dictionary.
|udrandom                         |udr            Random Urban Dictionary factoid.
_____________________________________________________________________________________________________
                              -=dictionary=-
|define                                           Search All dictionaries
|ahd                                              Search American Heritage Dictionary
|century                                          Search Century Dictionary and Cyclopedia
|macmillan                                        Search Macmillan Dictionary
|wiktionary                                       Search Wiktionary
|webster                                          Search Merriam Webster Dictionary
|wordnet                                          Search Wordnet

Additionally you can include these word types to get a specific form of the word

noun, adjective, verb, adverb, interjection, pronoun, preposition, abbreviation,
affix, article, auxiliary-verb, conjunction, definite-article family-name, given-name,
idiom, imperative, noun-plural, noun-posessive, past-participle, phrasal-prefix, proper-noun

E.G
|define epistemology
|webster epistemology
|century adjective strong
_____________________________________________________________________________________________________________
```
'''
help2text = '''
```
|help                                             Displays a help dialog
|hello                                            Displays a friendly greeting
|postrules                                        Post the rules dialog
|rules @mention                                   Prompts this user to read the rules
|logs                                             Displays info about a user from the logs
|warn                                             Warns a user
|mute                                             Soft-mutes
|unmute                                           Un-soft-mutes a user
|kick                                             Kicks a user
|ban                                              Bans a user
|purgeban                                         Bans user and deletes all their messages going back one week
|commend                                          Commends a user
|read                                             Puts a user in reading
|unread                                           Removes user from reading
```
'''


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, name='fullhelp', aliases=['ha'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def fullhelp(self, ctx):
        """Return all help dialogs"""
        sys.stdout.write(f'{ctx.message.author} ran command "fullhelp"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "fullhelp"')
        await ctx.send(help1text)
        await ctx.send(help2text)
        await ctx.send(help3text)
        await ctx.send(help4text)

    @fullhelp.error
    async def fullhelp_error(self, ctx, error):
        logging.error('Command "fullhelp" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='help2', aliases=['h2'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def help2(self, ctx):
        """Return help 2"""
        sys.stdout.write(f'{ctx.message.author} ran command "help2"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "help2"')
        await ctx.send(help2text)

    @help2.error
    async def help2_error(self, ctx, error):
        logging.error('Command "help2" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='help1', aliases=['h1', 'h'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def help1(self, ctx):
        """Return help 1"""
        sys.stdout.write(f'{ctx.message.author} ran command "help1"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "help1"')
        admin = True
        if admin:
            await ctx.send(help1text)
        else:
            await ctx.send(help1text)

    @help1.error
    async def help1_error(self, ctx, error):
        logging.error('Command "help1" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='help3', aliases=['h3'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def help3(self, ctx):
        """Return help 3"""
        sys.stdout.write(f'{ctx.message.author} ran command "help3"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "help3"')
        await ctx.send(help3text)

    @help3.error
    async def help3_error(self, ctx, error):
        logging.error('Command "help3" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='help4', aliases=['search', 'h4'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def help4(self, ctx):
        """Return help 4"""
        sys.stdout.write(f'{ctx.message.author} ran command "help4"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "help4"')
        await ctx.send(help4text)

    @help4.error
    async def help4_error(self, ctx, error):
        logging.error('Command "help4" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



def setup(bot):
    bot.add_cog(HelpCog(bot))
