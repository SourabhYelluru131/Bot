import discord
from discord.ext import commands
from datetime import date, time,datetime,timedelta
import random
import asyncio
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
raffledb = myclient["raffleinfodb"]
rafflecol = raffledb["raffle"]
admin_msg = 'You need "Administrator" permissions to use this command!!'
botid = 434285481841131520

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

class Raffle(commands.Cog):
    def __init__(self,bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, pay):
        if pay.user_id !=botid:
            guild = self.client.get_guild(pay.guild_id)
            query = {"Guildid":guild.id}
            doc = rafflecol.find(query)
            for x in doc:
                msgid=x["msgid"]
                users=x["users"]
                if pay.message_id != msgid:  # Checks for the reaction message
                    return
                if str(pay.emoji) != "🎉" :   #Checks for the  🎉 reaction"U+1F389":
                    return
                try:
                    user = self.client.get_user(pay.user_id)
                    users.append(dict(user))
                    new_value={"$set":{"users":users}}
                    rafflecol.update_one(query,new_value)
                except Exception as error:
                    print("Error:{}".format(error))

    @commands.Cog.listener()
    async def on_reaction_remove(self,pay):
        guild = self.client.get_guild(pay.guild_id)
        query = {"Guildid": guild.id}
        doc = rafflecol.find(query)
        for x in doc:
            msgid = x["msgid"]
            users = x["users"]
            if pay.message_id != msgid:  # Checks for the reaction message
                return
            if pay.emoji != "🎉":  # Checks for the  🎉 reaction
                return
            try:
                user = self.bot.get_user(pay.user_id)
                users.remove(user)
            except Exception as error:
                print(error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def raffle(self,ctx, in_prize: str, time_period: str):
        tp = int(time_period)
        message_time = datetime.utcnow()
        raffle_end_time = message_time + timedelta(seconds=tp)
        time_until_end = raffle_end_time - datetime.utcnow()
        hours, remainder = divmod(int(time_period), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.message.delete()  # Deletes the command message
        async with ctx.channel.typing():  # Send typing status for the bot
            entry = {"Guildid":ctx.guild.id,"channelid":ctx.channel.id,"users":[]}
            rafflecol.insert_one(entry)
            my_embed = discord.Embed(title="🎉 GIVEAWAY/RAFFLE !! 🎉", colour=0x00ff00)
            my_embed.add_field(name="**Giveaway/Raffle event started**",
                                   value="React to this with 🎉 for a chance to win")
            my_embed.add_field(name="**Prize:**", value=in_prize)
            my_embed.add_field(name="Time left", value=f"```{days}d, {hours}h, {minutes}m, {seconds}s```")
            msg = await ctx.send(embed=my_embed)
            print(msg.id)
            new_value = {"$set":{"msgid":msg.id}}
            rafflecol.update_one(entry,new_value)
            await asyncio.sleep(2)
            await msg.add_reaction("🎉")  # Adds 🎉 to the bot's embed
        while time_until_end:
            hours, remainder = divmod(tp, 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            my_new_embed = discord.Embed(title="🎉 GIVEAWAY/RAFFLE !! 🎉", colour=0x00ff00)
            my_new_embed.add_field(name="**Giveaway/Raffle event started**",
                                       value="React to this with 🎉 for a chance to win")
            my_new_embed.add_field(name="**Prize:**", value=in_prize)
            my_new_embed.add_field(name="**Time left.**",
                                       value=f"You have ```{days}d, {hours}h, {minutes}m, {seconds}s``` left to enter the giveaway/raffle")
            await msg.edit(embed=my_new_embed)
            await asyncio.sleep(5)
            tp -= 5
            time_until_end = time_until_end - timedelta(seconds=5)
        query={"Guildid":ctx.guild.id}
        doc = rafflecol.find(query)
        for x in doc:
            users = x["users"]
            winner = random.choice(users)  # Selects a random user
            winnerac = self.client.get_user(winner["User id"])
            x = 1
            while x > 0:
                if winner.id != botid:
                    break  # Makes sure that the bot is never the winner
                else:
                    winner = random.choice(users)
                    x = x + 1
                    if x > 20:
                        await ctx.channel.send("No winner , as no one reacted . Sorry!")  # If no one reacts
                        return
            raffle_end_embed = discord.Embed(title="🎉 GIVEAWAY/RAFFLE  🎉 ", colour=0x00ff00)
            raffle_end_embed.add_field(name="RESULTS : ", value="Thank you for participating, better luck next time!")
            raffle_end_embed.add_field(name="Winner:", value=winnerac.mention)
            await msg.edit(content=" 🎉 **GIVEAWAY/RAFFLE ENDED** 🎉 ", embed=raffle_end_embed)
            await ctx.channel.send(
                'Congratulations, {} has won the raffle.'.format(winnerac.mention))  # Mentions the winner
        rafflecol.del_query_one(rafflecol,query)

def setup(bot):
    bot.add_cog(Raffle(bot))