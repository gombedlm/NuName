import discord
from discord.ext import commands
import os
import json
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Add this if needed

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

# Function to extract ID from nickname
def extract_id(nickname):
    match = re.match(r"(\d{3})", nickname)
    if match:
        return int(match.group(1))
    return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f"Guilds: {[guild.name for guild in bot.guilds]}")  # Print guild names for debugging

    try:
        synced = await bot.tree.sync()  # Sync the slash commands with Discord
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    # Check if the bot is in any guilds
    if bot.guilds:
        guild = bot.guilds[0]
        # Initial organization of nicknames when the bot starts
        await organize_all_nicknames(guild)
    else:
        print("The bot is not currently in any guilds.")

# Function to organize all nicknames in the server
async def organize_all_nicknames(guild):
    user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
    naming_convention = load_json(NAMING_CONVENTION_PATH, {"format": "{counter:03} | {display_name}"})
    naming_format = naming_convention["format"]

    current_ids = {extract_id(member.display_name) for member in guild.members if extract_id(member.display_name) is not None}
    max_id = max(current_ids, default=0)

    members_with_convention = []
    members_without_convention = []

    for member in guild.members:
        if member.bot:
            # Rename bots to "BOT"
            await member.edit(nick="BOT | " + member.name)
        elif extract_id(member.display_name) is not None:
            members_with_convention.append(member)
        else:
            members_without_convention.append(member)

    members_without_convention.sort(key=lambda m: m.display_name)

    available_ids = sorted(set(range(1, max_id + 2)) - current_ids)
    new_counter = max_id + 1
    user_data["counter"] = new_counter

    for member in members_without_convention:
        new_id = available_ids.pop(0) if available_ids else new_counter
        new_nickname = naming_format.format(counter=new_id, display_name=member.display_name)
        await member.edit(nick=new_nickname)
        user_data["users"][str(member.id)] = new_nickname
        if not available_ids:
            new_counter += 1
            available_ids.append(new_counter)
        user_data["counter"] = new_counter

    save_json(USER_DATA_PATH, user_data)

# Event when a member joins the server
@bot.event
async def on_member_join(member: discord.Member):
    if member.bot:
        # Rename bots to "BOT"
        await member.edit(nick="BOT | " + member.name)
    else:
        user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
        naming_convention = load_json(NAMING_CONVENTION_PATH, {"format": "{counter:03} | {display_name}"})
        naming_format = naming_convention["format"]
        
        guild = member.guild
        current_ids = {extract_id(m.display_name) for m in guild.members if extract_id(m.display_name) is not None}
        available_ids = sorted(set(range(1, user_data["counter"] + 1)) - current_ids)
        new_counter = max(current_ids, default=0) + 1

        new_id = available_ids.pop(0) if available_ids else new_counter
        new_nickname = naming_format.format(counter=new_id, display_name=member.display_name)
        await member.edit(nick=new_nickname)

        user_data["users"][str(member.id)] = new_nickname
        user_data["counter"] = new_counter

        save_json(USER_DATA_PATH, user_data)

# Event when a member leaves the server
@bot.event
async def on_member_remove(member: discord.Member):
    user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
    if str(member.id) in user_data["users"]:
        del user_data["users"][str(member.id)]
        save_json(USER_DATA_PATH, user_data)

# Slash command to display available commands
@bot.tree.command(name="list_commands", description="Show available commands.")
async def list_commands(interaction: discord.Interaction):
    command_list = "\n".join([f"/{command.name}: {command.description}" for command in bot.tree.get_commands()])
    await interaction.response.send_message(f"Available Commands:\n{command_list}")

# Slash command to manually organize all nicknames
@bot.tree.command(name="organize_nicknames", description="Organize all nicknames in the server.")
async def organize_nicknames(interaction: discord.Interaction):
    if interaction.guild:
        await organize_all_nicknames(interaction.guild)
        await interaction.response.send_message("Nicknames have been organized.")
    else:
        await interaction.response.send_message("This command can only be used in a server.")

# Run the bot with the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No valid DISCORD_TOKEN found. Bot cannot start.")
