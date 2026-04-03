import discord

name = "interaction"

async def execute(bot, interaction):
    if interaction.type == discord.InteractionType.application_command:
        command_name = interaction.data["name"]
        await bot.loader.command_manager.execute_command(interaction, command_name, "slash")
