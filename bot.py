import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize bot with a command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Directories and file paths for data storage
LOGS_DIR = 'logs'
DATA_DIR = 'data'
USER_DATA_PATH = os.path.join(DATA_DIR, 'user_data.json')
NAMING_CONVENTION_PATH = os.path.join(DATA_DIR, 'naming_convention.json')

# Ensure directories exist for logging and data storage
for directory in [LOGS_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to load JSON data from file
def load_json(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading {file_path}: {e}")
    return default_data

# Function to save JSON data to file
def save_json(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

# Event to print bot's login confirmation upon successful connection
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Slash command to organize nicknames based on a numbering convention
@bot.slash_command(name="organize-nicknames", description="Organize nicknames based on a numbering convention.")
async def organize_nicknames(ctx: commands.Context):
    user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
    naming_convention = load_json(NAMING_CONVENTION_PATH, {"format": "{counter:03} | {username}"})

    try:
        while user_data["counter"] + 1 in user_data["users"]:
            user_data["counter"] += 1

        user_data["counter"] += 1
        new_nickname = naming_convention["format"].format(counter=user_data["counter"], username=ctx.author.name)
        user_data["users"][str(ctx.author.id)] = new_nickname

        # Save updated user data
        save_json(USER_DATA_PATH, user_data)
        await ctx.send(f"Your nickname has been updated to: {new_nickname}")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Slash command to display available commands
@bot.slash_command(name="list-commands", description="Show available commands.")
async def list_commands(ctx: commands.Context):
    command_list = "\n".join([f"/{command.name}: {command.description}" for command in bot.slash_commands])
    await ctx.send(f"Available Commands:\n{command_list}")

# Run the bot with the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No valid DISCORD_TOKEN found. Bot cannot start.")
import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize bot with a command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Directories and file paths for data storage
LOGS_DIR = 'logs'
DATA_DIR = 'data'
USER_DATA_PATH = os.path.join(DATA_DIR, 'user_data.json')
NAMING_CONVENTION_PATH = os.path.join(DATA_DIR, 'naming_convention.json')

# Ensure directories exist for logging and data storage
for directory in [LOGS_DIR, DATA_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to load JSON data from file
def load_json(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading {file_path}: {e}")
    return default_data

# Function to save JSON data to file
def save_json(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

# Event to print bot's login confirmation upon successful connection
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Slash command to organize nicknames based on a numbering convention
@bot.slash_command(name="organize-nicknames", description="Organize nicknames based on a numbering convention.")
async def organize_nicknames(ctx: commands.Context):
    user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
    naming_convention = load_json(NAMING_CONVENTION_PATH, {"format": "{counter:03} | {username}"})

    try:
        while user_data["counter"] + 1 in user_data["users"]:
            user_data["counter"] += 1

        user_data["counter"] += 1
        new_nickname = naming_convention["format"].format(counter=user_data["counter"], username=ctx.author.name)
        user_data["users"][str(ctx.author.id)] = new_nickname

        # Save updated user data
        save_json(USER_DATA_PATH, user_data)
        await ctx.send(f"Your nickname has been updated to: {new_nickname}")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Slash command to display available commands
@bot.slash_command(name="list-commands", description="Show available commands.")
async def list_commands(ctx: commands.Context):
    command_list = "\n".join([f"/{command.name}: {command.description}" for command in bot.slash_commands])
    await ctx.send(f"Available Commands:\n{command_list}")

# Run the bot with the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No valid DISCORD_TOKEN found. Bot cannot start.")
