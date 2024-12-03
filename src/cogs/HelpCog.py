from discord.ext import commands
from lib.embed import create_embed

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 起動確認
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のHelpCogが起動しました。')
    
    @commands.command(name='help', help='ヘルプを表示')
    async def help(self, ctx):
        help_embed = create_embed("ヘルプ", "試験問題を検索するためのBotです。")
        help_embed.add_field(name="!save", value="画像を保存します。!save (授業名) (年度) + 画像添付\n使用例) !save 統計力学 2003 + 統計力学のテストを添付", inline=False)
        help_embed.add_field(name="!exams", value="指定されたコースの全ての年度の試験問題を取得します。\n使用例) !exams 統計力学", inline=False)
        help_embed.add_field(name="!list", value="利用可能な試験と年度の一覧を表示します。", inline=False)
        help_embed.add_field(name="!help", value="ヘルプを表示します。", inline=False)
        await ctx.send(embed=help_embed)
        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
