#================================================   Imports   =========================================================#

import discord
from discord.ext import commands
from discord import Embed
from datetime import date, time,datetime,timedelta
#from DiscordHooks import Hook, Embed, EmbedAuthor, Color
import asyncio
import token

#================================================   Cogs   ============================================================#

extensions = ["Cogs.help","Cogs.fun","Cogs.feedback","Cogs.raffle","Cogs.embed","Cogs.wolframalpha","Cogs.xkcd","Cogs.economy"]

#================================================   Setting variables   ===============================================#

bot = commands.Bot(description="My first cool bot", command_prefix=".")
bot.remove_command('help')
admin_msg = 'You need "Administrator" permissions to use this command!!'
botid = 434285481841131520                    #Enter BOT ID here
botname = ["Mythicley", "mythicley","@Mythicley"]                  #Enter Bot name here

#=================================================   Bot events   =====================================================#

# Logging and setting status when the bot turns on
@bot.event
async def on_ready():
    print("Heave ho, the bot is running....")
    print("________________________________________________________________________")
    await bot.loop.create_task(presence_task())

@bot.event
async def presence_task():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with You"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Streaming(name=".help", url="https://twitch.tv"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with My owner"))
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Chatting with humans"))
        await asyncio.sleep(30)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with Myself"))
        await asyncio.sleep(5)
# 🎉 / 👀
@bot.event
async def on_message(message):
    contents = message.content.split(" ")            # Splits the message into smaller elements when divided with space
    for n in contents:
        if n in botname:                             # Checks for botname in the contents of the message
            await message.add_reaction("👀")         # Adds 👀 reaction when the bot's name is taken
    await bot.process_commands(message)              # Sends the message to process commands when done with the loop

#@bot.event
#async def on_message(ctx,message):
 #   if message.content.startswith("set webhookchannel"):
 #           webhook_channel_id = ctx.channel.id
 #           print(webhook_channel_id)
 #           await create_webhook(name=Orthohookey, avatar=None)
 #   await bot.process_commands(message)

#======================================================   BOT COMMANDS   ==============================================#
@bot.command()
async def load(extension):
    try:
        bot.load_extension(extension)
        print("Loaded {}".format(extension))
    except Exception as error:
        print("{} cannot be loaded. [{}]".format(extension,error))

@bot.command()
async def unload(extension):
    try:
        bot.unload_extension(extension)
        print("Unloaded {}".format(extension))
    except Exception as error:
        print("{} cannot be unloaded. [{}]".format(extension,error))

# 7
#@bot.command()
#async def hug(ctx, user: discord.Member):
#    await ctx.send("{} has given {}, a hug".format(ctx.message.author.mention, user.mention))

# 8
#@bot.command()
#async def thump(ctx, user: discord.Member):
#    await ctx.send("Hey {}, You just got thumped on the head ! Quit being a knucklehead!".format(user.mention))

#11
@bot.command()
async def hook(ctx):
    webhook_url = "https://discordapp.com/api/webhooks/469108008794718208/UOoUk49oK3GP6EPhjibdMQmSz_M1tLDNnSf4knl0AjU6rpCNrR8zDN9TqnmQEoKco6V1"
    embed = Embed(title='look here', url=webhook_url, description="some embed text here", timestamp=datetime.now(),
                color=Color.Aqua, author=EmbedAuthor(name="Orthocresol#3004"))
    Hook(hook_url=webhook_url, username="Orthocresol's webhook",
         avatar_url='https://avatars1.githubusercontent.com/u/14138694',
         content="Hello there! \U0001f62e", embeds=[embed]).execute()

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded, [{}]'.format(extension,error))
    # Running the bot with its token
    bot.run(token.botapi)