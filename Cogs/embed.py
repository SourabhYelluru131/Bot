import discord
from discord.ext import commands
import copy

class Embed(commands.Cog):
    def __init__(self,bot):
        self.client = bot

    @commands.command()
    async def createembed(self,ctx, channel: discord.TextChannel, colour: discord.Colour, *args):
        botembed = discord.Embed(title=args[0], description="\u200b", colour=colour)
        # errembed = discord.Embed(title="Invalid colour", description="Something went wrong with the colour argument", colour=discord.Colour.red())
        # errembed.add_field(name="`{}` must be a hex value(with a #) or a CSS colour keyword".format(colour))
        # errembed.set_footer(text="Owner: Orthocresol#3004|{}".format(datetime.utcnow()))
        # await ctx.send(embed=errembed)
        n = len(args)
        for i in range(1, n):
            botembed.add_field(name=args[i], value="\u200b", inline=True)
        await ctx.message.delete()
        await channel.send(embed=botembed)

    @commands.command()
    async def editembed(self,channel: discord.TextChannel, *args):
        embid = args[0]
        message = await channel.fetch_message(embid)
        msg = message.embeds[0]
        if args[1] == "Title" or args[1] == "title":
            newEmbed = copy.copy(msg)
            newEmbed.title = args[2]
        elif args[1] == "body" or args[1] == "Body":
            n = len(args) - 2
            newtempEmbed = copy.copy(msg)
            newEmbed = discord.Embed(title=newtempEmbed.title, description="\u200b", colour=newtempEmbed.colour)
            for i in range(0, n):
                newEmbed.add_field(name=args[i + 2], value="\u200b", inline=True)
        else:
            newEmbed = copy.copy(msg)
        await message.edit(embed=newEmbed)

def setup(bot):
    bot.add_cog(Embed(bot))