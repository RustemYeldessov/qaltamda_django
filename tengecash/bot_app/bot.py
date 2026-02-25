import asyncio
import sys
import os
import django
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tengecash.settings')
django.setup()

from loader import dp, bot
from tengecash.bot_app.handlers.common import router as common_router
from tengecash.bot_app.handlers.categories import router as cat_router
from tengecash.bot_app.handlers.expenses import router as exp_router
from tengecash.bot_app.states import router as states_router
from tengecash.bot_app.handlers.register import router as register_router


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