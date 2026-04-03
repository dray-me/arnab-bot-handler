import discord
from discord.ext import commands
import os
from core.loader import Loader
from core.logger import setup_logger
from core.hot_reload import HotReloader
from core.intents import get_intents
from database.mongo import MongoManager

class ArnabBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger()
        
        # Dynamic intents
        intents = get_intents()
        
        super().__init__(
            command_prefix=config["prefix"]["value"],
            intents=intents,
            help_command=None
        )
        
        self.loader = Loader(self)
        self.db = MongoManager(config["database"]["mongodbUrl"]) if config["database"].get("mongodbUrl") else None
        self.reloader = HotReloader(self)

    async def setup_hook(self):
        self.logger.info("Initializing systems...")
        
        # Connect to DB
        if self.db:
            await self.db.connect()
            self.logger.info("MongoDB connected.")

        # Load everything
        await self.loader.load_all()
        
        # Start hot reloader
        self.reloader.start()
        self.logger.info("Hot reloader active.")

    async def start_bot(self):
        token = self.config["bot"]["token"]
        if not token or token == "YOUR_BOT_TOKEN_HERE":
            self.logger.error("Invalid bot token in config.json")
            return
        
        await self.start(token)

    async def on_error(self, event, *args, **kwargs):
        from core.error_handler import handle_global_error
        await handle_global_error(self, event, *args, **kwargs)
