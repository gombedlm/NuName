import discord
from discord.ext import commands
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Directories
LOGS_DIR = 'logs'
DATA_DIR = 'data'

# File paths
USER_DATA_PATH = os.path.join(DATA_DIR, 'user_data.json')
NAMING_CONVENTION_PATH = os.path.join(DATA_DIR, 'naming_convention.json')

# Ensure directories exist
for directory in [LOGS_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(os.path.join(LOGS_DIR, 'bot.log'))
                    ])

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize bot with intents and without command prefix for slash commands
bot = commands.Bot(intents=intents)

# Load data
user_data = {"counter": 0, "users": {}}
naming_convention = {"format": "{counter:03} | {username}"}

def load_json(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading {file_path}: {e}")
    return default_data

user_data = load_json(USER_DATA_PATH, user_data)
naming_convention = load_json(NAMING_CONVENTION_PATH, naming_convention)

def save_json(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving {file_path}: {e}")

# Event Handlers

@bot.event
async def on_ready():
    """Handles the bot's readiness."""
    logger.info(f'NuName bot {bot.user} is ready.')
    try:
        # Optionally sync slash commands (not necessary with latest discord.py)
        # await bot.slash_command('ping', description='Check if the bot is responsive').sync()
        logger.info("Slash commands synced.")
    except Exception as e:
        logger.error(f"Failed to sync slash commands: {e}")

    if not bot.guilds:
        logger.warning("Bot is not connected to any guilds.")
        return

    guild = bot.guilds[0]
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

    save_json(USER_DATA_PATH, user_data)

@bot.event
async def on_member_join(member):
    """Handles a new member joining the server."""
    try:
        if member.bot:
            new_nickname = f'BOT | {member.name}'
            await member.edit(nick=new_nickname)
            logger.info(f'Assigned bot nickname {new_nickname} to {member.name}')
            return

        while user_data["counter"] + 1 in user_data["users"]:
            user_data["counter"] += 1

        user_data["counter"] += 1
        new_nickname = naming_convention["format"].format(counter=user_data["counter"], username=member.name)
        user_data["users"][str(member.id)] = new_nickname
        save_json(USER_DATA_PATH, user_data)

        await member.edit(nick=new_nickname)
        logger.info(f'Assigned nickname {new_nickname} to {member.name}')

        await member.send(f"Welcome to the server, {member.name}! Your ID-like nickname is now: {new_nickname}")

    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {member.name}")
    except Exception as e:
        logger.error(f"Error in on_member_join: {e}")

@bot.event
async def on_member_remove(member):
    """Handles a member leaving the server."""
    logger.info(f'{member.name} has left the server.')

@bot.event
async def on_member_update(before, after):
    """Handles a member's nickname update."""
    try:
        if before.nick != after.nick and after.nick != user_data["users"].get(str(after.id)):
            await after.edit(nick=user_data["users"][str(after.id)])
            logger.info(f'Reverted nickname change for {after.name}')
    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {after.name}")
    except KeyError:
        logger.error(f"User {after.name} not found in user_data")
    except Exception as e:
        logger.error(f"Error in on_member_update: {e}")

# Slash Commands

@bot.slash_command(name="organize-nicknames", description="Organize member nicknames with a predefined format.")
async def organize_nicknames(ctx: commands.Context):
    try:
        guild = ctx.guild
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

        save_json(USER_DATA_PATH, user_data)

        for member in guild.members:
            if not member.bot:
                while user_data["counter"] + 1 in user_data["users"]:
                    user_data["counter"] += 1

                user_data["counter"] += 1
                new_nickname = naming_convention["format"].format(counter=user_data["counter"], username=member.name)
                user_data["users"][str(member.id)] = new_nickname
                save_json(USER_DATA_PATH, user_data)

                await member.edit(nick=new_nickname)
                logger.info(f'Assigned nickname {new_nickname} to {member.name}')

        await ctx.send("Nicknames organized successfully.")

    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {member.name}")
        await ctx.send("Permission error: Unable to change nicknames due to missing permissions.")

    except Exception as e:
        logger.error(f"Error in organize_nicknames: {e}")
        await ctx.send(f"An error occurred: {e}")

@bot.slash_command(name="help", description="Show available commands.")
async def help_command(ctx: commands.Context):
    """Display available commands."""
    command_list = "\n".join([f"/{command.name}: {command.description}" for command in bot.slash_commands])
    await ctx.send(f"Available Commands:\n{command_list}")

# Run the bot
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    logger.error("No valid DISCORD_TOKEN found. Bot cannot start.")
