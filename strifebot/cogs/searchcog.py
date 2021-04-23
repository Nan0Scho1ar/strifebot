import urbandictionary as ud
import sys
import logging
from wordnik import *
import wikipedia
import discord
from discord.ext import commands
import re

WORDNIK_URL = 'http://api.wordnik.com/v4'

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
    elif "WORKNIK_KEY" in line:
        WORKNIK_KEY = line.split("=")[-1:][0].strip()

wordnikClient = swagger.ApiClient(WORKNIK_KEY, WORDNIK_URL)
wordApi = WordApi.WordApi(wordnikClient)

# START SEARCH FUNCTIONS

#Search Wikipedia
async def wikiSearch(term):
    try:
        page = wikipedia.page(term)
        summary = wikipedia.summary(term, sentences=5)
        #print(summary)
        #print(page)
        em = discord.Embed(title=str(page.title), description=str(summary) + '\n' +  page.url, colour=0x7eff00)
        if len(page.images) > 0:
            em.set_thumbnail(url=page.images[0])
        #if len(page.images) > 0:
        #    em.set_author(name=str(page.title), icon_url=page.images[0])
        #else:
        #    em.set_author(name=str(page.title), icon_url=client.user.default_avatar_url)
        return em
    except wikipedia.exceptions.DisambiguationError as es:
        #print(es)
        lines = str(es).split('\n')
        #print(lines)
        desc = ''
        i = 0
        for line in lines:
            if i == 0:
                #print(line)
                desc += line + '\n'
                i += 1
            elif i < 51:
                #print(line)
                desc += str(i) + ': ' + line + '\n'
                i += 1
            else:
                desc += '\nRESULTS TRUNCATED\n'
                break
        #print(desc)
        em = discord.Embed(title="use '|wikip #' to continue", description=str(desc), colour=0x7eff00)
        em.set_author(name='Disambiguation Required', icon_url='')
        return em
    except wikipedia.exceptions.PageError as es:
        em = discord.Embed(title="Error", description="Page not found", colour=0x7eff00)
        em.set_author(name='Cannot find page' + str(term), icon_url='')
        return em


