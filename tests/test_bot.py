import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import discord
from discord.ext import commands
from unittest.mock import AsyncMock, patch, MagicMock

# Assuming your bot code is in a file named 'bot.py'
from bot import bot, on_member_join, on_member_update

@pytest.fixture
def bot_instance():
    return bot

@pytest.fixture
def guild():
    guild = MagicMock(discord.Guild)
    guild.id = 123456789
    guild.members = []
    return guild

@pytest.fixture
def member(guild):
    member = MagicMock(discord.Member)
    member.id = 987654321
    member.name = "TestUser"
    member.guild = guild
    return member

@pytest.fixture
def bot_member(guild):
    bot_member = MagicMock(discord.Member)
    bot_member.id = 123123123
    bot_member.name = "TestBot"
    bot_member.bot = True
    bot_member.guild = guild
    return bot_member

@pytest.mark.asyncio
async def test_on_member_join_member(bot_instance, member):
    with patch('bot.save_user_data', new_callable=AsyncMock), \
         patch.object(bot_instance, 'get_guild', return_value=member.guild):

        await on_member_join(member)

        assert member.edit.called
        assert member.edit.call_args[1]['nick'] == '001 | TestUser'

@pytest.mark.asyncio
async def test_on_member_join_bot(bot_instance, bot_member):
    with patch('bot.save_user_data', new_callable=AsyncMock), \
         patch.object(bot_instance, 'get_guild', return_value=bot_member.guild):

        await on_member_join(bot_member)

        assert bot_member.edit.called
        assert bot_member.edit.call_args[1]['nick'] == 'BOT | TestBot'

@pytest.mark.asyncio
async def test_on_member_update_nickname_change(bot_instance, member):
    before = member
    after = MagicMock(discord.Member)
    after.id = member.id
    after.name = member.name
    after.guild = member.guild
    after.nick = "WrongNickname"

    user_data = {"counter": 1, "users": {str(member.id): "001 | TestUser"}}

    with patch('bot.user_data', user_data):
        await on_member_update(before, after)

        assert after.edit.called
        assert after.edit.call_args[1]['nick'] == '001 | TestUser'

@pytest.mark.asyncio
async def test_on_member_update_no_change(bot_instance, member):
    before = member
    after = member

    user_data = {"counter": 1, "users": {str(member.id): "001 | TestUser"}}

    with patch('bot.user_data', user_data):
        await on_member_update(before, after)

        assert not after.edit.called

@pytest.mark.asyncio
async def test_on_member_update_key_error(bot_instance, member):
    before = member
    after = MagicMock(discord.Member)
    after.id = member.id
    after.name = member.name
    after.guild = member.guild
    after.nick = "001 | TestUser"

    user_data = {"counter": 1, "users": {}}

    with patch('bot.user_data', user_data):
        await on_member_update(before, after)

        assert not after.edit.called

@pytest.mark.asyncio
async def test_on_command_error(bot_instance):
    ctx = MagicMock(discord.ext.commands.Context)
    error = commands.CommandNotFound()

    with patch.object(ctx, 'send', new_callable=AsyncMock) as mock_send:
        await bot_instance.on_command_error(ctx, error)

        mock_send.assert_called_once_with("Command not found.")
