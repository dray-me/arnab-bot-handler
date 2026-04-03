import discord
import time

metadata = {
    "name": "ping",
    "description": "Check the bot's latency",
    "category": "general",
    "cooldown": 5
}

async def execute(bot, ctx_or_interaction):
    latency = round(bot.latency * 1000)
    message = f"🏓 Pong! Latency: {latency}ms"
    
    if hasattr(ctx_or_interaction, "response"):
        await ctx_or_interaction.response.send_message(message)
    else:
        await ctx_or_interaction.send(message)
