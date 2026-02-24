from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tengecash.bot_app.database import get_user_by_tg_id, logout_user_db


router = Router()

HELP_COMMAND = """
/info - инструкция по внесению трат
/start - начать работу с ботом
/login - регистрация в Tenge Cash
/register - регистрация пользователя
/logout - выход из бота

/expadd - добавить трату

/catlist - список категорий
/catadd - создать новую категорию
/catedit - редактировать список категорий
/catdelete - удалить категорию и ее содержимое

/list - список последних 10-ти расходов
/total - сумма расходов за текущий месяц

/site - перейти на веб-сайт Tenge Cash
"""

@router.message(Command("help"))
async def handle_help(message: Message):
    await message.answer(text=HELP_COMMAND)


@router.message(Command("info"))
async def handle_info(message: Message):
    await message.answer('Введи по очереди трату, сумму, затем выбери категорию')

class LoginStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

@router.message(Command("start"))
async def handle_start(message: Message):
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)
    if user:
        await message.answer(f'С возвращением, {user.username}!')
    else:
        await message.answer(
            "Упс... Ты не авторизован.\n"
            "Пожалуйста, введи команду для привязки: /login"
        )


@router.message(Command("login"))
async def handle_login(message: Message, state: FSMContext):
    await message.answer("Введи логин:")
    await state.set_state(LoginStates.waiting_for_username)



@router.message(Command("logout"))
async def handle_logout(message: Message):
    success = await logout_user_db(message.from_user.id)
    if success:
        await message.answer('Выход выполнен успешно. Для повторного входа выполни команду /login')
    else:
        await message.answer('Ты не был авторизован')