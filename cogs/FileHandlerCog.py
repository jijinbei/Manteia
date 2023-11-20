from discord.ext import commands
import discord
import os
import sqlite3
import traceback
from lib.embed import create_embed, error_embed

class FileHandlerCog(commands.Cog):
    def __init__(self, bot, saved_path="saved_images", db_name="db.sqlite"):
        self.bot = bot
        self.saved_path = saved_path
        self.db_path = saved_path + "/" + db_name
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のFileHandlerCogが起動しました。')
    
    @commands.command(name='exams', help='指定されたコースの全ての年度のPDFを取得')
    async def get_all_years(self, ctx, course: str):
        years = self._get_years_for_course(course)
        if not years:
            not_found_embed = error_embed(f"{course}に関連するPDFは見つかりませんでした。")
            await ctx.send(embed=not_found_embed)
            return
        
        files = []
        for year in years:
            file_path = f"{self.saved_path}/{course}/{course}_{year}.pdf"
            if os.path.exists(file_path):
                files.append(discord.File(file_path))
        
        course_description = f"{years[0]}年度から{years[-1]}年度の問題"
        course_embed = create_embed(f"{course}の問題",course_description)
        await ctx.send(embed=course_embed)
        await ctx.send(files=files)
    
    def _get_years_for_course(self, course):
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(f"SELECT DISTINCT year FROM exam_table WHERE course = ?", (course,))
            years = cur.fetchall()
            con.close()
            return [year[0] for year in years]  # 年度のリストを返す
        except Exception as e:
            print(f"エラー発生: {e}")
            traceback.print_exc()  # スタックトレースの出力

async def setup(bot):
    await bot.add_cog(FileHandlerCog(bot))