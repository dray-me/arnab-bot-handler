metadata = {
    "name": "kick",
    "description": "Kick a user",
    "category": "moderation",
    "userPermissions": ["kick_members"]
}

async def execute(bot, ctx, *args):
    await ctx.send("Kick command executed (Mock)")
