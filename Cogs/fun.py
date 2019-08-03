import discord
from discord.ext import commands
from datetime import date, time,datetime,timedelta
import random


class Fun(commands.Cog):
    def __init__(self,bot):
        self.client = bot

        self.client.launch_time = datetime.utcnow()

    @commands.command()
    async def ping(self,ctx):
        latency = self.client.latency
        await ctx.send("{}, Pong!, that took {} ms  🏓".format(ctx.message.author.mention, int(latency * 1000)))

    # 2
    @commands.command()
    async def uptime(self,ctx):
        delta_uptime = datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"```{days}d, {hours}h, {minutes}m, {seconds}s```")  # Shows the uptime in d ,h ,m ,s format

    # 3
    @commands.command()
    async def praise(self,ctx):
        await ctx.send(
            "{}, you are GREAT . In fact, you are the greatest of all. Everyone, hail {}".format(
                ctx.message.author.mention,
                ctx.message.author))

    # 4
    @commands.command()
    async def whatsnew(self,ctx):
        await ctx.send(
            "```Version 1.0.5``` Added `.wa` and `.waext` command for Wolfram Querying!! and also `.rps` command for playing rock paper scissors with the bot and `.coin` and `.roll` commands to flip a coin or roll a die!")

    # 5
    @commands.command()
    async def embed(self, ctx):
        """Sends and Embed """
        embed = discord.Embed(title="title", description="description", colour=0x00ff00)
        embed.set_footer(text="footer")
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
        embed.set_author(name="author")
        icon_url = 'https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png'
        embed.add_field(name="field", value="value", inline=True)
        embed.add_field(name="field", value="value", inline=False)
        embed.add_field(name="field", value="value", inline=False)
        embed.add_field(name="field", value="value", inline=True)
        await ctx.send(embed=embed)

    #6
    @commands.command()
    async def calc(self, ctx, calcstr):
        async with ctx.channel.typing():
            input = calcstr
            output = str(eval(calcstr))
            embed = discord.Embed(title="Calculator", description="Calculates your input", colour=0x00ff00)
            embed.add_field(name="INPUT", value="```" + input + "```", inline=True)
            embed.add_field(name="OUTPUT", value="```" + output + "```", inline=False)
            await ctx.send(embed=embed)

    #7
    @commands.command()
    async def rps(self,ctx, optstr):
        expected_options = ["rock", "paper", "scissors"]
        botchoice = random.choice(expected_options)
        if botchoice == "rock":
            choice_emoji = ":punch:"
        elif botchoice == "paper":
            choice_emoji = ":hand_splayed:"
        elif botchoice == "scissors":
            choice_emoji = ":v:"
        if optstr not in expected_options:
            await ctx.send(
                "❌ | {}, the correct usage is `.rps [rock/paper/scissors]` :white_small_square:| e.g. `.rps rock`".format(
                    ctx.message.author))
        else:
            output_message = "I'm choosing **" + botchoice + "**! " + choice_emoji
            if botchoice == optstr:
                await ctx.send(output_message + " It's a tie!")
            else:
                if botchoice == "rock":
                    if optstr == "paper":
                        await ctx.send(output_message + " **PAPER** wins")
                    else:
                        await ctx.send(output_message + " **ROCK** wins")
                elif botchoice == "paper":
                    if optstr == "rock":
                        await ctx.send(output_message + " **PAPER** wins")
                    else:
                        await ctx.send(output_message + " **SCISSORS** wins")
                elif botchoice == "scissors":
                    if optstr == "rock":
                        await ctx.send(output_message + " **ROCK** wins")
                    else:
                        await ctx.send(output_message + " **SCISSORS** wins")

    #8
    @commands.command()
    async def coin(self,ctx):
        res_opt = ["HEADS", "TAILS"]
        bot_opt = random.choice(res_opt)
        flipembed = discord.Embed(title="Coinflip Results", description=None, colour=discord.Colour.red())
        flipembed.set_footer(text="Owner: Orthocresol#3004")
        flipembed.set_thumbnail(
            url='http://media.buzzle.com/media/images-en/gallery/symbols/600-141325539-coin-toss.jpg')
        # flipembed.set_author(name=None)
        flipembed.add_field(name="\u200b", value="{} tossed a coin and got {}!".format(ctx.message.author, bot_opt),
                            inline=True)
        await ctx.send(embed=flipembed)

    #9
    @commands.command()
    async def roll(self,ctx):
        res = random.randrange(1, 6, 1)
        rollembed = discord.Embed(title="Results", description=None, colour=0x00ff00)
        rollembed.set_footer(text="Owner: Orthocresol#3004")
        rollembed.set_thumbnail(
            url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYuK-0-eHQlL-OL95jW9C7IyQ01lfjOdHJmUhF-fwNG1GNUCl8')
        rollembed.add_field(name="\u200b",
                            value="In the end, result was {}!".format(res), inline=True)
        await ctx.send(embed=rollembed)

def setup(bot):
    bot.add_cog(Fun(bot))