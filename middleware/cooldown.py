import discord

async def check_cooldown(bot, ctx_or_interaction, metadata):
    cooldown = metadata.get("cooldown", 0)
    if cooldown <= 0:
        return True, None
    
    # Simple in-memory cooldown for demo
    # In production, use Redis or a database
    if not hasattr(bot, "_cooldowns"):
        bot._cooldowns = {}
    
    user_id = ctx_or_interaction.user.id if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author.id
    cmd_name = metadata["name"]
    key = f"{user_id}:{cmd_name}"
    
    import time
    now = time.time()
    last_used = bot._cooldowns.get(key, 0)
    
    if now - last_used < cooldown:
        remaining = round(cooldown - (now - last_used), 1)
        return False, f"Slow down! You can use this command again in {remaining}s."
    
    bot._cooldowns[key] = now
    return True, None
