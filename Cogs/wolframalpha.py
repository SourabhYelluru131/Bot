import discord
from discord.ext import commands
import re
import wolframalpha
import random
import token

app_ID = token.Wolframappid
waclient = wolframalpha.Client(app_ID)
messageHistory = set()
computemessageHistory = set()
ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
ipv6_regex = re.compile(
    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

# Fun strings for invalid queries
invalidQueryStrings = ["Nobody knows.",
                       "It's a mystery.",
                       "I have no idea.",
                       "No clue, sorry!",
                       "I'm afraid I can't let you do that.",
                       "Maybe another time.",
                       "Ask someone else.",
                       "That is anybody's guess.",
                       "Beats me.",
                       "I haven't the faintest idea."]

# Prints a single result pod
async def printPod(ctx, text, title):
    text = text.replace("Wolfram|Alpha", "Wolfbot")
    text = text.replace("Wolfram", "Wolf")
    text = re.sub(ipv4_regex, "IP Redacted", text)
    text = re.sub(ipv6_regex, "IP Redacted", text)
    resembed = discord.Embed(title=title, description="Wolfram|Alpha Results", colour=0x00ff00)
    resembed.set_footer(text="Owner: Orthocresol#3004")
    resembed.set_thumbnail(
        url='https://pbs.twimg.com/profile_images/804868917990739969/OFknlig__400x400.jpg')
    resembed.set_author(name="Wolfram|Alpha")
    resembed.add_field(name="Result:", value=text, inline=True)
    await ctx.send(embed=resembed)
    messageHistory.add(resembed)

# Prints a single image pod
async def printImgPod(ctx, img, title):
    resembed = discord.Embed(title=title, description="Wolfram|Alpha results", colour=0x00ff00)
    resembed.set_footer(text="Owner: Orthocresol#3004")
    resembed.set_image(
        url=img)
    resembed.set_thumbnail(
        url='https://pbs.twimg.com/profile_images/804868917990739969/OFknlig__400x400.jpg')
    resembed.set_author(name="Wolfram|Alpha")
    await ctx.send(embed=resembed)
    messageHistory.add(resembed)

class WolframAlpha(commands.Cog):
    def __init__(self,bot):
        self.client = bot

    #1
    @commands.command()
    async def wa(self,ctx):
        previousQuery = " "
        if len(ctx.message.content) > 3:
            # Strip .wa
            query = ctx.message.content[3:]

            # Run wolfram alpha query
            if len(query) > 1:
                queryComputeMessage = await ctx.send(
                    ":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
                print(ctx.author.name + " | Query: " + query)
            else:
                print(ctx.author.name + " | Query: " + previousQuery)
                queryComputeMessage = await ctx.send(
                    ":wolf: Computing '" + previousQuery + "' :computer: :thought_balloon: ...")
            computemessageHistory.add(queryComputeMessage)

            # Short answer query
            res = waclient.query(query)
            if len(list(res.pods)) > 0:
                resultPresent = 0
                podLimit = 0
                # WA returns a "result" pod for simple maths queries but for more complex ones it returns randomly titled ones
                for pod in res.pods:
                    if pod.title == 'Result':
                        resultPresent = 1

                for pod in res.pods:
                    if pod.text:
                        if resultPresent == 1:
                            if pod.title == 'Result':
                                await printPod(ctx.message.channel, pod.text, pod.title)
                        # If no result pod is present, prints input interpretation and 1 other pod (normally contains useful answer)
                        else:
                            if podLimit < 2:
                                await printPod(ctx.message.channel, pod.text, pod.title)
                                podLimit += 1
            else:
                await ctx.send(random.choice(invalidQueryStrings))

            if len(list(res.pods)) - 2 > 0:
                await queryComputeMessage.edit(content=str(
                    queryComputeMessage.content) + "Finished! " + ctx.message.author.mention + " :checkered_flag: (" + str(
                    len(list(res.pods)) - 2) + " more result pods available, rerun query with .waext)")
            else:
                await queryComputeMessage.edit(content=str(
                    queryComputeMessage.content) + "Finished! " + ctx.message.author.mention + " :checkered_flag:")
        previousQuery = query

    #2
    @commands.command()
    async def waext(self,ctx):
        query = ctx.message.content[6:]
        previousQuery = ""
        if len(query) > 1:
            queryComputeMessage = await ctx.send(":wolf: Computing '" + query + "' :computer: :thought_balloon: ...")
            print(ctx.author.name + " | Query: " + query)
        else:
            print(ctx.author.name + " | Query: " + previousQuery)
            queryComputeMessage = await ctx.send(
                ":wolf: Computing '" + previousQuery + "' :computer: :thought_balloon: ...")
        computemessageHistory.add(queryComputeMessage)
        # Expanded query
        if len(query) > 1:
            res = waclient.query(query)
            if len(list(res.pods)) > 0:
                for pod in res.pods:
                    if pod.text:
                        await printPod(ctx.message.channel, pod.text, pod.title)
                    else:
                        for sub in pod.subpods:
                            for img in sub.img:
                                await printImgPod(ctx.message.channel, img['@src'], pod.title)

                await queryComputeMessage.edit(content=str(
                    queryComputeMessage.content) + "Finished! " + ctx.message.author.mention + " :checkered_flag:")
            else:
                await ctx.send(random.choice(invalidQueryStrings))
        else:
            res = waclient.query(previousQuery)
            if len(list(res.pods)) > 0:
                for pod in res.pods:
                    if pod.text:
                        await printPod(ctx.message.channel, pod.text, pod.title)
                    elif pod.img:
                        await printImgPod(ctx.message.channel, pod.img, pod.title)

                await queryComputeMessage.edit(content=str(
                    queryComputeMessage.content) + "Finished! " + ctx.message.author.mention + " :checkered_flag:")

def setup(bot):
    bot.add_cog(WolframAlpha(bot))