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
    
    @commands.command(name='exams', help='指定されたコースの全ての年度の試験問題を取得')
    async def get_all_years(self, ctx, course: str):
        years = self._get_years_for_course(course)
        if not years:
            not_found_embed = error_embed(f"{course}に関連する試験問題は見つかりませんでした。")
            await ctx.send(embed=not_found_embed)
            return
        
        files = []
        for year in years:
            file_path = f"{self.saved_path}/{course}/{course}_{year}.pdf"
            if os.path.exists(file_path):
                files.append(discord.File(file_path))
        
        course_description = f"{years[0]}年度から{years[-1]}年度の試験問題"
        course_embed = create_embed(f"{course}の試験問題",course_description)
        await ctx.send(embed=course_embed)
        await ctx.send(files=files)
    
    @commands.command(name='list', help='利用可能な試験と年度の一覧を表示')
    async def list_courses(self, ctx):
        courses = self._get_courses_and_years()
        
        if not courses:
            await ctx.send("試験はありません。")
            return
        
        embed = discord.Embed(title="試験の授業名と年度の一覧", description="現在保存されている授業と年度の一覧は次の通りです", color=0x00ff00)
        for course, years in courses.items():
            embed.add_field(name=course, value=", ".join(map(str, years)), inline=False)
        
        await ctx.send(embed=embed)
    
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
    
    def _get_courses_and_years(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT course, year FROM exam_table")
        rows = cur.fetchall()
        con.close()
        
        courses = {}
        for row in rows:
            course, year = row
            if course in courses:
                courses[course].append(year)
            else:
                courses[course] = [year]
        
        return courses

async def setup(bot):
    await bot.add_cog(FileHandlerCog(bot))