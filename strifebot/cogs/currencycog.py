import requests
import sys
import logging
import xmltodict
import random
import datetime
import json
from discord.ext import commands

BANK_URL = 'http://localhost:5000/accounts'
BANK_ARCHIVE_URL = 'http://localhost:5000/archivedaccounts'

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


#returns a codeblock containing all archived or regular accounts
async def getAccounts(archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL)
    else:
        r = requests.get(BANK_URL)
    accounts = []
    chunk = "```"
    print(r.json)
    for account in r.json():
        if (len(chunk) > 1800):
            chunk += "```"
            accounts.append(chunk)
            chunk = "```"
        chunk += "{}: {} | {}\n".format(account['id'], account['USERID'], account['BALANCE'])
    chunk += "```"
    accounts.append(chunk)
    if accounts[0] == "``````":
        if archived:
            accounts = "There are currently no archived accounts"
        else:
            accounts = "There are currently no regular accounts"
    return accounts

#returns a the accountnumber for a given userid
async def getAccountNumByUserId(userId, archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL)
    else:
        r = requests.get(BANK_URL)
    for account in r.json():
        if int(account['USERID']) == int(userId):
            return account['id']
    return None


#returns a codeblock containing all archived or regular accounts
async def accountIsRegistered(userId, archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL)
    else:
        r = requests.get(BANK_URL)
    for account in r.json():
        if int(account['USERID']) == int(userId):
            return True
    return False



