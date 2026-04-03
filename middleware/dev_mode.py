async def check_dev_mode(bot, ctx_or_interaction, metadata):
    if metadata.get("devOnly"):
        user = ctx_or_interaction.user if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author
        if str(user.id) != str(bot.config["bot"]["ownerId"]):
            return False, "This command is currently in development mode."
    return True, None
