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
from handlers.expenses import router as exp_router
from states import router as states_router
from handlers.register import router as register_router


async def main():
    dp.include_router(common_router)
    dp.include_router(cat_router)
    dp.include_router(states_router)
    dp.include_router(exp_router)
    dp.include_router(register_router)

    print('Бот запущен...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())