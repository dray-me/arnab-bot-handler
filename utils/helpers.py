import discord

def create_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(title=title, description=description, color=color)
