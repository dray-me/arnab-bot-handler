import discord
from discord.ext import commands
import importlib
import sys

class CommandManager:
    def __init__(self, bot):
        self.bot = bot
        self.slash_commands = {}
        self.prefix_commands = {}

    async def register_slash_command(self, module_path):
        try:
            if module_path in sys.modules:
                importlib.reload(sys.modules[module_path])
            module = importlib.import_module(module_path)
            
            metadata = getattr(module, "metadata", None)
            execute = getattr(module, "execute", None)

            if metadata and execute:
                name = metadata.get("name")
                self.slash_commands[name] = {
                    "metadata": metadata,
                    "execute": execute,
                    "module_path": module_path
                }
                self.bot.logger.info(f"Registered slash command: {name}")
        except Exception as e:
            self.bot.logger.error(f"Failed to register slash command {module_path}: {e}")

    async def register_prefix_command(self, module_path):
        try:
            if module_path in sys.modules:
                importlib.reload(sys.modules[module_path])
            module = importlib.import_module(module_path)
            
            metadata = getattr(module, "metadata", None)
            execute = getattr(module, "execute", None)

            if metadata and execute:
                name = metadata.get("name")
                
                @self.bot.command(name=name, help=metadata.get("description"))
                async def cmd(ctx, *args):
                    await self.execute_command(ctx, name, "prefix", *args)
                
                self.prefix_commands[name] = {
                    "metadata": metadata,
                    "execute": execute,
                    "module_path": module_path
                }
                self.bot.logger.info(f"Registered prefix command: {name}")
        except Exception as e:
            self.bot.logger.error(f"Failed to register prefix command {module_path}: {e}")

    async def execute_command(self, ctx_or_interaction, name, type, *args):
        cmd_data = self.slash_commands.get(name) if type == "slash" else self.prefix_commands.get(name)
        if not cmd_data:
            return

        metadata = cmd_data["metadata"]
        execute = cmd_data["execute"]

        # Middleware Pipeline
        from middleware.rate_limit import check_rate_limit
        from middleware.cooldown import check_cooldown
        from middleware.permissions import check_permissions
        from middleware.roles import check_roles
        from middleware.dev_mode import check_dev_mode

        middlewares = [
            check_rate_limit,
            check_cooldown,
            check_permissions,
            check_roles,
            check_dev_mode
        ]

        for middleware in middlewares:
            passed, message = await middleware(self.bot, ctx_or_interaction, metadata)
            if not passed:
                if message:
                    if hasattr(ctx_or_interaction, "response"):
                        await ctx_or_interaction.response.send_message(message, ephemeral=True)
                    else:
                        await ctx_or_interaction.send(message)
                return

        try:
            await execute(self.bot, ctx_or_interaction, *args)
            # Log usage
            await self.log_command_usage(ctx_or_interaction, name)
        except Exception as e:
            from core.error_handler import handle_command_error
            await handle_command_error(self.bot, ctx_or_interaction, e)

    async def log_command_usage(self, ctx_or_interaction, name):
        webhook_url = self.bot.config["logging"].get("commandLogsChannelId")
        if not webhook_url or webhook_url == "COMMAND_WEBHOOK_URL_HERE":
            return
        
        user = ctx_or_interaction.user if hasattr(ctx_or_interaction, "user") else ctx_or_interaction.author
        guild = ctx_or_interaction.guild
        
        async with self.bot.session.post(webhook_url, json={
            "content": f"Command `{name}` used by {user} (ID: {user.id}) in {guild} (ID: {guild.id})"
        }) as resp:
            pass
