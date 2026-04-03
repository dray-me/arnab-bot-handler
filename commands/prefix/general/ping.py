import discord

metadata = {
    "name": "ping",
    "description": "Check the bot's latency",
    "category": "general",
    "cooldown": 5
}

async def execute(bot, ctx, *args):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")
