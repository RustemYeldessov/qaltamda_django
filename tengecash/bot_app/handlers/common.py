from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton

from tengecash.bot_app.database import get_user_by_tg_id, logout_user_db


router = Router()

HELP_COMMAND = """
/info - Этот бот предназначен для помощи в ведении расходов. Для показа списка команд введи /help
/start - начать работу с ботом
/login - регистрация в Tenge Cash
/register - регистрация пользователя
/logout - выход из бота

/expadd - добавить трату

/catlist - список категорий
/catadd - создать новую категорию
/catedit - редактировать список категорий
/catdelete - удалить категорию и ее содержимое

/list - список последних 10-ти расходов (в разработке)
/stats - сумма расходов за текущий месяц

/site - перейти на веб-сайт Tenge Cash
"""

@router.message(Command("help"))
async def handle_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=HELP_COMMAND)


@router.message(Command("info"))
async def handle_info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Для внесения траты в базу данных используй команду /expadd')

class LoginStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)
    if user:
        await message.answer(f'С возвращением, {user.first_name}!')
    else:
        await message.answer(
            "Упс... Ты не авторизован.\n"
            "Пожалуйста, введи команду для привязки: /login"
        )


@router.message(Command("login"))
async def handle_login(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if user:
        await message.answer(f"Ты уже авторизован как пользователь {user.username}")
    else:
        await message.answer("Введи логин:")
        await state.set_state(LoginStates.waiting_for_username)



@router.message(Command("logout"))
async def handle_logout(message: Message, state: FSMContext):
    await state.clear()

    success = await logout_user_db(message.from_user.id)
    if success:
        await message.answer('Выход выполнен успешно. Для повторного входа выполни команду /login')
    else:
        await message.answer('Ты не был авторизован')


@router.message(Command("site"))
async def handle_site(message: Message, state: FSMContext):
    await state.clear()

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🌐 Перейти на сайт Tenge Cash",
        url="https://expenzo-94dq.onrender.com")
    )
    await message.answer(
        "Нажми на кнопку ниже для перехода в веб-версию приложения:",
        reply_markup=builder.as_markup()
    )