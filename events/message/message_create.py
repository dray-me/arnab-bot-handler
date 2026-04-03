import discord

name = "message"

async def execute(bot, message):
    if message.author.bot:
        return
    
    # Prefix commands are handled by discord.py's internal command handler
    # but we can add custom logic here if needed
    await bot.process_commands(message)
