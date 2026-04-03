async def check_roles(bot, ctx_or_interaction, metadata):
    required_roles = metadata.get("requiredRoles", [])
    if not required_roles:
        return True, None
        
    member = ctx_or_interaction.user if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author
    if not hasattr(member, "roles"):
        return True, None # Not in a guild
        
    for role_id in required_roles:
        if not any(str(r.id) == str(role_id) for r in member.roles):
            return False, f"You need a specific role to use this command."
            
    return True, None
