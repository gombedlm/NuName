import discord
from discord.ext import commands
import json
import os
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler('bot.log')
                    ])

logger = logging.getLogger('discord')

# Define intents
intents = discord.Intents.default()
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Load user data
user_data = {"counter": 0, "users": {}}
if os.path.exists('user_data.json'):
    try:
        with open('user_data.json', 'r') as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading user_data.json: {e}")

# Save user data
def save_user_data():
    try:
        with open('user_data.json', 'w') as f:
            json.dump(user_data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving user_data.json: {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info(f'NuName bot {bot.user} is ready.')
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

    save_user_data()

# Event: Member joins the server
@bot.event
async def on_member_join(member):
    try:
        if member.bot:
            new_nickname = f'BOT | {member.name}'
            await member.edit(nick=new_nickname)
            logger.info(f'Assigned bot nickname {new_nickname} to {member.name}')
            return

        while user_data["counter"] + 1 in user_data["users"]:
            user_data["counter"] += 1

        user_data["counter"] += 1
        user_data["users"][str(member.id)] = f'{user_data["counter"]:03} | {member.name}'
        save_user_data()

        new_nickname = f'{user_data["counter"]:03} | {member.name}'
        await member.edit(nick=new_nickname)
        logger.info(f'Assigned nickname {new_nickname} to {member.name}')

        await member.send(f"Welcome to the server, {member.name}! Your ID-like nickname is now: {new_nickname}")

    except discord.Forbidden:
        logger.error(f"Permission error: Cannot change nickname for {member.name}")
    except Exception as e:
        logger.error(f"Error in on_member_join: {e}")

# Event: Member leaves the server
@bot.event
async def on_member_remove(member):
    logger.info(f'{member.name} has left the server.')

# Event: Member nickname update
@bot.event
async def on_member_update(before, after):
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

# Slash command to list available commands
@bot.tree.command(name="NuName-Commands", description="List all commands currently available")
async def slash_command(interaction: discord.Interaction):
    commands_list = [
        ("!help", "Displays this help message."),
        ("!ping", "Replies with 'Pong!' to test the bot's responsiveness."),
        ("!stats", "Shows statistics about the current server."),
        # Add more commands as necessary
    ]
    
    command_descriptions = "\n".join(f"{cmd}: {desc}" for cmd, desc in commands_list)
    response = f"**Available Commands:**\n{command_descriptions}"

    await interaction.response.send_message(response)

# Example command for testing
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

# Example command for server statistics
@bot.command(name="stats")
async def stats(ctx):
    member_count = len(ctx.guild.members)
    await ctx.send(f"This server has {member_count} members.")

# Run the bot
try:
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
except Exception as e:
    logger.error("No valid DISCORD_TOKEN found. Bot cannot start.")

# Event: Handle disconnect
@bot.event
async def on_disconnect():
    logger.info("Closing aiohttp client session...")
    await bot.http.close()

# Ensure the event loop is closed properly
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    asyncio.get_event_loop().close()
