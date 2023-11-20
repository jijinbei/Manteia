from discord.ext import commands
import discord
import urllib.request
import sqlite3

def tenpu_image_download(url):
    pass

class FileHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のFileHandlerCogが起動しました。')
    
    # !upload
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        try:
            if message.author.bot:
                return
            if message.content.startswith("!output"):
                await message.channel.send('!outputを検知しました')
        except Exception as e:
            print("Error Message: {}".format(e))
            

async def setup(bot):
    await bot.add_cog(FileHandlerCog(bot))
