import discord

name = "ready"
once = True

async def execute(bot):
    bot.logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    bot.logger.info(f"Connected to {len(bot.guilds)} guilds")
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        bot.logger.info(f"Synced {len(synced)} slash commands")
    except Exception as e:
        bot.logger.error(f"Failed to sync slash commands: {e}")
