import os
import importlib
import sys
from commands.manager import CommandManager

class Loader:
    def __init__(self, bot):
        self.bot = bot
        self.command_manager = CommandManager(bot)

    async def load_all(self):
        await self.load_events()
        await self.load_commands()
        await self.load_functions()

    async def load_events(self):
        event_dirs = ["events/client", "events/guild", "events/message"]
        for directory in event_dirs:
            if not os.path.exists(directory):
                continue
            for filename in os.listdir(directory):
                if filename.endswith(".py"):
                    module_path = f"{directory.replace('/', '.')}.{filename[:-3]}"
                    await self.load_event(module_path)

    async def load_event(self, module_path):
        try:
            if module_path in sys.modules:
                importlib.reload(sys.modules[module_path])
            module = importlib.import_module(module_path)
            
            name = getattr(module, "name", None)
            execute = getattr(module, "execute", None)
            once = getattr(module, "once", False)

            if name and execute:
                if once:
                    self.bot.once(name)(execute)
                else:
                    self.bot.event(execute)
                self.bot.logger.info(f"Loaded event: {name}")
        except Exception as e:
            self.bot.logger.error(f"Failed to load event {module_path}: {e}")

    async def load_commands(self):
        # Slash commands
        slash_dir = "commands/slash"
        for root, dirs, files in os.walk(slash_dir):
            for filename in files:
                if filename.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, filename), ".")
                    module_path = rel_path.replace(os.sep, ".")[:-3]
                    await self.command_manager.register_slash_command(module_path)

        # Prefix commands
        prefix_dir = "commands/prefix"
        for root, dirs, files in os.walk(prefix_dir):
            for filename in files:
                if filename.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, filename), ".")
                    module_path = rel_path.replace(os.sep, ".")[:-3]
                    await self.command_manager.register_prefix_command(module_path)

    async def load_functions(self):
        from functions.scheduler import Scheduler
        self.bot.scheduler = Scheduler(self.bot)
        await self.bot.scheduler.load_functions()
