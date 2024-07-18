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
    try:
        synced = await bot.tree.sync()  # Sync the slash commands with Discord
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command to organize nicknames based on a numbering convention
@bot.tree.command(name="organize_nicknames", description="Organize nicknames based on a numbering convention.")
async def organize_nicknames(interaction: discord.Interaction):
    user_data = load_json(USER_DATA_PATH, {"counter": 0, "users": {}})
    naming_convention = load_json(NAMING_CONVENTION_PATH, {"format": "{counter:03} | {display_name}"})
    naming_format = naming_convention["format"]

    # Function to parse ID from nickname
    def extract_id(nickname):
        match = re.match(r"(\d{3})", nickname)
        if match:
            return int(match.group(1))
        return None

    # Ensure the bot has the required permissions
    if not interaction.guild.me.guild_permissions.manage_nicknames:
        await interaction.response.send_message("I do not have the `Manage Nicknames` permission.", ephemeral=True)
        return

    members = interaction.guild.members
    current_ids = {extract_id(member.display_name) for member in members if extract_id(member.display_name) is not None}
    max_id = max(current_ids, default=0)
    
    # Filter and sort members
    members_with_convention = []
    members_without_convention = []
    
    for member in members:
        if extract_id(member.display_name) is not None:
            members_with_convention.append(member)
        else:
            members_without_convention.append(member)

    # Sort members without convention
    members_without_convention.sort(key=lambda m: m.display_name)

    # Assign IDs to members without convention
    available_ids = set(range(1, max_id + 2)) - current_ids
    new_counter = max_id + 1
    user_data["counter"] = new_counter

    for member in members_without_convention:
        new_id = min(available_ids, default=new_counter)
        new_nickname = naming_format.format(counter=new_id, display_name=member.display_name)
        await member.edit(nick=new_nickname)
        user_data["users"][str(member.id)] = new_nickname
        available_ids.discard(new_id)
        if not available_ids:
            new_counter += 1
            available_ids.add(new_counter)
        user_data["counter"] = new_counter

    # Save updated user data
    save_json(USER_DATA_PATH, user_data)

    await interaction.response.send_message("Nicknames have been organized and updated.")

# Slash command to display available commands
@bot.tree.command(name="list_commands", description="Show available commands.")
async def list_commands(interaction: discord.Interaction):
    command_list = "\n".join([f"/{command.name}: {command.description}" for command in bot.tree.get_commands()])
    await interaction.response.send_message(f"Available Commands:\n{command_list}")

# Run the bot with the Discord token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("No valid DISCORD_TOKEN found. Bot cannot start.")
