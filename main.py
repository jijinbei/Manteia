import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.app_commands import CommandTree

load_dotenv()
intents = discord.Intents.all()  # 全ての権限を有効にする
intents.members = True  # メンバーを取得するために必要
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # !で始まるコマンドをトリガーにする

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
