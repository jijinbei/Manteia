import discord

def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=0x00ff00)
    return embed

def error_embed(description):
    embed = discord.Embed(title="エラー発生", description=description, color=0xff0000)
    return embed
