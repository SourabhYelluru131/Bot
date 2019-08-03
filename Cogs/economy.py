import discord
from discord.ext import commands
import pymongo
import random
import datetime
#import time
#import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from functools import partial
botid = 434285481841131520

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
ecodb = myclient["usereconomyinfodb"]
ecocol = ecodb["economy"]
shopdb = myclient["shopinfodb"]
shopcol = shopdb["shop"]
pickdb = myclient["pickinfodb"]
pickcol = pickdb["pick"]
cpm = [0,0,1,2,2,3,4,4,5]
cpp=[50,50,50,50,50,50,50,100,100,100,100,100,100,200,200,200,200,200,300,300,300,300,400,400,400,500,500,1000]
dailyamt = 100
bonusamt = 200

#================================================ Scheduling Jobs =================================================#
def reset_daily():
    query = {}
    doc = ecocol.find(query)
    for x in doc:
        if x["DailyBool"] == 0:
            new_value_streak = {"$set": {"Streak": 0}}
            query_streak = {"name": x["name"], "id": x["id"]}
            ecocol.update_one(query_streak, new_value_streak)  # Resets streak if daily reward is not collected
        else:
            print("Streak not Reset for {}".format(x["name"]))
        new_value_daily = {"$set": {"DailyBool": 0}}
        ecocol.update_many(query, new_value_daily)

def del_query_one(col,q):
    try:
        col.delete_one(q)
        print("..................................Deleted.........................")
    except:
        print("........................Did not delete!.........................")

def del_query_many(col,q):
    try:
        col.delete_many(q)
        print("..................................Deleted.........................")
    except:
        print("........................Did not delete!.........................")

def add_amount(user,guild,amount):
    print("{} , {} , {}".format(user.name, user.id, guild))
    query = {"name": user.name,"id":user.id,"guild":guild}
    print("add_amount has begun")
    doc = ecocol.find(query)
    if doc is None :
        print("No doc found")
    else:
        for x in doc:
            bal = x['balance']
            new_value = {"$set":{"balance": bal+amount}}
            ecocol.update_one(query,new_value)

def subtract_amount(user,guild,amount):
    query = {"name": user.name,"id":user.id,"guild":guild}
    doc = ecocol.find(query)
    for x in doc:
        bal = x['balance']
        new_value = {"$set": {"balance": bal - amount}}
        ecocol.update_one(query, new_value)

def add_item(guild,name,price,desc):
    query = {"Guild":guild,"Item": name, "Price": price, "description": desc}
    shopcol.insert_one(query)

def remove_item(guild,name):
    query = {"Guild":guild,"Item": name}
    del_query_one(shopcol,query)

