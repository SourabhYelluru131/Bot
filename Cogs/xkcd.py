import discord
from discord.ext import commands
import urllib.request, json
from discord import Embed
import random

def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def _formatComic(data, imgsrc):
    if int(data["month"]) < 10:
        month = "".join(("0", str(data["month"])))
    else:
        month = data["month"]
    if int(data["day"]) < 10:
        day = "".join(("0", str(data["day"])))
    else:
        day = data["day"]
    imgtitle = data["title"]
    imgalt = data["alt"]
    imgnum = data["num"]
    imgdate = "".join((data["year"], "-", month, "-", day))
    e = Embed(color=0x7610ba)
    e.set_image(url=imgsrc)
    e.set_footer(text=imgalt)
    e.add_field(name=imgtitle, value=imgdate + " | " + str(imgnum), inline=False)
    return e

def getLatestComicData():
    # Feteches the JSON of the latest submission.
    with urllib.request.urlopen("https://xkcd.com/info.0.json") as url:
        data = json.load(url)
        return data

def getLatestComic():
    data = getLatestComicData()
    imgsrc = data["img"]
    return _formatComic(data, imgsrc)

def getRandomComic():
    latest = getLatestComicData()
    # Generates a random number to represent the ComicID.
    randomComicID = random.randint(1, latest["num"])
    # Fetches the JSON and returns the image.
    with urllib.request.urlopen("http://xkcd.com/" + str(randomComicID) + "/info.0.json") as randomUrl:
        data = json.load(randomUrl)
    imgsrc = data["img"]
    return _formatComic(data, imgsrc)

def getComic(comicID):
    latest = getLatestComicData()
    if comicID > 0 and comicID <= latest["num"]:
        # Comic ID is valid.
        with urllib.request.urlopen("http://xkcd.com/" + str(comicID) + "/info.0.json") as comicUrl:
            data = json.load(comicUrl)
            imgsrc = data["img"]
    elif comicID > latest["num"]:
        return 0
    return _formatComic(data, imgsrc)

class Xkcd(commands.Cog):
    def __init__(self,bot):
        self.client = bot

    def is_me(self, m):
        return m.author == self.bot.user

    @commands.command()
    async def ch(self,ctx, *args):
        async with ctx.channel.typing():
            if not args:
                comic_embed = getRandomComic()
                await ctx.send(embed=comic_embed)
            elif args[0] == "latest":
                comic_embed = getLatestComic()
                await ctx.send(embed=comic_embed)
            elif is_int(args[0]):
                if int(args[0]) <= 0:
                    await ctx.send("Xkcd comic number must be positive")
                comic_embed = getComic(int(args[0]))
                if type(comic_embed) is not discord.embeds.Embed and int(args[0]) > 0:
                    await ctx.send("Ok... Error bringing an xkcd comic from the future. Try again with a lower number.")
                else:
                    await ctx.send(embed=comic_embed)
            else:
                await ctx.send("Something went wrong. Use `.help ch` for help for this command!")

def setup(bot):
    bot.add_cog(Xkcd(bot))