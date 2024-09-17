import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.start_handler import router as start_router
from handlers.weather_handler import router as weather_router
from handlers.guide_handler import router as guide_router
from handlers.exit_handler import router as exit_router
from services.db_service import create_db
# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрируем все роутеры
dp.include_router(start_router)
dp.include_router(weather_router)
dp.include_router(guide_router)
dp.include_router(exit_router)

async def main():
    create_db()  # Создаем БД при запуске бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
