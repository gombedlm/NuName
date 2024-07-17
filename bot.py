import discord
from discord.ext import commands
import json
import os
import logging
from dotenv import load_dotenv
from interactions import SlashCommand
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
slash = SlashCommand(bot, sync_commands=True)  # Initialize SlashCommand with the bot instance

# Load or initialize the internal counter and user data
user_data = {"counter": 0, "users": {}}

if os.path.exists('user_data.json'):
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading user_data.json: {e}")
else:
    logger.info("user_data.json not found, initializing with default values.")

def save_user_data():
    try:
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving user_data.json: {e}")

@bot.event
async def on_ready():
    try:
        logger.info(f'NuName bot {bot.user} is ready.')

        if len(bot.guilds) == 0:
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

        save_user_data()

    except Exception as e:
        logger.error(f"Error in on_ready: {e}")

@bot.event
async def on_member_join(member):
    try:
        if member.bot:
            new_nickname = f'BOT | {member.name}'
            await member.edit(nick=new_nickname)
            logger.info(f'NuName assigned bot nickname {new_nickname} to {member.name}')
            return

        while user_data["counter"] + 1 in user_data["users"].keys():
            user_data["counter"] += 1

        user_data["counter"] += 1
        user_data["users"][str(member.id)] = f'{user_data["counter"]:03} | {member.name}'
        save_user_data()

        new_nickname = f'{user_data["counter"]:03} | {member.name}'
        await member.edit(nick=new_nickname)
        logger.info(f'NuName assigned nickname {new_nickname} to {member.name}')

        await member.send(f"Welcome to the server, {member.name}! Your ID-like nickname is now: {new_nickname}")

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
        if before.nick != after.nick and after.nick != user_data["users"].get(str(after.id), None):
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
    try:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use this command.")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("I do not have permission to perform this action.")
        else:
            await ctx.send("An error occurred.")
            logger.error(f"Unhandled command error: {error}")
    except Exception as e:
        logger.error(f"Error in on_command_error: {e}")

# Define slash commands using SlashCommand's decorator
@slash.slash(name="ping", description="Check if the bot is alive")
async def ping(ctx: SlashContext):
    await ctx.send("Pong!")

@slash.slash(name="id", description="Get your ID-like nickname")
async def id(ctx: SlashContext):
    try:
        user_nickname = user_data["users"].get(str(ctx.author.id), "Nickname not found.")
        await ctx.send(f"Your ID-like nickname is: {user_nickname}")
    except Exception as e:
        await ctx.send("An error occurred while fetching your nickname.")
        logger.error(f"Error in id command: {e}")

@slash.slash(name="set_ids", description="Set ID-like nicknames for all members (Admin only)")
async def set_ids(ctx: SlashContext):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to use this command.", hidden=True)
        return

    try:
        guild = ctx.guild
        user_data["counter"] = 0

        for member in guild.members:
            if member.bot:
                new_nickname = f'BOT | {member.name}'
                await member.edit(nick=new_nickname)
                logger.info(f'NuName assigned bot nickname {new_nickname} to {member.name}')
                continue

            user_data["counter"] += 1
            new_nickname = f'{user_data["counter"]:03} | {member.name}'
            await member.edit(nick=new_nickname)
            user_data["users"][str(member.id)] = new_nickname
            logger.info(f'NuName assigned nickname {new_nickname} to {member.name}')

        save_user_data()
        await ctx.send("ID-like nicknames have been set for all members.", hidden=True)
    except discord.Forbidden:
        await ctx.send("Permission error: Cannot change nickname for some members.", hidden=True)
    except Exception as e:
        await ctx.send("An error occurred while setting ID-like nicknames.", hidden=True)
        logger.error(f"Error in set_ids command: {e}")

@slash.slash(name="toggle_functionality", description="Enable or disable bot functionality (Admin only)")
async def toggle_functionality(ctx: SlashContext, feature: str):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("You do not have permission to use this command.", hidden=True)
        return

    if feature.lower() == "nickname":
        user_data["toggle_nickname"] = not user_data.get("toggle_nickname", False)
        status = "enabled" if user_data["toggle_nickname"] else "disabled"
        await ctx.send(f"Nickname functionality has been {status}.", hidden=True)
        logger.info(f"Nickname functionality has been {status}.")
    else:
        await ctx.send("Unsupported feature. Currently only 'nickname' is supported.", hidden=True)

    save_user_data()

# Get the Discord token from environment variables
try:
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN is None:
        raise ValueError("DISCORD_TOKEN environment variable is not set")
except Exception as e:
    logger.error(f"Error retrieving DISCORD_TOKEN: {e}")
    TOKEN = None

# Run the bot with the token
if TOKEN:
    bot.run(TOKEN)
else:
    logger.error("No valid DISCORD_TOKEN found. Bot cannot start.")
