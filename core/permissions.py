import discord

async def has_permissions(bot, user, permissions):
    if not permissions:
        return True
    
    # Check if user is owner
    if str(user.id) == str(bot.config["bot"]["ownerId"]):
        return True
        
    # Check if user is admin
    if str(user.id) in bot.config["bot"]["admins"]:
        return True
        
    return False # Placeholder for more complex permission logic
