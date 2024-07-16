import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bot
# Load environment variables from .env file (adjust path as needed)
load_dotenv(dotenv_path="../.env")

# Mocking bot.py imports
with patch('discord.Client') as mock_client:
    mock_bot = MagicMock(spec=commands.Bot)
    mock_client.return_value = mock_bot
    mock_bot.user = MagicMock(spec=discord.User)

    import bot  # Import your bot.py module after mocking

async def test_bot_on_ready():
    assert bot.bot.on_ready is not None
    await bot.bot.on_ready()  # Simulate bot ready event
    assert "NuName bot" in bot.logger.handlers[0].messages[0]  # Adjust as per your logging configuration

async def test_bot_on_member_join():
    mock_member = MagicMock(spec=discord.Member)
    mock_member.id = "1234567890"
    mock_member.name = "TestMember"
    
    assert bot.bot.on_member_join is not None
    await bot.bot.on_member_join(mock_member)  # Simulate member join event
    assert f'NuName assigned nickname' in bot.logger.handlers[0].messages[1]  # Adjust as per your logging configuration

async def test_bot_on_member_remove():
    mock_member = MagicMock(spec=discord.Member)
    mock_member.name = "TestMember"

    assert bot.bot.on_member_remove is not None
    await bot.bot.on_member_remove(mock_member)  # Simulate member remove event
    assert f'{mock_member.name} has left the server.' in bot.logger.handlers[0].messages[2]  # Adjust as per your logging configuration

async def test_bot_on_member_update():
    mock_before = MagicMock(spec=discord.Member)
    mock_after = MagicMock(spec=discord.Member)
    mock_before.nick = "OldNick"
    mock_after.nick = "NewNick"
    mock_after.id = "1234567890"

    assert bot.bot.on_member_update is not None
    await bot.bot.on_member_update(mock_before, mock_after)  # Simulate member update event
    assert f'NuName reverted nickname change' in bot.logger.handlers[0].messages[3]  # Adjust as per your logging configuration

async def test_bot_on_command_error():
    mock_ctx = MagicMock(spec=commands.Context)
    mock_error = commands.CommandNotFound("Command not found")

    assert bot.bot.on_command_error is not None
    await bot.bot.on_command_error(mock_ctx, mock_error)  # Simulate command error event
    assert "Command not found." in bot.logger.handlers[0].messages[4]  # Adjust as per your error handling

# Run all tests
async def run_tests():
    await test_bot_on_ready()
    await test_bot_on_member_join()
    await test_bot_on_member_remove()
    await test_bot_on_member_update()
    await test_bot_on_command_error()

if __name__ == "__main__":
    asyncio.run(run_tests())
