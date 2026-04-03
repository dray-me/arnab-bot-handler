name = "guild_leave"

async def execute(bot, guild):
    bot.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")
