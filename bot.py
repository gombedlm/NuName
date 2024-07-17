import discord
from discord.ext import commands
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('bot.log')

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Define intents
intents = discord.Intents.default()
intents.members = True  # Enable the members intent

bot = commands.Bot(command_prefix="!", intents=intents)

# Load or initialize the internal counter and user data
if os.path.exists('user_data.json'):
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading user_data.json: {e}")
        user_data = {"counter": 0, "users": {}}
else:
    user_data = {"counter": 0, "users": {}}

def save_user_data():
    try:
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f)
    except Exception as e:
        logger.error(f"Error saving user_data.json: {e}")

@bot.event
async def on_ready():
    logger.info(f'NuName bot {bot.user} is ready.')

    # Ensure bot is connected to at least one guild
    if len(bot.guilds) == 0:
        logger.warning("Bot is not connected to any guilds.")
        return

    # Proceed with handling guild data
    guild = bot.guilds[0]  # Assuming the bot is in only one guild

    existing_numbers = []
    for member in guild.members:
        if member.nick:
            try:
                number = int(member.nick.split(" | ")[0])
                existing_numbers.append(number)
            except ValueError:
                logger.warning(f"Invalid nickname format for {member.name}")

    if existing_numbers:
        user_data["counter"] = max(existing_numbers)

    save_user_data()

@bot.event
async def on_member_join(member):
    existing_numbers = []
    try:
        # Find the next available counter
        while user_data["counter"] + 1 in existing_numbers:
            user_data["counter"] += 1

        user_data["counter"] += 1
        user_data["users"][str(member.id)] = f'{user_data["counter"]:03} | {member.name}'
        save_user_data()

        new_nickname = user_data["users"][str(member.id)]
        await member.edit(nick=new_nickname)
        logger.info(f'NuName assigned nickname {new_nickname} to {member.name}')
    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {member.name}")
    except Exception as e:
        logger.error(f"Error in on_member_join: {e}")

@bot.event
async def on_member_remove(member):
    try:
        logger.info(f'{member.name} has left the server.')
    except Exception as e:
        logger.error(f"Error in on_member_remove: {e}")

@bot.event
async def on_member_update(before, after):
    try:
        if before.nick != after.nick and after.nick != user_data["users"][str(after.id)]:
            await after.edit(nick=user_data["users"][str(after.id)])
            logger.info(f'NuName reverted nickname change for {after.name}')
    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {after.name}")
    except KeyError:
        logger.error(f"User {after.name} not found in user_data")
    except Exception as e:
        logger.error(f"Error in on_member_update: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Bad argument.")
    else:
        await ctx.send("An error occurred.")
        logger.error(f"Unhandled command error: {error}")

# Get the Discord token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    logger.error("DISCORD_TOKEN is not set in the .env file.")
else:
    # Run the bot with the Discord token
    bot.run(TOKEN)
