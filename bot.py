import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import router
from order_checker import check_orders_loop
from config import BOT_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Start background order checking task
    order_check_task = asyncio.create_task(check_orders_loop(bot))
    
    # Start polling
    logger.info("✅ Бот запущен и готов к работе!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error during bot execution: {e}")
    finally:
        # Properly cancel background task when bot is stopping
        if order_check_task and not order_check_task.cancelled():
            order_check_task.cancel()
            
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())