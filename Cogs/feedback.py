import discord
from discord.ext import commands
import pymongo
import asyncio

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
chdb = myclient["channelinfodb"]
chcol = chdb["channels"]
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

class Feedback(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,pay):
        if pay.user_id != botid:
            myqueryl = {"reactionmsgbool": "yes", "guild": pay.guild_id}
            mydocl = chcol.find(myqueryl)
            for abd in mydocl:
                reactionmessageid = abd['feedbackembedid']
                guildname = abd['guildname']
                if pay.message_id == reactionmessageid:
                    if str(pay.emoji) == "✉":
                        chdict2 = {"reacted": "yes", "userid": pay.user_id, "respguild": pay.guild_id}
                        chcol.insert_one(chdict2)
                        dmembed = discord.Embed(title="Suggestion",
                                                description="You have requested a suggest for {} community.Please enter your message below and when you're done , it shall be delivered. ".format(
                                                    guildname),
                                                colour=discord.Colour.dark_gold())
                        # dmembed.set_image(file=discord.File(ctx.guild.icon))
                        dmembed.set_author(name="Mythicley",
                                           icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                        myquery = {"reacted": "yes", "userid": pay.user_id}
                        mdoc = chcol.find(myquery)
                        for asx in mdoc:
                            print("React from {}".format(asx["respguild"]))
                            user = self.bot.get_user(pay.user_id)
                            print("Reaction was from {}".format(user.display_name))
                        user = self.bot.get_user(pay.user_id)
                        dmembedmsg = await user.send(embed=dmembed)
                        channel = self.bot.get_channel(pay.channel_id)
                        message = await channel.fetch_message(pay.message_id)
                        await message.remove_reaction(emoji="✉", member=user)
                        myquery = {"reacted": "yes"}
                        new_entry = {"$set": {"dm_id": dmembedmsg.channel.id}}
                        chcol.update_one(myquery, new_entry)
                        print("updated dm_id!")

                        def check(message):
                            myquery = {"reacted": "yes"}
                            mydoc = chcol.find(myquery)
                            for asd in mydoc:
                                print("asd: {}".format(asd))
                                userdmid = asd['dm_id']
                                if userdmid == message.channel.id:
                                    return True
                                else:
                                    return False

                        try:
                            await self.bot.wait_for('message', timeout=120.0, check=check)
                        except asyncio.TimeoutError:
                            await user.send('Feedback timed out! React again to apply for a suggestion')
                            myquery = {"reacted": "yes"}
                            del_query_many(chcol, myquery)

    count = 0
    @commands.Cog.listener()
    async def on_message(self,message):
        global count
        count = 0
        if message.author.id == botid:
            return
        else:
            if message.guild is None and count == 0:
                print("yeah!")
                count += 1
                myquery = {"reacted": "yes"}
                mydoc = chcol.find(myquery)
                for x in mydoc:
                    print("message received in DM!")
                    print(x)
                    userdmid = x['dm_id']
                    guildid = x['respguild']
                    sugg = message.content
                    print("")
                    print("Suggestion Received!")
                    print("{}:".format(message.author))
                    print(sugg)
                    print("")
                    myqueryn = {"chtype": "feedback", "guild": guildid}
                    mydocrn = chcol.find(myqueryn)
                    for z in mydocrn:
                        y = z['chid']
                        xyz = self.bot.get_channel(y)
                        await xyz.send("{} is sending a feedback!".format(message.author.mention))
                        finfeedembed = discord.Embed(title="{} has a feedback!".format(message.author.name),
                                                     description=sugg,
                                                     colour=discord.Colour.blue())
                        await xyz.send(embed=finfeedembed)
                        confembed = discord.Embed(title="Message sent!",
                                                  description="Thank you for providing us with your valuable suggestion! Your message has been sent and will be read shortly!",
                                                  colour=discord.Colour.blurple())
                        confembedsend = self.bot.get_channel(userdmid)
                        await confembedsend.send(embed=confembed)
                        print("Going to delete!")
                myquerylast = {"reacted": "yes"}
                del_query_many(chcol, myquerylast)
            count = 0
    #1
    @commands.command()
    async def setfeedbackchannel(self,ctx):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.message.delete()
            feedid = ctx.channel.id
            mquery = {"guild": ctx.guild.id, "chtype": "feedback", "chid": feedid}
            mdoc = chcol.find(mquery)
            if mdoc:
                print("previous instance found!!")
                del_query_many(chcol, mquery)
                chdict = {"guild": ctx.guild.id, "chtype": "feedback", "chid": feedid}
                chcol.insert_one(chdict)
                await ctx.send("Done! This channel will be used for sending feedbacks! Set appropriate permissions!")
            elif not mdoc:
                print("No previous instance")
                chdict = {"guild": ctx.guild.id, "chtype": "feedback", "chid": feedid}
                chcol.insert_one(chdict)
                await ctx.send("Done! This channel will be used for sending feedbacks! Set appropriate permissions!")

    #2
    @commands.command()
    async def setwelcomechannel(self,ctx):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.message.delete()
            welchid = ctx.channel.id
            mquery = {"guild": ctx.guild.id, "chtype": "welcome", "chid": welchid}
            mdoc = chcol.find(mquery)
            doclist = list(mdoc)
            mquery2 = {"guild": ctx.guild.id, "reactionmsgbool": "yes"}
            if doclist:
                print("previous instance found!!")
                del_query_one(chcol, mquery)
                del_query_many(chcol, mquery2)
            mdoc = chcol.find(mquery)
            doclist = list(mdoc)
            if not doclist:
                print("previous instance not found!")
                chdict = {"guild": ctx.guild.id, "chtype": "welcome", "chid": welchid}
                chcol.insert_one(chdict)
                async with ctx.channel.typing():
                    welcembed = discord.Embed(title="Welcome", description="Welcome to {}".format(ctx.guild.name),
                                              colour=discord.Colour.red())
                    # welcembed.set_image( file = discord.File(ctx.guild.icon) )
                    welcembed.set_author(name="Mythicley",
                                         icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                    welcembed.add_field(name="\u200b",
                                        value="This channel provides necessary information to help get you started as a member."
                                              "Please take the time to familiarize yourself with our guidelines carefully.",
                                        inline=True)
                    feedembed = discord.Embed(title="Submit a feedback",
                                              description="If you have any further questions or feedback, please `click` on the reaction below."
                                                          "We'll be able to answer any of your comments once we receive them",
                                              colour=0x00ff00)
                    # feedembed.set_author(name="Mythicley",
                    #            icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                    await ctx.send(embed=welcembed)
                    feedback = await ctx.send(embed=feedembed)
                    print(type(feedback))
                    myqueryz = {"reactionmsgbool": "yes", "guild": feedback.guild.id, "feedbackembedid": feedback.id,
                                "guildname": feedback.guild.name}
                    chcol.insert_one(myqueryz)
                    await feedback.add_reaction("✉")

    #3
    @commands.command()
    async def resetreactmsg(self,ctx, id: int):
        messageid = id
        myquery1 = {"reactionmsgbool": "yes", "guild": ctx.guild.id, "guildname": ctx.guild.name}
        myquery = {"reactionmsgbool": "yes", "guild": ctx.guild.id, "feedbackembedid": messageid,
                   "guildname": ctx.guild.name}
        mydoc = chcol.find(myquery1)
        doclist = list(mydoc)
        print(doclist)
        if doclist:
            print("Previous instance found!")
            del_query_many(chcol, mydoc)
            print("Yes!")
        try:
            chcol.insert_one(myquery)
            await ctx.send("Reaction message updated succesfully!!")
        except Exception as error:
            print("{}".format(error))

    #4
    @commands.command()
    async def addfeedbackreaction(self,ctx, id):
        msg = await ctx.channel.fetch_message(id)
        await msg.add_reaction("✉")

def setup(bot):
    bot.add_cog(Feedback(bot))