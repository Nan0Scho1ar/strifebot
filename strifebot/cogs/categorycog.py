import requests
import sys
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

# START CATEGORIES FUNCTIONS
#return questions for a specific category
async def category(category, approved):
    if approved:
        r = requests.get(APPROVED_URL)
    else:
        r = requests.get(SUGGESTED_URL)
    batch = []
    topics = "```"
    for topic in r.json():
        if topic['CATEGORY'] == category:
            t = topic['TOPIC'] + "\n"
            if len(t) + len(topics) > 1950:
                batch.append(topics + '```')
                topics = "```" + t
            else:
                topics += t
    batch.append(topics + '```')

    if batch[0] == "``````":
        if approved:
            batch[0] = "There are currently no approved category matching "  + category
        else:
            batch[0] = "There are currently no suggested category matching " + category
    return batch


#return the categories
async def categories(approved):
    if approved:
        r = requests.get(APPROVED_URL)
    else:
        r = requests.get(SUGGESTED_URL)
    cats  = []
    for topic in r.json():
        category = str(topic['CATEGORY'])
        if category not in cats:
            cats.append(category)
    catString = '\n'.join(cats)
    categories = "```\n" + catString + "```"
    if len(categories) > 1900:
        categories = categories[:1900]
        categories += "RESULTS TRUNCATED"
    if categories == "``````":
        if approved:
            topics = "There are currently no approved category "
        else:
            topics = "There are currently no suggested category "
    return categories

# END CATEGORIES FUNCTIONS




class CategoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# START CATEGORIES COMMANDS

    #Returns all topics for a suggested category
    @commands.command(pass_context=True, name='suggestedcategory', aliases=['cs'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def suggestedcategory(self, ctx):
        """Returns all topics for a suggested category"""
        sys.stdout.write(f'{ctx.message.author} ran command "suggestedcategory"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "suggestedcategory"')
        if ctx.message.content.lower().strip().startswith('suggestedcategory '):
            cat = ctx.message.content[len('suggestedcategory '):].strip()
        else:
            cat = ctx.message.content[len('cs '):].strip()
        topics = await category(cat, False)
        await ctx.send(topics)

    @suggestedcategory.error
    async def suggestedcategory_error(self, ctx, error):
        logging.error('Command "suggestedcategory" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    #Returns all suggested categories
    @commands.command(pass_context=True, name='suggestedcategories', aliases=['acs'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, clerk_roleid, cbbb)
    async def suggestedcategories(self, ctx):
        """Returns all suggested categories"""
        sys.stdout.write(f'{ctx.message.author} ran command "suggestedcategories"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "suggestedcategories"')
        cats = await categories(False)
        await ctx.send(cats)

    @suggestedcategories.error
    async def suggestedcategories_error(self, ctx, error):
        logging.error('Command "suggestedcategories" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



    #Returns all categories
    @commands.command(pass_context=True, name='categories', aliases=['ac'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def categories(self, ctx):
        """Returns all categories"""
        sys.stdout.write(f'{ctx.message.author} ran command "categories"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "categories"')
        cats = await categories(True)
        await ctx.send(cats)

    @categories.error
    async def categories_error(self, ctx, error):
        logging.error('Command "categories" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #Returns all topics for a category
    @commands.command(pass_context=True, name='category', aliases=['c'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def category(self, ctx):
        """Returns all topics for a category"""
        sys.stdout.write(f'{ctx.message.author} ran command "category"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "category"')
        if ctx.message.content.lower().strip().startswith('category '):
            cat = ctx.message.content[len('category '):].strip()
        else:
            cat = ctx.message.content[len('c '):].strip()
        topics = await category(cat, True)
        for msg in topics:
            await ctx.send(msg)

    @category.error
    async def category_error(self, ctx, error):
        logging.error('Command "category" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

# END CATEGORIES COMMANDS






def setup(bot):
    bot.add_cog(CategoryCog(bot))
