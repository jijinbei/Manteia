from discord.ext import commands
from discord import Embed, File

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # 起動確認
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}のHelpCogが起動しました。')

    # ヘルプ機能
    @commands.command()
    async def help(self, message):
        if message.author.bot:
            return
        else:
            embed = Embed(title="ヘルプ機能", description="コマンドの説明。最初に『!』をつけてください。", color=0xff9300)
            embed.add_field(name="!save", value="添付ファイルから画像の保存をする ex)!save 量子力学2 2022 + 添付ファイル", inline=False)
            embed.add_field(name="!Support", value="管理人にサポートメッセージを送る(DM)", inline=False)
            embed.add_field(name="!cleanup (※管理人のみ)", value="テキストチャンネルのメッセージをすべて消す", inline=False)
            fname="fig.jpeg" # アップロードするときのファイル名 自由に決めて良いですが、拡張子を忘れないように
            file = File(fp="fig.jpeg",filename=fname,spoiler=False) # ローカル画像からFileオブジェクトを作成
            embed.set_image(url=f"attachment://{fname}") # embedに画像を埋め込むときのURLはattachment://ファイル名
            await message.channel.send(file=file, embed=embed) # ファイルとembedを両方添えて送信する

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
