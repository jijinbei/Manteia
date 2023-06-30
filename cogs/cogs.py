from discord.ext import commands
import sqlite3

# Cog = コマンドと処理を分離

class cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect('database.sqlite')
        # tableの作成
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS pastexam (id INTEGER, class STRING)')
        
        print(f'{self.bot.user.name}が起動しました。')

    # ping pong
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')
    
    # 保存
    @commands.command()
    async def save(self, ctx, id, class_name):
        db = sqlite3.connect('database.sqlite')
        cur = db.cursor()
        cur.execute('INSERT INTO pastexam VALUES (?, ?)', (id, class_name))
        await ctx.send('保存しました')


async def setup(bot):
    await bot.add_cog(cogs(bot))
