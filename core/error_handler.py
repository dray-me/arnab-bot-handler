import discord

async def handle_command_error(bot, ctx_or_interaction, error):
    bot.logger.error(f"Command error: {error}")
    
    message = "An unexpected error occurred while executing this command."
    
    if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
        message = f"Cooldown! Try again in {round(error.retry_after, 2)}s."
    
    if hasattr(ctx_or_interaction, "response"):
        if not ctx_or_interaction.response.is_done():
            await ctx_or_interaction.response.send_message(message, ephemeral=True)
        else:
            await ctx_or_interaction.followup.send(message, ephemeral=True)
    else:
        await ctx_or_interaction.send(message)

    # Log to webhook
    webhook_url = bot.config["logging"].get("errorLogs")
    if webhook_url and webhook_url != "YOUR_ERROR_WEBHOOK_URL_HERE":
        # Send error details to webhook
        pass

async def handle_global_error(bot, event, *args, **kwargs):
    bot.logger.error(f"Global error in {event}: {args} {kwargs}")
