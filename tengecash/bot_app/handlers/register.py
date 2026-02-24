from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tengecash.bot_app.database import registration_user_db

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_password_confirm = State()


@router.message(Command("register"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Начнем регистрацию!\nВведи свое имя:")
    await state.set_state(RegistrationStates.waiting_for_first_name)

@router.message(RegistrationStates.waiting_for_first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.strip())
    await message.answer("Введи свою фамилию:")
    await state.set_state(RegistrationStates.waiting_for_last_name)

@router.message(RegistrationStates.waiting_for_last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text.strip())
    await message.answer("Придумай логин для входа:")
    await state.set_state(RegistrationStates.waiting_for_username)

@router.message(RegistrationStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text.strip().lower())
    await message.answer("Придумай пароль:")
    await state.set_state(RegistrationStates.waiting_for_password)

@router.message(RegistrationStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
    await message.answer("Повтори пароль:")
    await state.set_state(RegistrationStates.waiting_for_password_confirm)

@router.message(RegistrationStates.waiting_for_password_confirm)
async def process_password_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    password_confirm = message.text
    await message.delete()

    if password_confirm != data['password']:
        await message.answer("❌ Пароли не совпадают! Начни ввод пароля заново.\nВведи пароль:")
        await state.set_state(RegistrationStates.waiting_for_password)
        return
    success, result_message = await registration_user_db(
        tg_id=message.from_user.id,
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password']
    )
    await message.answer(result_message)
    await state.clear()