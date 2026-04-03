metadata = {
    "name": "ban",
    "description": "Ban a user",
    "category": "moderation",
    "userPermissions": ["ban_members"],
    "botPermissions": ["ban_members"]
}

async def execute(bot, interaction):
    # Implementation here
    await interaction.response.send_message("Ban command executed (Mock)")
