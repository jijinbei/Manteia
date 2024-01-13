from discord.ext import commands
import discord
import os
import sqlite3
import traceback
from lib.embed import create_embed, error_embed
from lib.rename import cource_rename

db_path = "exams/db.sqlite"

class FileHandlerCog(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
    
    # 初期設定
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のFileHandlerCogが起動しました。')
    
    @commands.command(name='exams', help='指定されたコースの全ての年度の過去問を取得')
    async def output_exams(self, ctx, course: str):
        renamed_course = cource_rename(course)
        datas = get_data_for_course(renamed_course) # [(year, path), (year, path), ...]
        if not datas:
            await ctx.send(embed=error_embed(f"{renamed_course}に関連する過去問は見つかりませんでした。"))
            return
        
        files = []
        years = []
        for data in datas:
            year, file_path = data
            # ファイルが存在するか確認
            if os.path.exists(file_path):
                files.append(discord.File(file_path))
                years.append(year)
        
        # メッセージ
        if len(years) == 1:
            course_description = f"{years[0]}年度の過去問"
        else:
            course_description = f"{min(years)}年度から{max(years)}年度の過去問"
        
        course_embed = create_embed(f"{renamed_course}の試験問題",course_description)
        await ctx.send(embed=course_embed)
        await ctx.send(files=files)
    
    @commands.command(name='list', help='利用可能な過去問と年度の一覧を表示')
    async def list_courses(self, ctx: commands.Context):
        courses = get_courses_and_years()
        
        if not courses:
            await ctx.send("過去問はありません。")
            return
        embed = create_embed("過去問の授業名と年度の一覧", "現在保存されている授業と年度の一覧は次の通りです")
        
        for course, years in courses.items():
            value_str = ",  ".join([f"{year}x{count}" if count > 1 else f"{year}" for year, count in years.items()])
            embed.add_field(name=course, value=value_str, inline=False)
        await ctx.send(embed=embed)

def get_data_for_course(course):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(f"SELECT year, path FROM exam_table WHERE course = ?", (course,))
    data = cur.fetchall()
    print(data)
    con.close()
    
    return data  # 年度のリストを返す ex)[(2020, 3), (2021, 1)]

def get_courses_and_years():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT course, year FROM exam_table")
    rows = cur.fetchall()
    con.close()
    courses = {}
    
    for row in rows:
        course, year = row
        if course in courses: # 既にある授業なら
            if year in courses[course]:
                courses[course][year] += 1 # 既にある年度ならカウントを増やす
            else:
                courses[course][year] = 1 # 新しい年度を追加
        else:
            courses[course] = {year: 1}
    
    return courses

async def setup(bot):
    await bot.add_cog(FileHandlerCog(bot))