#Search dictionaries
async def define(dictChoice, word):
    pospeech = ''
    if word.lower().strip().startswith('noun '):
        pospeech = 'noun'
        word = word[len('noun '):].strip()
    elif word.lower().strip().startswith('adjective '):
        pospeech = 'adjective'
        word = word[len('adjective '):].strip()
    elif word.lower().strip().startswith('verb '):
        pospeech = 'verb'
        word = word[len('verb '):].strip()
    elif word.lower().strip().startswith('adverb '):
        pospeech = 'adverb'
        word = word[len('adverb '):].strip()
    elif word.lower().strip().startswith('interjection '):
        pospeech = 'interjection'
        word = word[len('interjection '):].strip()
    elif word.lower().strip().startswith('pronoun '):
        pospeech = 'pronoun'
        word = word[len('pronoun '):].strip()
    elif word.lower().strip().startswith('preposition '):
        pospeech = 'preposition'
        word = word[len('preposition '):].strip()
    elif word.lower().strip().startswith('abbreviation '):
        pospeech = 'abbreviation'
        word = word[len('abbreviation '):].strip()
    elif word.lower().strip().startswith('affix '):
        pospeech = 'affix'
        word = word[len('affix '):].strip()
    elif word.lower().strip().startswith('article '):
        pospeech = 'article'
        word = word[len('article '):].strip()
    elif word.lower().strip().startswith('auxiliary-verb '):
        pospeech = 'auxiliary-verb'
        word = word[len('auxiliary-verb '):].strip()
    elif word.lower().strip().startswith('conjunction '):
        pospeech = 'conjunction'
        word = word[len('conjunction '):].strip()
    elif word.lower().strip().startswith('definite-article '):
        pospeech = 'definite-article'
        word = word[len('definite-article '):].strip()
    elif word.lower().strip().startswith('family-name '):
        pospeech = 'family-name'
        word = word[len('family-name '):].strip()
    elif word.lower().strip().startswith('given-name '):
        pospeech = 'given-name'
        word = word[len('given-name '):].strip()
    elif word.lower().strip().startswith('idiom '):
        pospeech = 'idiom'
        word = word[len('idiom '):].strip()
    elif word.lower().strip().startswith('imperative '):
        pospeech = 'imperative'
        word = word[len('imperative '):].strip()
    elif word.lower().strip().startswith('noun-plural '):
        pospeech = 'noun-plural'
        word = word[len('noun-plural '):].strip()
    elif word.lower().strip().startswith('noun-posessive '):
        pospeech = 'noun-posessive'
        word = word[len('noun-posessive '):].strip()
    elif word.lower().strip().startswith('past-participle '):
        pospeech = 'past-participle'
        word = word[len('past-participle '):].strip()
    elif word.lower().strip().startswith('phrasal-prefix '):
        pospeech = 'phrasal-prefix'
        word = word[len('phrasal-prefix '):].strip()
    elif word.lower().strip().startswith('propper-noun '):
        pospeech = 'propper-noun'
        word = word[len('propper-noun '):].strip()

    logging.info("Getting definitions")
    logging.info(word)
    logging.info(pospeech)
    logging.info(dictChoice)
    if pospeech == '':
        definitions = wordApi.getDefinitions(word, sourceDictionaries=dictChoice)
    else:
        definitions = wordApi.getDefinitions(word, partOfSpeech=pospeech, sourceDictionaries=dictChoice)
    if definitions is None:
        return discord.Embed(title="Definitons for {}".format(word), description="Could not find definition matching search parameters", colour=0x7eff00)
    body = ""
    attr = definitions[0].attributionText
    for definition in definitions:
        if len(body) < 1800:
            if pospeech == '':
                if not attr == definition.attributionText:
                    if len(body) > 0:
                        body += "{}\n-=+=-\n\n".format(attr)
                    attr = definition.attributionText
                body += "{}\n{}\n\n".format(definition.partOfSpeech, definition.text)
            elif pospeech == definition.partOfSpeech:
                if not attr == definition.attributionText:
                    if len(body) > 0:
                        body += "{}\n-=+=-\n\n".format(attr)
                    attr = definition.attributionText
                body += "{}\n\n".format(definition.text)
            #body += "{}\n{}\n{}\n\n".format(definition.partOfSpeech, definition.text, definition.sourceDictionary)
    body += attr
    body = str(body)
    body = re.sub("\<i\>", "*", body)
    body = re.sub("\</i\>", "*", body)
    body = re.sub("\<strong\>", "**", body)
    body = re.sub("\</strong\>", "**", body)
    body = re.sub("\<em\>", "**", body)
    body = re.sub("\</em\>", "**", body)
    body = re.sub("\</", "<", body)
    body = re.sub("\<internalXref.*\>", "", body)
    body = re.sub("\<spn\>", "", body)
    body = re.sub("\<altname\>", "", body)
    body = re.sub("\<xref\>", "", body)
    if body == "":

        return discord.Embed(title="Definitons for {}".format(word), description="Could not find definition matching search parameters", colour=0x7eff00)
    if pospeech == '':
        em = discord.Embed(title="Definitons for {}".format(word), description=body, colour=0x7eff00)
    else:
        em = discord.Embed(title="{} definitons for {}".format(pospeech, word), description=body, colour=0x7eff00)
    #em.set_author(name='', icon_url=client.user.default_avatar_url)
    return em


class SearchCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Dictionary search
    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def define(self, ctx):
        """Returns the definition for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "define"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "define"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        em = await define("all", word)
        await ctx.send(embed=em)

    @define.error
    async def define_error(self, ctx, error):
        logging.error('Command "define" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def ahd(self, ctx):
        """Search American Heritage dictionary for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "ahd"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "ahd"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        #em = await define("ahd", word)
        em = discord.Embed(title="AHD unavailable", description="Due to API issues both AHD and Macmillan are unavailable.", colour=0x7eff00)
        await ctx.send(embed=em)

    @ahd.error
    async def ahd_error(self, ctx, error):
        logging.error('Command "ahd" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def century(self, ctx):
        """Search Century dictionary for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "century"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "century"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        em = await define("century", word)
        await ctx.send(embed=em)

    @century.error
    async def century_error(self, ctx, error):
        logging.error('Command "century" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #@commands.command(pass_context=True)
    #@commands.has_role(504227058738790400)
    #async def cmu(self, ctx):
    #    word = message.content[len('cmu '):].strip()
    #    em = await define("cmu", word)
    #    await ctx.send(embed=em)

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def macmillan(self, ctx):
        """Search Macmillan dictionary for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "macmillan"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "macmillan"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        #em = await define("macmillan", word)
        em = discord.Embed(title="Macmillan unavailable", description="Due to API issues both Macmillan and AHD are unavailable.", colour=0x7eff00)
        await ctx.send(embed=em)

    @macmillan.error
    async def macmillan_error(self, ctx, error):
        logging.error('Command "macmillan" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def wiktionary(self, ctx):
        """Search Wictionary for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "wiktionary"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "wiktionary"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        em = await define("wiktionary", word)
        await ctx.send(embed=em)

    @wiktionary.error
    async def wiktionary_error(self, ctx, error):
        logging.error('Command "wiktionary" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def webster(self, ctx):
        """Search Webster dictionary for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "webster"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "webster"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        em = await define("webster", word)
        await ctx.send(embed=em)

    @webster.error
    async def webster_error(self, ctx, error):
        logging.error('Command "webster" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def wordnet(self, ctx):
        """Search Wordnet for a word"""
        sys.stdout.write(f'{ctx.message.author} ran command "wordnet"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "wordnet"')
        word = ctx.message.content.split(" ", 1)[1].strip()
        em = await define("wordnet", word)
        await ctx.send(embed=em)

    @wordnet.error
    async def wordnet_error(self, ctx, error):
        logging.error('Command "wordnet" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #Wikipedia continue with disambiguation
    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def wikip(self, ctx):
        """Continue from wikipedia disambiguation"""
        sys.stdout.write(f'{ctx.message.author} ran command "wikip"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "wikip"')
        selection = int(ctx.message.content[len('wikip '):])
        messageFound = False
        async for message in ctx.message.channel.history(limit=20):
            if message.author == self.bot.user:
                if len(message.embeds) > 0 :
                    #print(message.embeds)
                    embed = message.embeds[0]
                    #print(embed)
                    if embed.title == "use '|wikip #' to continue":
                        description = embed.description
                        #print(description)
                        lines = str(description).split('\n')
                        #print(lines)
                        #print(selection)
                        if len(lines) > selection:
                            line = lines[selection]
                            #print(line)
                            if len(line) > 0:
                                em = await wikiSearch(line)
                                await ctx.send(embed=em)
                                messageFound = True
                            else:
                                await ctx.send("Invalid Selection")
                                messageFound = True
                        else:
                            await ctx.send("Invalid Selection")
                            messageFound = True
                        break
        if not messageFound:
            await ctx.send("Search with '|wiki topic' before attempting to continue")

    @wikip.error
    async def wikip_error(self, ctx, error):
        logging.error('Command "wikip" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    # #Wikipedia
    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def wiki(self, ctx):
        """Search wikipedia"""
        sys.stdout.write(f'{ctx.message.author} ran command "wiki"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "wiki"')
        message = ctx.message
        term = message.content[len('wiki '):].strip()
        em =  await wikiSearch(term)
        await ctx.send(embed=em)

    @wiki.error
    async def wiki_error(self, ctx, error):
        logging.error('Command "wiki" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    #Urban Dictionary
    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def ud(self, ctx):
        """Search urban dictionary"""
        sys.stdout.write(f'{ctx.message.author} ran command "ud"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "ud"')
        message = ctx.message
        term = message.content[len('ud '):]
        defs = ud.define(term)
        if len(defs) < 1:
            await ctx.send("could not find definition for '{}' ".format(term))
        else:
            word = defs[0].word
            body = ''
            for d in defs:
                if len(body) < 1500:
                    body += d.definition + '\n'
                else:
                    body += 'RESULTS TRUNCATED'
                    break
            em = discord.Embed(title=word, description=body, colour=0x7eff00)
            await ctx.send(embed=em)

    @ud.error
    async def ud_error(self, ctx, error):
        logging.error('Command "ud" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #Urban Dictionary Random
    @commands.command(pass_context=True)
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, commoners_roleid, cbbb)
    async def udr(self, ctx):
        """Returns a random urban dictionary article"""
        sys.stdout.write(f'{ctx.message.author} ran command "udr"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "udr"')
        defs = ud.random()
        em = discord.Embed(title=defs[0].word, description=defs[0].definition, colour=0x7eff00)
        await ctx.send(embed=em)

    @udr.error
    async def udr_error(self, ctx, error):
        logging.error('Command "udr" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

# END SEARCH COMMANDS


def setup(bot):
    bot.add_cog(SearchCog(bot))
