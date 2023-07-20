from discord.ext import commands
import discord
import sqlite3
import requests
import os

# Cog = コマンドと処理を分離

class save(commands.Cog):
    def __init__(self, bot:discord.Client):
        self.bot = bot
        self.table_name = 'examdata'
    
    def _download_img(self, url, file_name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)
    
    def _make_dir(self, dir_name):
        if not(os.path.exists(f'./{self.table_name}')):
            os.makedirs(f'./{self.table_name}')
        if not(os.path.exists(f'./{self.table_name}/{dir_name}')):
            os.makedirs(f'./{self.table_name}/{dir_name}')
    
    def _convert_pdf(self, file_name):
        pass
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            # tableの作成
            db = sqlite3.connect('./database.sqlite')
            cur = db.cursor()
            table = f"""create table if not exists {self.table_name} 
            (id     integer primary key autoincrement,
            name    text,
            year    integer,
            path    text)"""
            cur.execute(table)
            print(f'{self.bot.user.name}のSaveCogが起動しました。')
        except Exception as e:
            print("Error Message: {}".format(e))

    # 保存(別の例)
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        try:
            if message.author.bot:
                return
            if message.content.startswith("!save"):
                await message.channel.send('!saveを検知しました')
                
                if not(message.attachments):
                    await message.channel.send("画像が添付されていません")
                    return
                
                # メッセージの内容を取得
                await message.channel.send("メッセージの内容を取得しました")
                class_name = message.content.split()[1]
                year = int(message.content.split()[2])

                # 画像の保存
                await message.channel.send("画像の保存を開始します")
                filename = message.attachments[0].filename
                url = message.attachments[0].url
                filedir = f"./{self.table_name}/{class_name}/{class_name}_{year}.png"
                self._make_dir(class_name)
                self._download_img(url, filedir)
                
                # databaseに保存
                await message.channel.send("databaseに保存します")
                con = sqlite3.connect('database.sqlite')
                cur = con.cursor()
                insert = f"insert into {self.table_name} (name, year, path) values (?, ?, ?)"
                cur.execute(insert, (class_name, year, filedir))
                con.commit()
                await message.channel.send('保存しました')
                
        except Exception as e:
            await message.channel.send("保存に失敗しました")
            await message.channel.send("Error Message: {}".format(e))
    
    # 保存(info.errorを使ってみたい)
    # @commands.command()
    # async def save(self, ctx, class_name:str, year:int):
    #     try:
    #         con = sqlite3.connect('database.sqlite')
    #         cur = con.cursor()
    #         insert = f"insert into {self.table_name} (name, year, path) values (?, ?, ?)"
    #         cur.execute(insert, (class_name, year, "hoge"))
    #         con.commit()
    #         await ctx.send('保存しました')
    #     except Exception as e:
    #         await ctx.send('保存に失敗しました')
    #         await ctx.send("Error Message: {}".format(e))
        

async def setup(bot:discord.Client):
    await bot.add_cog(save(bot))
