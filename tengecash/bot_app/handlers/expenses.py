from decimal import Decimal
from pyexpat.errors import messages

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tengecash.bot_app.database import (
    get_user_by_tg_id,
    create_expense,
    get_first_section,
    get_categories_db
)
from tengecash.bot_app.states import ExpenseStates


router = Router()

@router.message(Command("expadd"))
async def handle_expense_create(message: Message, state: FSMContext):
    await state.clear()

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

    new_expense = await create_expense(
        user=user,
        category_id=category_id,
        amount=Decimal(data['amount']),
        description=data['description'],
        section=section
    )

    formatted_date = new_expense.date.strftime("%d.%m.%Y")

    await callback.message.edit_text(
        f"✅ Сохранено! <b>ID траты: {new_expense.id}</b>\n\n"
        f"Трата: {data['description']}\n"
        f"Сумма: {data['amount']} тг.\n"
        f"Дата: {formatted_date}",
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()

@router.message(Command("expdelete"))
async def handle_expense_delete(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    await message.answer("Введи ID траты, которую нужно удалить:")
    await state.set_state(ExpenseStates.waiting_for_expense_id)

@router.callback_query(F.data == "show_all_categories")
async def show_all_categories_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user_by_tg_id(callback.from_user.id)
    all_categories = await get_categories_db()

    if not all_categories:
        await callback.answer("Категорий пока нет", show_alert=True)
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cat.name, callback_data=f"saveexp_{cat.id}")]
        for cat in all_categories
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="Назад к избранным", callback_data="show_favorite_categories")
    ])

    await callback.message.edit_text(
        "Выбери категорию:",
        reply_markup=keyboard
    )

    await callback.answer()
