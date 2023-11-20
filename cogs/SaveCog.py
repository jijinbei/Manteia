from discord.ext import commands
import discord
import sqlite3
from discord.ext.commands.context import Context
import requests
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Cog = コマンドと処理を分離

class SaveCog(commands.Cog):
    def __init__(self, bot:discord.Client):
        self.bot = bot
        self.saved_path = "saved_images"
        self.db_path = self.saved_path + "/db.sqlite"
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            # ディレクトリの作成
            if not os.path.exists(self.saved_path):
                os.mkdir(self.saved_path)
            
            # databaseの作成
            db = sqlite3.connect(self.db_path)
            cur = db.cursor()
            table = f"""create table if not exists {self.saved_path} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cource TEXT,
                        year INTEGER,
                        path TEXT)"""
            cur.execute(table)
            print(f'{self.bot.user.name}のSaveCog起動成功')
        except Exception as e:
            print(f"SaveCog起動失敗\nError Type: {type(e).__name__}, Error Message: {e}")

    @commands.command(name='save', help="画像の保存")
    async def save_image(self, ctx, course: str, year: int):
        """画像の保存を行う命令

        Args:
            ctx (_type_): 
            course (str): 授業名
            year (int): 何年度の試験
        """
        if not ctx.message.attachments:
            await ctx.send('画像が添付されていません。')
            return
        
        attachment = ctx.message.attachments[0]
        print(ctx.message.attachments)
        print(attachment)
        filename = attachment.filename
        print(filename)
        url = attachment.url
        print(url)
        
        # 許可されるファイル形式
        allowed_extensions = ['pdf', 'png', 'jpeg', 'jpg']
        
        extension = filename.split('.')[-1].lower()
        
        if extension not in allowed_extensions:
            extention_error_embed = self._error_embed(f"{extension}は許可されていないファイル形式です。\n許可されるファイル形式は{allowed_extensions}です。")
            await ctx.send(embed=extention_error_embed)
            return
        
        # ファイル名
        filedir = f"{self.saved_path}/{course}/{course}_{year}.{extension}"
        
        # ディレクトリの作成
        os.makedirs(os.path.dirname(filedir), exist_ok=True)
        
        # 画像の保存
        response = requests.get(url)
        with open(filedir, "wb") as f:
            f.write(response.content)
        
        # databaseに保存
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        insert = f"insert into {self.saved_path} (cource, year, path) values (?, ?, ?)"
        cur.execute(insert, (course, year, filedir))
        con.commit()
        
        save_embed = self._create_embed("画像の保存", f"{course}_{year}.{extension}を保存しました。")
        await ctx.send(embed=save_embed)
    
    # エラー処理
    # @commands.Cog.listener()
    # async def cog_command_error(self, ctx: Context, error: Exception) -> None:
    #     embed = self._create_embed("エラー発生", f"Error Message: {error}")
    #     await ctx.send(embed=embed)
    
    def _convert_images_to_pdf(image_paths, output_pdf_path):
        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        
        for image_path in image_paths:
            image = Image.open(image_path)
            image_width, image_height = image.size
            c.setPageSize((image_width, image_height))
            c.drawImage(image_path, 0, 0, image_width, image_height)
            c.showPage()
        c.save()
    
    def _create_embed(self, title, description):
        embed = discord.Embed(title=title, description=description, color=0x00ff00)
        return embed
    
    def _error_embed(self, description):
        embed = discord.Embed(title="エラー発生", description=description, color=0xff0000)
        return embed

async def setup(bot:discord.Client):
    await bot.add_cog(SaveCog(bot))
