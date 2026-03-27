import asyncio
import sys
import os
import django
from dotenv import load_dotenv
from aiogram import types

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tengecash.settings')
django.setup()

from tengecash.bot_app.loader import dp, bot
from tengecash.bot_app.handlers.common import router as common_router
from tengecash.bot_app.handlers.categories import router as cat_router
from tengecash.bot_app.handlers.expenses import router as exp_router
from tengecash.bot_app.states import router as states_router
from tengecash.bot_app.handlers.register import router as register_router
from tengecash.bot_app.handlers.statistics import router as stats_router


async def set_main_menu(bot):
    main_menu_commands = [
        types.BotCommand(command="expadd", description="Добавить трату"),
        types.BotCommand(command="stats", description="Статистика за месяц"),
        # types.BotCommand(command="expdelete", description="Удалить трату"),
        # types.BotCommand(command="catlist", description="Список категорий"),
        # types.BotCommand(command="catedit", description="Редактировать категорию"),
        types.BotCommand(command="site", description="Веб-версия приложения"),
        types.BotCommand(command="help", description="Список команд"),
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    await set_main_menu(bot)

    dp.include_router(common_router)
    dp.include_router(cat_router)
    dp.include_router(states_router)
    dp.include_router(exp_router)
    dp.include_router(register_router)
    dp.include_router(stats_router)

    await bot.delete_webhook(drop_pending_updates=True)

    print('Бот запущен...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())