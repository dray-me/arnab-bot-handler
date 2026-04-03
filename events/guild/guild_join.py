name = "guild_join"

async def execute(bot, guild):
    bot.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")
