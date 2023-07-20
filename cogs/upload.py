from discord.ext import commands
import urllib.request
import sqlite3

def tenpu_image_download(url):
    pass

class upload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のUploadCogが起動しました。')

async def setup(bot):
    await bot.add_cog(upload(bot))
