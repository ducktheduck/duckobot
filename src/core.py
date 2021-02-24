import glob # Importing required libraries and modules.
from discord.ext import commands
import discord
import json
import platform
import random
from termcolor import colored
bot = commands.Bot(command_prefix='-', intents = discord.Intents.all()) # Initiating the bot with a custom prefix and intents enabled.
bot.remove_command('help') # Removing the help command to add a custom one.
from Library.Util.ReloadCommand import ReloadCommand
# import os, sys
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '..')))

data = json.load(open('./Library/Config/config.json', "r"))
token = data["token"]


@bot.event
async def on_ready(): # On ready event

    print(f'Ready <{colored(bot.user.name, "red")}>')
    games = ["Venom: Let There Be Carnage", "Godzilla vs. Kong"]
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(games)))


@bot.event
async def on_command_error(ctx, error): # Error handler

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.BadArgument):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        return

    if isinstance(error, commands.MissingPermissions):
        return

    else:
        raise error


if __name__ == "__main__": # Running cogs
    possibleCommands = glob.glob('./Commands/**/*.py')

    for file in possibleCommands:
        try:
                        
            if file.endswith('.py'):    
                
                if platform.system() == "Linux":

                    bot.load_extension(file[2:].replace('/', '.')[:-3])

                    print("Cog stable: " + str(file[2:].replace('/', '.')[:-3].split(".")[2]))
                else:
                    bot.load_extension(file[2:].replace('\\', '.')[:-3])
                    print("Cog stable: " + str(file[2:].replace('\\', '.')[:-3].split(".")[2]))

        except Exception as e:

            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error, unstable cog: {}\n{}'.format(file, exc))


@bot.command()
async def reload(self, ctx): # Reload command
    await ReloadCommand(self, ctx, bot)


bot.run(token)