def create_pick_embed(amount,planter):      #takes in planter name ONLY
    pickembed = discord.Embed(title="{} planted some money!".format(planter), description="Total amount:{}".format(amount), colour=discord.Colour.green())
    pickembed.set_author(name=planter,
                             icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
    pickembed.add_field(name="\u200b", value="Type '.pick' to take the planted money. The first gets the money", inline=True)
    return pickembed

class Economy(commands.Cog):
    def __init__(self,bot):
        self.client = bot



    async def random_plant(self):
        query = {}
        res = pickcol.find(query)
        for x in res:
            amount = random.choice(cpp)
            guild = x["guild_id"]
            channel = x["pickchannel_id"]
            msgguild = self.bot.get_guild(guild)
            msgchan = msgguild.get_channel(channel)
            res_amount = x["pickamount"]
            res_amount += amount
            embed = create_pick_embed(amount, "Someone")
            msg = await msgchan.send(embed=embed)
            queryz = {"guild_id":guild}
            new_value = {"$set": {"pickamount": res_amount, "pickembed_id": msg.id}}
            pickcol.update_one(queryz, new_value)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        name = member.name
        mid = member.id
        dictit = {"name":name,"id":mid,"guild":member.guild.id,"balance":0,"ItemsOwned":[],"DailyBool":0,"Streak":0}
        ecocol.insert_one(dictit)

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild is not None:
            author_id = message.author.id
            query = {"id":author_id,"guild":message.guild.id}
            doc = ecocol.find(query)
            nor = doc.count()
            if message.author.id != botid:
                if nor != 0:
                    try:
                        print("account found ")
                        add_amount(message.author,message.guild.id,random.choice(cpm))
                    except Exception as errorc:
                        print(errorc)
                        print("It went wrong here in line 84!!")
                else:
                    print("account not found :(")
                    newdict = {"name":message.author.name,"id":message.author.id,"guild":message.guild.id,"balance":random.choice(cpm),"ItemsOwned":[],"DailyBool":0,"Streak":0}
                    ecocol.insert_one(newdict)
            #if message.content.startswith('.pick'):
             #   await message.delete()

    @commands.command(aliases=['$,balance,cash'])
    async def bal(self,ctx):
        query = {"name":ctx.author.name,"id":ctx.author.id,"guild":ctx.guild.id}
        baldoc = ecocol.find(query)
        nor = baldoc.count()
        if nor == 0:
            newdict = {"name": ctx.author.name, "id": ctx.author.id, "guild": ctx.guild.id, "balance": random.choice(cpm),"ItemsOwned":[],"DailyBool":0,"Streak":0}
            ecocol.insert_one(newdict)
        else:
            print("It's going to else... implies baldoc is found..... Printing x in baldoc")
            for x in baldoc:
                bal = x["balance"]
                balance_embed = discord.Embed(title="Balance", description="Total amount",colour=discord.Colour.green())
                balance_embed.set_author(name=ctx.author.name,icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                balance_embed.add_field(name="\u200b",value=bal,inline=True)
                await ctx.send(embed=balance_embed)

    @commands.command()
    async def give(self,ctx, user: discord.User, amount : int):
        add_amount(user,ctx.guild.id,amount)
        subtract_amount(ctx.author,ctx.guild.id,amount)
        give_embed = discord.Embed(title="Pay", description="\u200b", colour=discord.Colour.red())
        give_embed.set_author(name=ctx.author.name,
                                 icon_url=user.avatar_url)
        give_embed.add_field(name="\u200b", value="{} paid {} {} coins".format(ctx.author,user,int), inline=True)
        await ctx.send(embed=give_embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset(self,ctx):
        try:
            ecocol.update_many({"guild":ctx.guild.id},{"$set":{"balance":0,"ItemsOwned":[]}})
            print("Done!")
        except:
            await ctx.send("could not reset")
            print("Could not reset")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_item(self,ctx,name:str,price:int,desc:str):
        add_item(ctx.guild.id,name,price,desc)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remove_item(self,ctx,name:str):
        remove_item(ctx.guild.id,name)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def displayshop(self,ctx):
        shop_embed = discord.Embed(title="Shop", description="\u200b", colour=discord.Colour.dark_orange())
        shop_embed.set_author(name=ctx.guild.name,
                              icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
        shop_embed.add_field(name="Item                                                                      Price", value="\u200b", inline=True)
        dicti = {"Guild":ctx.guild.id}
        docshop = shopcol.find(dicti)
        noofres = docshop.count()
        if noofres !=0 :
            list_of_items = []
            i = 1
            for x in docshop:
                shop_embed.add_field(name="{}.{}                                                                      {}".format(i,x["Item"],x["Price"]), value="{}".format(x["description"]), inline=True)
                i += 1
                list_of_items.append(x["Item"])
            await ctx.send(embed=shop_embed)
            insdic = {"shop_guild":ctx.guild.id,"ListOfItems":list_of_items}
            shopcol.insert_one(insdic)
        else:
            print("Shop not found")

    @commands.command()
    async def buy(self,ctx,opt :int):
        firstquery = {"shop_guild":ctx.guild.id}
        doc = shopcol.find(firstquery)
        list_of_items = doc["ListOfItems"]
        buyquery = {"Guild":ctx.guild.id,"Item":list_of_items[opt-1]}
        newdoc = shopcol.find(buyquery)
        cost = newdoc["Price"]                               #Finding cost for the item
        subtract_amount(ctx.author,ctx.guild.id,cost)
        newquery = {"name":ctx.author.name,"id":ctx.author.id,"guild":ctx.guild.id}
        docs = ecocol.find(newquery)
        originallist = docs["ItemsOwned"]
        originallist.append(list_of_items[opt-1])
        new_value = {"$set": {"ItemsOwned": originallist}}
        ecocol.update_one(newquery, new_value)              #Adding item to User's profile

    @commands.command()
    async def daily(self,ctx):
        query = {"name": ctx.author.name, "id": ctx.author.id, "guild": ctx.guild.id}
        mdoc = ecocol.find(query)
        for x in mdoc:
            streak = x["Streak"]
            boola = x["DailyBool"]
            if not boola :
                try:
                    add_amount(ctx.author,ctx.guild.id,dailyamt)
                    await ctx.send("Collected your Daily Reward for today!!")
                    print("added daily amount")
                    if streak < 4:
                        new_streak = streak+ 1
                        print("incremented streak to {}".format(new_streak))
                    elif streak == 4:
                        new_streak = 0
                        add_amount(ctx.author,ctx.guild.id,bonusamt)            #Gives bonus on collecting daily for 5 consecutive days
                        await ctx.send("You've gained a bonus amount of {} for collecting daily reward 5 days in a row".format(bonusamt))
                    new_value = {"$set":{"DailyBool":1,"Streak":new_streak}}
                    ecocol.update_one(query,new_value)               #Updating that user has collected the day's reward already
                except:
                    print("Unsuccessful daily reward collection")
            else:
                tomorrow = datetime.datetime.replace(datetime.datetime.now()+datetime.timedelta(days=1),hour = 0, minute=0, second=0)
                delta = tomorrow - datetime.datetime.now()
                await ctx.send("You have {} until the next reward".format(delta))

    #Temporary command until it resets properly
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetdaily(self,ctx):
        try:
            reset_daily()
            await ctx.send("reset succesfully!!")
        except Exception as errorb:
            print(errorb)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mainchannel(self,ctx):
        querymain={"guild_id":ctx.guild.id}
        entry={"guild_id":ctx.guild.id,"guild_name":ctx.guild.name,"pickchannel_id":ctx.channel.id,"pickamount":0,"pickembed_id":0}
        find = pickcol.find(querymain)
        nor = find.count()
        if nor == 0:
            try:
                pickcol.insert_one(entry)
                await ctx.send("Main channel has been set!")
            except Exception as errora:
                print("error:{}".format(errora))
        else:
            await ctx.send("There exists another main channel. Do you want to replace it with this? Reply with Y/N")
            @commands.Cog.listener()
            async def on_message(message):
                author = message.author
                if ctx.author==author & message.content == "Y":
                    try:
                        del_query_one(pickcol,querymain)
                        pickcol.insert_one(entry)
                        await ctx.send("The main channel has been replaced with the old one!")
                    except Exception as erroro:
                        print("error:{}".format(erroro))
                else:
                    await ctx.send("Ok. The channel will not be replaced.")

    @commands.command()
    async def plant(self,ctx,amount:int):
        query = {"guild_id":ctx.guild.id}
        res = pickcol.find(query)
        for x in res:
            if x["pickchannel_id"]==ctx.channel.id:
                subtract_amount(ctx.author,ctx.guild.id,amount)
                embed = create_pick_embed(amount,ctx.author.name)
                res_amount = x["pickamount"]
                res_amount += amount
                msg = await ctx.send(embed= embed)
                new_value ={"$set":{"pickamount":res_amount,"pickembed_id":msg.id}}
                pickcol.update_one(query,new_value)
                await ctx.message.delete()

    @commands.command()
    async def pick(self,ctx):
        query={"guild_id":ctx.guild.id}
        res = pickcol.find(query)
        for x in res:
            amount = x["pickamount"]
            if x["pickchannel_id"]==ctx.channel.id:
                add_amount(ctx.author,ctx.guild.id,amount)
                new_value={"$set":{"pickamount":0}}
                pickcol.update_one(query,new_value)
                embed = x["pickembed_id"]
                embedmsg = await ctx.channel.fetch_message(embed)
                await ctx.message.delete()
                await embedmsg.delete()

def setup(bot):
    bot.add_cog(Economy(bot))
    botz = Economy(bot)
    randomplantfunc = partial(await botz.random_plant())

    try:
        scheduler = AsyncIOScheduler()
        scheduler.start()
        scheduler.add_job(reset_daily, trigger="cron", hour=0, minute=0, id="reset", replace_existing=True)
        scheduler.add_job(randomplantfunc, trigger="interval", minutes=1, jitter=15)
    except Exception as errorno:
        print("errorno : {}".format(errorno))