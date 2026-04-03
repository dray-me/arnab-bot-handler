import discord

async def check_permissions(bot, ctx_or_interaction, metadata):
    user = ctx_or_interaction.user if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author
    
    # Owner Only
    if metadata.get("ownerOnly") and str(user.id) != str(bot.config["bot"]["ownerId"]):
        return False, "This command is restricted to the bot owner."
    
    # Admin Only
    if metadata.get("adminOnly") and str(user.id) not in bot.config["bot"]["admins"]:
        return False, "This command is restricted to bot admins."
    
    # User Permissions
    user_perms = metadata.get("userPermissions", [])
    if user_perms and hasattr(ctx_or_interaction, "channel"):
        perms = ctx_or_interaction.channel.permissions_for(user)
        for perm in user_perms:
            if not getattr(perms, perm, False):
                return False, f"You need the `{perm}` permission to use this command."
                
    return True, None
