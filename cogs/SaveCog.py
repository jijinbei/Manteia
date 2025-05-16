from discord.ext import commands
import discord
import os
from io import BytesIO
import requests
import sqlite3
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import traceback
from lib.embed import create_embed, error_embed
from lib.rename import cource_rename

saved_path = "exams"
db_path = "exams/db.sqlite"

class SaveCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            # ディレクトリの作成
            if not os.path.exists(saved_path):
                os.mkdir(saved_path)
            
            # databaseの作成
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            table = f"""CREATE TABLE IF NOT EXISTS exam_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        course TEXT,
                        year INTEGER,
                        path TEXT)"""
            cur.execute(table)
            con.close()
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
        
        # 入力ファイル  
        attachments = ctx.message.attachments
        # 出力ファイル
        course = cource_rename(course)
        print(course)
        filename = generate_unique_filename(course, year)
        output_pdf_path = f"{saved_path}/{course}/{filename}"
        
        if len(attachments) == 0:
            embed = error_embed("画像が添付されていません。")
            await ctx.send(embed=embed)
            return
        
        if '.pdf' in attachments[0].filename:# pdfならそのまま保存
            save_pdf(attachments[0].url, output_pdf_path)
        else: # 画像ならpdfに変換して保存
            # 画像のダウンロード
            images = []
            for attachment in attachments:
                image = await download_image(attachment, ctx)
                # 画像が適正でない場合抜け出す
                if image is None:
                    return
                images.append(image)
            
            # 画像ならpdfに変換して保存
            convert_images_to_pdf(images, output_pdf_path)
        
        # databaseに保存
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO exam_table (course, year, path) VALUES (?, ?, ?)", (course, year, output_pdf_path))
        con.commit()
        con.close()
        
        save_embed = create_embed("画像の保存", f"{filename}を保存しました。")
        await ctx.send(embed=save_embed)

# 画像をpdfに変換して保存
def convert_images_to_pdf(images, output_pdf_path):
    try:
        # 保存先の作成
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        
        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        for image in images:
            image_width, image_height = image.size
            c.setPageSize((image_width, image_height))
            c.drawInlineImage(image, 0, 0, image_width, image_height)
            c.showPage()
        c.save()
    except Exception as e:
        print(f"エラー発生: {e}")
        traceback.print_exc()

# pdfを保存
def save_pdf(url, output_pdf_path):
    # 保存先の作成
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    response = requests.get(url)
    with open(output_pdf_path, 'wb') as f:
        f.write(response.content)

# 画像のダウンロード
async def download_image(attachment, ctx):
    url = attachment.url
    filename = attachment.filename
    
    # 許可されるファイル形式
    allowed_extensions = ['pdf', 'png', 'jpeg', 'jpg']
    
    try:
        # 拡張子の確認
        extension = filename.split('.')[-1].lower()
        if extension not in allowed_extensions: # 画像が適正でない場合
            extention_error_embed = error_embed(f"{extension}は許可されていないファイル形式です。\n許可されるファイル形式は{allowed_extensions}です。")
            await ctx.send(embed=extention_error_embed)
            return
        else:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            return image
    except Exception as e:
        print(f"エラー発生: {e}")
        traceback.print_exc()

# ファイル名の生成
def generate_unique_filename(course, year):
    base_filename = f"{course}_{year}"
    
    # データベースで既存のファイル名を確認
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    cur.execute("SELECT COUNT(*) FROM exam_table WHERE course = ? AND year = ?", (course, year))
    match_num = cur.fetchone()[0]
    
    if match_num == 0:  # ファイルが存在しない場合
        con.close()
        return f"{base_filename}.pdf"
    else:
        con.close()
        return f"{base_filename}_{match_num}.pdf"

## 動くか確認

async def setup(bot:discord.Client):
    await bot.add_cog(SaveCog(bot))
