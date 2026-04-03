import asyncio

async def with_retry(func, bot, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            await func(bot)
            return
        except Exception as e:
            attempt += 1
            bot.logger.error(f"Function execution failed (Attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    bot.logger.error(f"Function failed after {retries} attempts.")
