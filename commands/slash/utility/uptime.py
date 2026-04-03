metadata = {
    "name": "uptime",
    "description": "Check bot uptime",
    "category": "utility"
}

async def execute(bot, interaction):
    await interaction.response.send_message("Uptime: 100% (Mock)")
