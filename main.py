import asyncio
import json
import os
from core.bot import ArnabBot
from core.logger import setup_logger

async def main():
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Arnab Bot Handler...")

    # Load config
    if not os.path.exists("config.json"):
        logger.error("config.json not found!")
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    # Initialize Bot
    bot = ArnabBot(config)

    try:
        await bot.start_bot()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
