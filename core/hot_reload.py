from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import asyncio

class HotReloader(FileSystemEventHandler):
    def __init__(self, bot):
        self.bot = bot
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self, "commands", recursive=True)
        self.observer.schedule(self, "events", recursive=True)
        self.observer.schedule(self, "functions", recursive=True)
        self.observer.start()

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            self.bot.logger.info(f"Detected change in {event.src_path}, reloading...")
            # Trigger reload logic
            asyncio.run_coroutine_threadsafe(self.bot.loader.load_all(), self.bot.loop)
