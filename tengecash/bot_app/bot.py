import asyncio
import os
import django
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tengecash.settings')
django.setup()

from loader import dp, bot
from handlers.common import router as common_router
from handlers.categories import router as cat_router
from states import router as states_router


async def main():
    dp.include_router(common_router)
    dp.include_router(cat_router)
    dp.include_router(states_router)

    print('Бот запущен...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())