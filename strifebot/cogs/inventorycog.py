import requests
import sys
import logging
import xmltodict
import random
import datetime
import json
from discord.ext import commands

INVENTORY_URL = 'http://localhost:5000/items'
INVENTORY_ARCHIVE_URL = 'http://localhost:5000/archiveditems'

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


#returns a codeblock containing all archived or regular items
async def getItems(archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL)
    else:
        r = requests.get(INVENTORY_URL)
    items = []
    for item in r.json():
        items.append([item['id'], item['USERID'], item['ITEM']])
    #print(items)
    return items

#returns a the itemnumber for a given userid
async def getItemNumByUserId(userId, archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL)
    else:
        r = requests.get(INVENTORY_URL)
    for item in r.json():
        if int(item['USERID']) == int(userId):
            return item['id']
    return None


#returns a codeblock containing all archived or regular items
async def inventoryIsRegistered(userId, archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL)
    else:
        r = requests.get(INVENTORY_URL)
    for item in r.json():
        if int(item['USERID']) == int(userId):
            return True
    return False



#returns a codeblock containing a specific archived or regular item
async def getItem(id, archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(INVENTORY_URL + '/' + id)
    for item in r.json():
        item = [item['id'], item['USERID'], item['ITEM']]
    return item


#returns a user ID for a specific archived or regular item
async def getUserId(id, archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(INVENTORY_URL + '/' + id)
    for item in r.json():
        return int(item['USERID'])

#returns a user ID for a specific archived or regular item
async def getItemBalance(id, archived):
    if archived:
        r = requests.get(INVENTORY_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(INVENTORY_URL + '/' + id)
    for item in r.json():
        return int(item['ITEM'])

#deletes a specific archived or regular item
async def deleteItem(id, archived):
    if archived:
        r = requests.delete(INVENTORY_ARCHIVE_URL + '/' + id)
    else:
        r = requests.delete(INVENTORY_URL + '/' + id)
    return



#deletes a all archived or regular items
async def deleteAllItems(archived):
    if archived:
        r = requests.delete(INVENTORY_ARCHIVE_URL)
    else:
        r = requests.delete(INVENTORY_URL)
    return



#returns a random regular item
async def getRandomItem():
    r = requests.get(INVENTORY_URL).json()
    item = r[random.randint(0, len(r))]
    return "***Item:***  {} | {}".format(item['USERID'], item['ITEM'])



#adds a new archived, or regular item
async def addItem(userId, item, archived):
    data = {'USERID': userId, 'ITEM': item}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
        requests.post(INVENTORY_ARCHIVE_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(INVENTORY_URL, data=json.dumps(data), headers=headers)
    return



#edits an archived or regular item
#data format should be "id newItemText, newDisciplineText"
async def editItem(itemId, item, userId, archived):
    data = {'USERID': userId, 'ITEM': item}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
                             #url + itemID
        requests.put(INVENTORY_ARCHIVE_URL + '/' + itemId, data=json.dumps(data), headers=headers)
    else:
        requests.put(INVENTORY_URL + '/' + itemId, data=json.dumps(data), headers=headers)



#archive regular item by itemID
async def archiveItem(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(INVENTORY_URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'USERID': t['USERID'], 'ITEM': t['ITEM']}
    requests.post(INVENTORY_ARCHIVE_URL, data=json.dumps(data), headers=headers)
    requests.delete(INVENTORY_URL + '/' + id)


# END Items FUNCTIONS



class InventoryCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='randomitem', help='Randomly selects an archived item.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomitem(self, ctx):
        """Returns a random item"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomitem"')
        await ctx.send(await getRandomItem())
        raise commands.BadArgument()

    @randomitem.error
    async def randomitem_error(self, ctx, error):
        logging.error('Command "randomitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='archiveditems')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archiveditems(self, ctx):
        """Returns all archived items"""
        sys.stdout.write(f'{ctx.message.author} ran command "archiveditems"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archiveditems"')
        items = await getItems(True)
        result = "```"
        for item in items:
            result = result + "{}: {}\n".format(item[0], item[2])
        result = result + "```"
        await ctx.send(result)

    @archiveditems.error
    async def archiveditems_error(self, ctx, error):
        logging.error('Command "getitems" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='editarchiveditem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editarchiveditem(self, ctx, itemNum, itemName):
        """Edit an archived item"""
        sys.stdout.write(f'{ctx.message.author} ran command "editarchiveditem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editarchiveditem"')
        recipient = ctx.message.mentions[0]
        await editItem(itemNum, itemName, recipient , True)
        await ctx.send("Edited archived item")

    @editarchiveditem.error
    async def editarchiveditem_error(self, ctx, error):
        logging.error('Command "editarchiveditem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='edititem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def edititem(self, ctx, itemNum, itemName):
        """edit an item"""
        sys.stdout.write(f'{ctx.message.author} ran command "edititem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "edititem"')
        recipient = ctx.message.mentions[0]
        await editItem(itemNum, itemName, recipient , False)
        await ctx.send("Edited item")

    @edititem.error
    async def edititem_error(self, ctx, error):
        logging.error('Command "edititem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='items')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def items(self, ctx):
        """return all items"""
        sys.stdout.write(f'{ctx.message.author} ran command "items"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "items"')
        items = await getItems(False)
        result = "```"
        for item in items:
            result = result + "{}: |{}| {}\n".format(item[0], item[1], item[2])
        result = result + "```"
        await ctx.send(result)

    @items.error
    async def items_error(self, ctx, error):
        logging.error('Command "items" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='item')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def item(self, ctx):
        """Return a specific item"""
        sys.stdout.write(f'{ctx.message.author} ran command "item"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "item"')
        item = ctx.message.content[len('item '):].strip()
        await ctx.send(await getItem(item, False))

    @item.error
    async def item_error(self, ctx, error):
        logging.error('Command "item" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteitem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deleteitem(self, ctx):
        """Delete a item"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteitem"')
        item = ctx.message.content[len('deleteitem '):]
        await deleteItem(item, False)
        await ctx.send("Deleted item")

    @deleteitem.error
    async def deleteitem_error(self, ctx, error):
        logging.error('Command "deleteitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteitems')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deleteitems(self, ctx):
        """Delete a items"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteitems"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteitems"')
        item = ctx.message.content[len('deleteitem '):]
        nums = item.split(' ')
        for num in nums:
            await deleteItem(num, False)
            await ctx.send("Deleted item")

    @deleteitems.error
    async def deleteitems_error(self, ctx, error):
        logging.error('Command "deleteitems" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deletearchiveditem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletearchiveditem(self, ctx):
        """Delete an archived item"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchiveditem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchiveditem"')
        item = ctx.message.content[len('deletearchiveditem '):].strip()
        await deleteItem(item, True)
        await ctx.send("Deleted archived item")

    @deletearchiveditem.error
    async def deletearchiveditem_error(self, ctx, error):
        logging.error('Command "deletearchiveditem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deletearchiveditem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletearchiveditem(self, ctx):
        """Deletes an archived item"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchiveditem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchiveditem"')
        items = ctx.message.content[len('deletearchiveditem '):].strip()
        nums = items.split(' ')
        for num in nums:
            await deleteItem(num, True)
            await ctx.send("Deleted archived item")

    @deletearchiveditem.error
    async def deletearchiveditem_error(self, ctx, error):
        logging.error('Command "deletearchiveditem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #TODO finish implementing lock
    @commands.command(pass_context=True, name='deleteallarchiveditems COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchiveditemscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchiveditemscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchiveditemscommit"')
        await deleteAllItems(True)
        await ctx.send("Deleted all archived items")

    @deleteallarchiveditemscommit.error
    async def deleteallarchiveditemscommit_error(self, ctx, error):
        logging.error('Command "deleteallarchiveditemscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteallarchiveditems')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchiveditems(self, ctx):
        """Delete all archived items"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchiveditems"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchiveditems"')
        await ctx.send("Are you sure you want to delete all archived items?\nType ```?deleteallarchiveditems COMMIT``` to continue")

    @deleteallarchiveditems.error
    async def deleteallarchiveditems_error(self, ctx, error):
        logging.error('Command "deleteallarchiveditemscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteallitems COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallitemscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallitemscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallitemscommit"')
        await deleteAllItems(False)
        await ctx.send("Deleted all items")

    @deleteallitemscommit.error
    async def deleteallitemscommit_error(self, ctx, error):
        logging.error('Command "deleteallitemscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteallitems')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallitems(self, ctx):
        """Delete all items"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallitems"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallitems"')
        await ctx.send("Are you sure you want to delete all items?\nType ```?deleteallitems COMMIT``` to continue")

    @deleteallitems.error
    async def deleteallitems_error(self, ctx, error):
        logging.error('Command "deleteallitems" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='newarchiveditem', aliases=['addarchiveditem'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newarchiveditem(self, ctx, item):
        """Create a new archived item"""
        sys.stdout.write(f'{ctx.message.author} ran command "newarchiveditem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newarchiveditem"')
        user = ctx.message.mentions[0]
        await addItem(str(user.id), item, True)
        await ctx.send("Added item {}".format(item))

    @newarchiveditem.error
    async def newarchiveditem_error(self, ctx, error):
        logging.error('Command "newarchiveditem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='giveroleitem', aliases=['giveitemtorole'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def giveroleitem(self, ctx, role, item):
        """Give an item to all members with a specific role on the server"""
        sys.stdout.write(f'{ctx.message.author} ran command "giveroleitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "giveroleitem"')
        for user in ctx.message.guild.members:
            if user.bot:
                continue
            for r in user.roles:
                if role == r.mention:
                    await addItem(str(user.id), item, False)
                    await ctx.send("Gave {} '{}'".format(user.name, item))

    @giveroleitem.error
    async def giveroleitem_error(self, ctx, error):
        logging.error('Command "giveroleitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='draw', aliases=['raffle'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def draw(self, ctx, item):
        """Picks a random member who owns an item"""
        sys.stdout.write(f'{ctx.message.author} ran command "draw"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "draw"')
        entries = []
        for i in await getItems(False):
            if i[2] == item:
                entries.append(i[1])
        winner = entries[random.randint(0, len(entries))]
        #I give up on trying to fetch the user by ID. This has taken too long.
        for user in ctx.message.guild.members:
            if user.id == winner:
              await ctx.send("Out of {} total entries and {} unique entries, {} wins!".format(len(entries), len(set(entries)), user.mention))

    @draw.error
    async def draw_error(self, ctx, error):
        logging.error('Command "draw" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='giveall', aliases=['giveallitem'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def giveall(self, ctx, item):
        """Give an item to all members on the server"""
        sys.stdout.write(f'{ctx.message.author} ran command "giveall"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "giveall"')
        for user in ctx.message.guild.members:
            if not user.bot:
                await addItem(str(user.id), item, False)
                await ctx.send("Gave {} '{}'".format(user.name, item))

    @giveall.error
    async def giveall_error(self, ctx, error):
        logging.error('Command "giveall" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='newitem', aliases=['additem'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newitem(self, ctx, item):
        """Create a new item"""
        sys.stdout.write(f'{ctx.message.author} ran command "newitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newitem"')
        user = ctx.message.mentions[0]
        await addItem(str(user.id), item, False)
        await ctx.send("Added item {}".format(item))

    @newitem.error
    async def newitem_error(self, ctx, error):
        logging.error('Command "neweitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='archiveitem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archiveitem(self, ctx):
        """Archive an item"""
        sys.stdout.write(f'{ctx.message.author} ran command "archiveitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archiveitem"')
        item = ctx.message.content[len('archiveitem '):].strip()
        await archiveItem(item)
        await ctx.send("Archived item " + item)

    @archiveitem.error
    async def archiveitem_error(self, ctx, error):
        logging.error('Command "archiveitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='item')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def item(self, ctx):
        """Return a specific item"""
        sys.stdout.write(f'{ctx.message.author} ran command "item"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "item"')
        item = ctx.message.content[len('item '):].strip()
        if len(item) == 0:
            await ctx.send("?item id               ?t id           Returns a specific item.")
        await ctx.send(await getItem(item, True))

    @item.error
    async def item_error(self, ctx, error):
        logging.error('Command "item" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='inventory', aliases=['inv'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def inventory(self, ctx):
        """Return your specific inventory"""
        sys.stdout.write(f'{ctx.message.author} ran command "inventory"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "inventory"')
        user = ""
        if ctx.message.content == "|inv" or ctx.message.content == "|inventory":
           user = ctx.message.author
        else:
           user = ctx.message.mentions[0]
        items = await getItems(False)
        result = "```"
        for item in items:
            userId = item[1]
            if userId == user.id:
                result = result + "{}: {}\n".format(item[0], item[2])
        result = result + "```"
        await ctx.send(result)

    @inventory.error
    async def inventory_error(self, ctx, error):
        logging.error('Command "inventory" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='giveitem')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def giveitem(self, ctx, itemId: str):
        """give a specific amount"""
        sys.stdout.write(f'{ctx.message.author} ran command "giveitem"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "giveitem"')
        recipient = ctx.message.mentions[0]
        item = await getItem(itemId, False)
        userId = int(item[1])
        if userId == ctx.message.author.id:
            await editItem(itemId, item[2], recipient.id, False)
            await ctx.send("Gifted {} to {}".format(item[2], recipient.mention))
        else:
            await ctx.send("You do not own this item")

    @giveitem.error
    async def giveitem_error(self, ctx, error):
        logging.error('Command "giveitem" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

def setup(bot):
    bot.add_cog(InventoryCog(bot))
