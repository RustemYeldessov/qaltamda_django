from decimal import Decimal
from pyexpat.errors import messages

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tengecash.bot_app.database import get_user_by_tg_id, create_expense, get_first_section
from tengecash.bot_app.states import ExpenseStates


router = Router()

@router.message(Command("addexp"))
async def handle_expense_create(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    await message.answer('Введи описание траты:')
    await state.set_state(ExpenseStates.waiting_for_description)

@router.callback_query(F.data.startswith("saveexp_"))
async def confirm_expense(callback: CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]
    data = await state.get_data()

    user = await get_user_by_tg_id(callback.from_user.id)
    section = await get_first_section(user)

    if not section:
        await callback.message.answer(
            "В базе пока нет разделов."
            "Добавь их в браузерной версии /site"
        )
        await callback.answer()
        return

    await create_expense(
        user=user,
        category_id=category_id,
        amount=Decimal(data['amount']),
        description=data['description'],
        section=section
    )

    await callback.message.edit_text(
        f"✅ Сохранено!\n"
        f"Трата: {data['description']}\n"
        f"Сумма: {data['amount']} тг."
    )
    await state.clear()
    await callback.answer()