#returns a codeblock containing a specific archived or regular account
async def getAccount(id, archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(BANK_URL + '/' + id)
    accounts = "```"
    for account in r.json():
        accounts += "{}: {} | {}\n".format(account['id'], account['USERID'], account['BALANCE'])
    accounts += "```"
    if accounts == "``````":
        if archived:
            accounts = "Cannot find archived account with id " + id
        else:
            accounts = "Cannot find regular account with id " + id
    return accounts


#returns a user ID for a specific archived or regular account
async def getUserId(id, archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(BANK_URL + '/' + id)
    for account in r.json():
        return int(account['USERID'])

#returns a user ID for a specific archived or regular account
async def getAccountBalance(id, archived):
    if archived:
        r = requests.get(BANK_ARCHIVE_URL + '/' + id)
    else:
        r = requests.get(BANK_URL + '/' + id)
    for account in r.json():
        return int(account['BALANCE'])

#deletes a specific archived or regular account
async def deleteAccount(id, archived):
    if archived:
        r = requests.delete(BANK_ARCHIVE_URL + '/' + id)
    else:
        r = requests.delete(BANK_URL + '/' + id)
    return



#deletes a all archived or regular accounts
async def deleteAllAccounts(archived):
    if archived:
        r = requests.delete(BANK_ARCHIVE_URL)
    else:
        r = requests.delete(BANK_URL)
    return



#returns a random regular account
async def getRandomAccount():
    r = requests.get(BANK_URL).json()
    account = r[random.randint(0, len(r))]
    return "***Account:***  {} | {}".format(account['USERID'], account['BALANCE'])



#adds a new archived, or regular account
async def addAccount(account, balance, archived):
    data = {'USERID': account, 'BALANCE': balance}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
        requests.post(BANK_ARCHIVE_URL, data=json.dumps(data), headers=headers)
    else:
        requests.post(BANK_URL, data=json.dumps(data), headers=headers)
    return



#edits an archived or regular account
#data format should be "id newAccountText, newDisciplineText"
async def editAccount(accountId, balance, userId, archived):
    data = {'USERID': userId, 'BALANCE': balance}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if archived:
                             #url + accountID
        requests.put(BANK_ARCHIVE_URL + '/' + accountId, data=json.dumps(data), headers=headers)
    else:
        requests.put(BANK_URL + '/' + accountId, data=json.dumps(data), headers=headers)



#archive regular account by accountID
async def archiveAccount(id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(BANK_URL + "/" + id)
    data = {}
    for t in r.json():
        data = {'USERID': t['USERID'], 'BALANCE': t['BALANCE']}
    requests.post(BANK_ARCHIVE_URL, data=json.dumps(data), headers=headers)
    requests.delete(BANK_URL + '/' + id)


# END Accounts FUNCTIONS



class AccountCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='randomaccount', help='Randomly selects an archived account.')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def randomaccount(self, ctx):
        """Returns a random account"""
        sys.stdout.write(f'{ctx.message.author} ran command "randomaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "randomaccount"')
        await ctx.send(await getRandomAccount())

    @randomaccount.error
    async def randomaccount_error(self, ctx, error):
        logging.error('Command "randomaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archivedaccounts')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archivedaccounts(self, ctx):
        """Returns all archived accounts"""
        sys.stdout.write(f'{ctx.message.author} ran command "archivedaccounts"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archivedaccounts"')
        accounts = await getAccounts(True)
        for account in accounts:
            if account=='T':
                await ctx.send('No Archived accounts')
                break
            else:
                await ctx.send(account)

    @archivedaccounts.error
    async def archivedaccounts_error(self, ctx, error):
        logging.error('Command "archivedaccounts" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='editarchivedaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editarchivedaccount(self, ctx):
        """Edit an archived account"""
        sys.stdout.write(f'{ctx.message.author} ran command "editarchivedaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editarchivedaccount"')
        din = ctx.message.content[len('editarchivedaccount '):].strip()
        accountId = din.split(' ', 1)[0]
        balance = din.split(' ', 1)[1]
        userId = await getUserId(accountId, archived)
        await editAccount(accountId, balance, userId , True)
        await ctx.send("Edited archived account")

    @editarchivedaccount.error
    async def editarchivedaccount_error(self, ctx, error):
        logging.error('Command "editarchivedaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________



    @commands.command(pass_context=True, name='editaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def editaccount(self, ctx):
        """edit an account"""
        sys.stdout.write(f'{ctx.message.author} ran command "editaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "editaccount"')
        din = ctx.message.content[len('editaccount '):].strip()
        accountId = din.split(' ', 1)[0]
        balance = din.split(' ', 1)[1]
        userId = await getUserId(accountId, archived)
        await editAccount(accountId, balance, userId , False)
        await ctx.send("Edited account")

    @editaccount.error
    async def editaccount_error(self, ctx, error):
        logging.error('Command "editaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='accounts')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def accounts(self, ctx):
        """return all accounts"""
        sys.stdout.write(f'{ctx.message.author} ran command "accounts"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "accounts"')
        accounts = await getAccounts(False)
        for account in accounts:
            if account=='T':
                await ctx.send('No accounts')
                break
            else:
                await ctx.send(account)

    @accounts.error
    async def accounts_error(self, ctx, error):
        logging.error('Command "accounts" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='account')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def account(self, ctx):
        """Return a specific account"""
        sys.stdout.write(f'{ctx.message.author} ran command "account"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "account"')
        account = ctx.message.content[len('account '):].strip()
        await ctx.send(await getAccount(account, False))

    @account.error
    async def account_error(self, ctx, error):
        logging.error('Command "account" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='deleteaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deleteaccount(self, ctx):
        """Delete a account"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteaccount"')
        account = ctx.message.content[len('deleteaccount '):]
        nums = account.split(' ')
        for num in nums:
            await deleteAccount(num, False)
            await ctx.send("Deleted account")

    @deleteaccount.error
    async def deleteaccount_error(self, ctx, error):
        logging.error('Command "deleteaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deletearchivedaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def deletearchivedaccount(self, ctx):
        """Delete an archived account"""
        sys.stdout.write(f'{ctx.message.author} ran command "deletearchivedaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deletearchivedaccount"')
        account = ctx.message.content[len('deletearchivedaccount '):].strip()
        nums = account.split(' ')
        for num in nums:
            await deleteAccount(num, True)
            await ctx.send("Deleted archived account")

    @deletearchivedaccount.error
    async def deletearchivedaccount_error(self, ctx, error):
        logging.error('Command "deletearchivedaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    #TODO finish implementing lock
    @commands.command(pass_context=True, name='deleteallarchivedaccounts COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedaccountscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedaccountscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedaccountscommit"')
        await deleteAllAccounts(True)
        await ctx.send("Deleted all archived accounts")

    @deleteallarchivedaccountscommit.error
    async def deleteallarchivedaccountscommit_error(self, ctx, error):
        logging.error('Command "deleteallarchivedaccountscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallarchivedaccounts')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallarchivedaccounts(self, ctx):
        """Delete all archived accounts"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallarchivedaccounts"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallarchivedaccounts"')
        await ctx.send("Are you sure you want to delete all archived accounts?\nType ```?deleteallarchivedaccounts COMMIT``` to continue")

    @deleteallarchivedaccounts.error
    async def deleteallarchivedaccounts_error(self, ctx, error):
        logging.error('Command "deleteallarchivedaccounts" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallaccounts COMMIT')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallaccountscommit(self, ctx):
        """FINAL WARNING"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallaccountscommit"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallaccountscommit"')
        await deleteAllAccounts(False)
        await ctx.send("Deleted all accounts")

    @deleteallaccountscommit.error
    async def deleteallaccountscommit_error(self, ctx, error):
        logging.error('Command "deleteallaccountscommit" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='deleteallaccounts')
    @commands.has_any_role(owner_roleid, admin_roleid, cbbb)
    async def deleteallaccounts(self, ctx):
        """Delete all accounts"""
        sys.stdout.write(f'{ctx.message.author} ran command "deleteallaccounts"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "deleteallaccounts"')
        await ctx.send("Are you sure you want to delete all accounts?\nType ```?deleteallaccounts COMMIT``` to continue")

    @deleteallaccounts.error
    async def deleteallaccounts_error(self, ctx, error):
        logging.error('Command "deleteallaccounts" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newarchivedaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def newarchivedaccount(self, ctx):
        """Create a new archived account"""
        sys.stdout.write(f'{ctx.message.author} ran command "newarchivedaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newarchivedaccount"')
        account = ctx.message.content[len('|newarchivedaccount '):].strip()
        await addAccount(account, 0, True)
        await ctx.send("Added account {}".format(account))

    @newarchivedaccount.error
    async def newarchivedaccount_error(self, ctx, error):
        logging.error('Command "newarchivedaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='newaccount')
    async def newaccount(self, ctx, userId):
        """Create a new account"""
        sys.stdout.write(f'{ctx.message.author} ran command "newaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "newaccount"')
        if not await accountIsRegistered(userId, False):
            await addAccount(userId, 0, False)
            await ctx.send("Added account {}".format(userId))
        else:
            await ctx.send("Account already registered")

    @newaccount.error
    async def newaccount_error(self, ctx, error):
        logging.error('Command "newaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='openaccount')
    async def openaccount(self, ctx):
        """Create a new account"""
        sys.stdout.write(f'{ctx.message.author} ran command "openaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "openaccount"')
        userId = ctx.message.author.id
        if not await accountIsRegistered(userId, False):
            await addAccount(userId, 0, False)
            await ctx.send("Added account {}".format(userId))
        else:
            await ctx.send("Account already registered")

    @openaccount.error
    async def openaccount_error(self, ctx, error):
        logging.error('Command "openaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________


    @commands.command(pass_context=True, name='archiveaccount')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def archiveaccount(self, ctx):
        """Archive a account"""
        sys.stdout.write(f'{ctx.message.author} ran command "archiveaccount"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "archiveaccount"')
        account = ctx.message.content[len('archiveaccount '):].strip()
        await archiveAccount(account)
        await ctx.send("Archived account " + account)

    @archiveaccount.error
    async def archiveaccount_error(self, ctx, error):
        logging.error('Command "archiveaccount" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='account')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def account(self, ctx):
        """Return a specific account"""
        sys.stdout.write(f'{ctx.message.author} ran command "account"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "account"')
        account = ctx.message.content[len('account '):].strip()
        if len(account) == 0:
            await ctx.send("?account id               ?t id           Returns a specific account.")
        await ctx.send(await getAccount(account, True))

    @account.error
    async def account_error(self, ctx, error):
        logging.error('Command "account" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='balance', aliases=['bal'])
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def balance(self, ctx):
        """Return a specific account"""
        sys.stdout.write(f'{ctx.message.author} ran command "balance"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "balance"')
        user = ""
        if ctx.message.content == "|bal" or ctx.message.content == "|balance":
           user = ctx.message.author
        else:
           user = ctx.message.mentions[0]
        if await accountIsRegistered(user.id, False):
            await ctx.send(await getAccount(str(await getAccountNumByUserId(user.id, False)), False))
        else:
            await ctx.send("Not registered")

    @balance.error
    async def balance_error(self, ctx, error):
        logging.error('Command "balance" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='answer')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def answer(self, ctx, answer: float):
        """Answer a question to manually mine arbitrary coin"""
        sys.stdout.write(f'{ctx.message.author} ran command "answer"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "answer"')
        answered = False
        async for message in ctx.message.channel.history(limit=20):
            if message.author == self.bot.user and "Correct" in message.content:
                await ctx.send("Question already answered")
                answered = True
                break
            if message.author == self.bot.user and message.content[0:len('Question:')] == "Question:":
                question = message.content.split(":")[1].strip()
                reward = int(message.content.split(":")[3].strip())
                if answer == eval(question):
                    await ctx.send("Correct! Reward: {}".format(reward))
                    if await accountIsRegistered(ctx.message.author.id, False):
                        answererAccId = await getAccountNumByUserId(ctx.message.author.id, False)
                        balance = await getAccountBalance(str(answererAccId), False)
                        await editAccount(str(answererAccId), balance + reward, ctx.message.author.id , False)
                    else:
                       await ctx.send("You are not registered")
                else:
                    await ctx.send("Incorrect")
                answered = True
                break
        if not answered:
            await ctx.send("can't find question (must be within 20 msgs)")

    @answer.error
    async def answer_error(self, ctx, error):
        logging.error('Command "answer" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='question')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def question(self, ctx):
        """Posts a question for mining arbitrary coin"""
        sys.stdout.write(f'{ctx.message.author} ran command "question"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "question"')
        reward = 0
        nums = range(1, 11)
        ops = random.choice("+-*/")
        if ops == "+":
            reward = 1
        if ops == "-":
            reward = 2
        if ops == "*":
            reward = 3
        if ops == "/":
            reward = 5
        a, b = random.choices(nums, k = 2)
        while ops == "/" and (a % b != 0 or a <= b):
            a, b = random.choices(nums, k=2)
        while ops == "-" and a<b:
            a, b = random.choices(nums, k=2)
        await ctx.send("Question: {} {} {} : Reward: {}".format(a, ops, b, reward))

    @question.error
    async def question_error(self, ctx, error):
        logging.error('Command "question" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

    @commands.command(pass_context=True, name='give')
    @commands.has_any_role(owner_roleid, admin_roleid, seniorMod_roleid, moderator_roleid, cbbb)
    async def give(self, ctx, amount: int):
        """give a specific amount"""
        sys.stdout.write(f'{ctx.message.author} ran command "give"\n')
        sys.stdout.flush()
        logging.info(f'{ctx.message.author} ran command "give"')
        recipientId = ctx.message.mentions[0].id
        if await accountIsRegistered(ctx.message.author.id, False):
            if await accountIsRegistered(recipientId, False):
                balance = await getAccountBalance(str(await getAccountNumByUserId(ctx.message.author.id, False)), False)
                if balance > amount:
                    balance2 = await getAccountBalance(str(await getAccountNumByUserId(recipientId, False)), False)
                    giver = await getAccountNumByUserId(ctx.message.author.id, False)
                    recipient = await getAccountNumByUserId(recipientId, False)
                    await editAccount(str(giver), balance - amount, ctx.message.author.id , False)
                    await editAccount(str(recipient), balance2 + amount, recipientId , False)
                    await ctx.send("Gifted arbitrary tokens")
                print(balance)
            else:
                await ctx.send("Recipient is not registered")
        else:
            await ctx.send("You are not registered")

    @give.error
    async def give_error(self, ctx, error):
        logging.error('Command "give" failed due to the following error:')
        logging.error(error)
        await ctx.send('Error processing that request')

    #__________________________________________________

def setup(bot):
    bot.add_cog(AccountCog(bot))
