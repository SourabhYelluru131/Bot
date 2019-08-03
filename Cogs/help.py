import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.client = bot

    @commands.command()
    async def help(self, ctx, *args):
        await ctx.send("Sending...")
        async with ctx.channel.typing():
            if not args:
                embed = discord.Embed(title="HELP", description="List of commands and its functions", colour=0x00ff00)
                embed.set_footer(text='Use ".help command" for more info on a command')
                embed.set_image(
                    url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="Help", value=".help   -   Shows this message", inline=True)
                embed.add_field(name="Ping", value=".ping   -  Pings you and shows bot latency🏓", inline=False)
                # embed.add_field(name="Praise", value=".praise   -  Makes the bot praise you :wink:", inline=True)
                embed.add_field(name="Update news", value=".whatsnew  -  Shows the latest changes to the bot",
                                inline=True)
                embed.add_field(name="Uptime", value=".uptime  -  Shows the time elapsed since the bot is online",
                                inline=True)
                # embed.add_field(name="Hug", value=".hug  -  Give a user a hug. Spread Love!", inline=True)
                # embed.add_field(name="Thump", value=".thump  -  Thump someone on the head(not recommended)", inline=True)
                embed.add_field(name="Calculator", value=".calc  -  calculate the value of an expression", inline=True)
                embed.add_field(name="WolframAlpha Querying", value='.wa  -  Query anything you want :)', inline=True)
                embed.add_field(name="Adv Wolfram Query",
                                value=".waext  -  Gives more results from Wolfram with plots and images!", inline=True)
                embed.add_field(name="Rock, Paper, Scissors",
                                value=".rps [option]  -  Play Rock, Paper, Scissors with the bot!", inline=True)
                embed.add_field(name="Coin flip", value=".coin  -  Flips a coin and gives Heads or Tails", inline=True)
                embed.add_field(name="Die rolling", value=".roll  -  Roll a 6 sided die to get a random result",
                                inline=True)
                embed.add_field(name="XKCD Comic", value=".ch  -  Get a random, latest or a particular xkcd comic",
                                inline=True)
                if ctx.message.author.guild_permissions.administrator:
                    embed.add_field(name="Raffle", value='.raffle  -  Start a giveaway / raffle !!', inline=True)
                embed.add_field(name="NEW COMMANDS", value="COMING SOON .... ⚙⚙⚙", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "ping":
                embed = discord.Embed(title="ping", description="Pings you and shows bot latency🏓", colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="Method", value="```.ping```", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "whatsnew":
                embed = discord.Embed(title="whatsnew", description="Shows the latest changes to the bot",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.whatsnew```", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "uptime":
                embed = discord.Embed(title="Uptime", description="Shows the time elapsed since the bot is online",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.uptime```", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "rps":
                embed = discord.Embed(title="rps", description="Play rock paper scissors with the bot!!",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.rps <your_option_here>``` Do not put the <> signs.",
                                inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "coin":
                embed = discord.Embed(title="coin", description="Tosses a coin and returns the result!",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.coin```", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "roll":
                embed = discord.Embed(title="roll", description="Rolls a 6 sided die and return the result",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.roll```", inline=True)
                await ctx.send(embed=embed)
            elif args[0] == "raffle":
                if ctx.message.author.guild_permissions.administrator:
                    embed = discord.Embed(title="raffle", description="Starts a giveaway/raffle!!!", colour=0x00ff00)
                    embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                    embed.set_author(name="Mythicley",
                                     icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                    embed.add_field(name="**Method :**", value="```.raffle <prize> <time_period>```", inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(admin_msg)
            elif args[0] == "wa" or args[0] == "waext":
                message1 = "For basic search : "
                embed = discord.Embed(title="wa", description="Queries Wolfram|Alpha and returns you the answer!!",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.wa <query>```", inline=True)
                # await ctx.send(embed=embed)
                message2 = "For advanced search : "
                extembed = discord.Embed(title="waext",
                                         description="Gives more info related to the query from Wolfram|Alpha",
                                         colour=0x00ff00)
                extembed.set_footer(text="The owner of this bot is Orthocresol#3004")
                extembed.set_author(name="Mythicley",
                                    icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                extembed.add_field(name="**Method :**", value="```.waext <query>```", inline=True)
                await ctx.send(content=message1, embed=embed)
                await ctx.send(content=message2, embed=extembed)
            elif args[0] == "ch" or args[0] == "xkcd":
                message1 = "for random comic"
                embed = discord.Embed(title="ch", description="Returns random comic !!",
                                      colour=0x00ff00)
                embed.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed.set_author(name="Mythicley",
                                 icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed.add_field(name="**Method :**", value="```.ch```", inline=True)
                message2 = "for latest comic"
                embed2 = discord.Embed(title="ch", description="Returns latest comic !!",
                                       colour=0x00ff00)
                embed2.set_footer(text="The owner of this bot is Orthocresol#3004")
                embed2.set_author(name="Mythicley",
                                  icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed2.add_field(name="**Method :**", value="```.ch latest```", inline=True)
                message3 = "for particular comic"
                embed3 = discord.Embed(title="ch", description="Returns random comic !!",
                                       colour=0x00ff00)
                embed3.set_footer(text="Do not put <> signs")
                embed3.set_author(name="Mythicley",
                                  icon_url='https://cdn.discordapp.com/attachments/437668400102244363/440693017020727305/Profile_Picture.png')
                embed3.add_field(name="**Method :**", value="```.ch <value>```", inline=True)
                await ctx.send(content=message1, embed=embed)
                await ctx.send(content=message2, embed=embed2)
                await ctx.send(content=message3, embed=embed3)
            else:
                await ctx.send('Command or category "{}" not found.'.format(args[0]))

def setup(bot):
    bot.add_cog(Help(bot))
