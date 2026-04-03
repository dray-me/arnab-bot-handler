import asyncio
import os
import importlib
import sys
from functions.retry_manager import with_retry

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.functions = []

    async def load_functions(self):
        func_dir = "functions"
        for filename in os.listdir(func_dir):
            if filename.endswith(".py") and filename not in ["scheduler.py", "retry_manager.py"]:
                module_path = f"functions.{filename[:-3]}"
                await self.register_function(module_path)

    async def register_function(self, module_path):
        try:
            if module_path in sys.modules:
                importlib.reload(sys.modules[module_path])
            module = importlib.import_module(module_path)
            
            interval = getattr(module, "interval", None)
            execute = getattr(module, "execute", None)
            once = getattr(module, "once", False)
            retry_attempts = getattr(module, "retryAttempts", 3)
            
            if execute:
                if once:
                    asyncio.create_task(self.run_once(execute, retry_attempts))
                elif interval:
                    asyncio.create_task(self.run_loop(execute, interval, retry_attempts))
                
                self.bot.logger.info(f"Registered function: {module_path}")
        except Exception as e:
            self.bot.logger.error(f"Failed to register function {module_path}: {e}")

    async def run_once(self, func, retries):
        await with_retry(func, self.bot, retries=retries)

    async def run_loop(self, func, interval_ms, retries):
        while not self.bot.is_closed():
            await with_retry(func, self.bot, retries=retries)
            await asyncio.sleep(interval_ms / 1000)
