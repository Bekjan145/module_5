import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


async def main() -> None:
    from inline_bot_with_api.handlers import start_router, wiki_router

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router, wiki_router)

    # Pollingni boshlashdan oldin botni sinab ko'rish
    try:
        await bot.get_me()
        logging.info("Bot successfully connected to Telegram API")
    except Exception as e:
        logging.error(f"Failed to connect to Telegram API: {e}")
        return

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    asyncio.run(main())