from decimal import Decimal

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from tengecash.bot_app.database import (
    bind_user_with_password,
    get_user_by_tg_id,
    category_exists,
    update_category_name,
    create_category,
    get_categoies_db,
    expense_exists,
    delete_expense_by_id
)

router = Router()

class LoginStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()

class ExpenseStates(StatesGroup):
    waiting_for_description = State()
    waiting_for_amount = State()
    waiting_for_category = State()
    waiting_fot_date = State()

    waiting_for_expense_id = State()


@router.message(LoginStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    await state.update_data(chosen_username=message.text)
    await message.answer("Введи пароль:")
    await state.set_state(LoginStates.waiting_for_password)

@router.message(LoginStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data['chosen_username']
    password = message.text

    await message.delete()
    result = await bind_user_with_password(message.from_user.id, username, password)
    await message.answer(result)
    await state.clear()

class CategoryEditStates(StatesGroup):
    selecting_category = State()
    remaining_category = State()
    waiting_for_new_cat_name = State()

@router.callback_query(F.data.startswith("edit_"))
async def process_edit_category(callback: CallbackQuery, state: FSMContext):
    cat_id = callback.data.split("_")[1]

    from tengecash.bot_app.database import Category
    category = await sync_to_async(Category.objects.filter(id=cat_id).first)()

    await state.update_data(editing_cat_id=cat_id)

    await callback.message.edit_text(
        f"Введи новое название для этой категории <b>{category.name}</b>:",
        parse_mode="HTML"
    )
    await state.set_state(CategoryEditStates.remaining_category)
    await callback.answer()

@router.message(CategoryEditStates.remaining_category)
async def process_new_name(message: Message, state: FSMContext):
    data = await state.get_data()
    cat_id = data.get("editing_cat_id")
    new_name = message.text.strip()

    user = await get_user_by_tg_id(message.from_user.id)

    if await category_exists(user, new_name):
        await message.answer(
            f"❌ Категория с именем <b>{new_name}</b> уже существует!\n"
            "Введи другое название:",
            parse_mode="HTML"
        )
        return

    await update_category_name(cat_id, new_name)

    await message.answer(
        f"✅ Категория успешно переименована в: <b>{new_name}</b>",
            parse_mode="HTML"
    )
    await state.clear()

@router.message(CategoryEditStates.waiting_for_new_cat_name)
async def process_add_category(message: Message, state: FSMContext):
    new_cat_name = message.text.strip()
    user = await get_user_by_tg_id(message.from_user.id)

    if await category_exists(user, new_cat_name):
        await message.answer(
            f"❌ Категория с именем <b>{new_cat_name}</b> уже существует!\n"
            "Введи другое название:",
            parse_mode="HTML"
        )
        return

    await create_category(user, new_cat_name)
    await message.answer(
        f"✅ Категория <b>{new_cat_name}</b> успешно создана!",
            parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data.startswith("delete_"))
async def process_delete_category(callback: CallbackQuery):
    cat_id = callback.data.split("_")[1]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, удалить ✅", callback_data=f"confirm_delete_{cat_id}"),
            InlineKeyboardButton(text="Отмена ❌", callback_data=f"cancel_delete")
        ]
    ])

    await callback.message.edit_text(
        "⚠️ <b>Внимание!</b>\n"
        "При удалении категории удалятся и все расходы, связанные с ней.\n"
        "Данные при необходимости можно восстановить.\n"
        "Удалить?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(ExpenseStates.waiting_for_description)
async def process_expense_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text.strip())
    await message.answer("Введи сумму:")
    await state.set_state(ExpenseStates.waiting_for_amount)

@router.message(ExpenseStates.waiting_for_amount)
async def process_expense_amount(message: Message, state: FSMContext):
    amount_text = message.text.strip().replace(',', '').replace(' ', '')

    try:
        amount = Decimal(amount_text)
    except:
        await message.answer("Ошибка! Введи сумму числом, например 1000")
        return

    await state.update_data(amount=str(amount))

    user = await get_user_by_tg_id(message.from_user.id)
    categories = await get_categoies_db(user)

    if not categories:
        await message.answer(
            "В базе пока нет категорий."
            "Добавь их в браузерной версии /site или при помощи команды /catadd."
        )
        await state.clear()
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cat.name, callback_data=f"saveexp_{cat.id}")]
        for cat in categories
    ])

    data = await state.get_data()
    await message.answer(
        f"Записываю: <b>{data['description']}</b> на сумму <b>{amount} тг.</b>\n"
        f"Выбери категорию:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await state.set_state(ExpenseStates.waiting_for_category)

@router.message(ExpenseStates.waiting_for_expense_id)
async def process_expense_id(message: Message, state: FSMContext):
    expense_id = message.text

    if not expense_id.isdigit():
        await message.answer("ID траты должно быть числом")
        return

    user = await get_user_by_tg_id(message.from_user.id)
    delete_count, _ = await delete_expense_by_id(user, int(expense_id))

    if delete_count > 0:
        await message.answer(f"✅ Трата №<b>{expense_id}</b> успешно удалена", parse_mode="HTML")
    else:
        await message.answer("Трата с таким ID не найдена")

    await state.clear()
