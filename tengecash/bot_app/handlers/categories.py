from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tengecash.bot_app.database import (
    get_user_by_tg_id,
    get_categories_db,
    category_delete,
    get_categories_db,
    get_favorite_categories_db
)
from tengecash.bot_app.states import CategoryEditStates


router = Router()

@router.message(Command("catlist"))
async def handle_catlist(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    categories = await get_categories_db(user)
    if not categories:
        await message.answer(
            "В базе пока нет категорий."
            "Добавь их в браузерной версии /site или при помощи команды /catadd."
        )
        return

    response_text = '<b>📁 Твои категории расходов:</b>\n\n'
    for index, cat in enumerate(categories, start=1):
        # section_name = cat.section.name if cat.section else "Без раздела"
        response_text += f"{index}. {cat.name}\n"
    await message.answer(response_text, parse_mode="HTML")


@router.message(Command("catedit"))
async def handle_catedit(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    categories = await get_categories_db(user)
    if not categories:
        await message.answer(
            "В базе пока нет категорий."
            "Добавь их в браузерной версии /site или при помощи команды /catadd."
        )
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✏️ {cat.name}", callback_data=f"edit_{cat.id}")]
        for cat in categories
    ])
    await message.answer("Выбери категорию для редактирования:", reply_markup=keyboard)



@router.message(Command("catadd"))
async def handle_category_create(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    await message.answer("Введи название новой категории:")
    await state.set_state(CategoryEditStates.waiting_for_new_cat_name)


@router.message(Command("catdelete"))
async def handle_category_delete(message: Message, state: FSMContext):
    await state.clear()

    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    categories = await get_categories_db(user)
    if not categories:
        await message.answer(
            "В базе пока нет категорий."
            "Добавь их в браузерной версии /site или при помощи команды /catadd."
        )
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"❌ {cat.name}", callback_data=f"delete_{cat.id}")]
        for cat in categories
    ])
    await message.answer("Выбери категорию для удаления:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete(callback: CallbackQuery):
    cat_id = callback.data.split("_")[2]
    tg_id = callback.from_user.id
    user = await get_user_by_tg_id(tg_id)

    await category_delete(user, cat_id)

    await callback.message.edit_text("✅ Категория и все её расходы успешно удалены.")
    await callback.answer()

@router.callback_query(F.data == "cancel_delete")
async def cancel_delete(callback: CallbackQuery):
    await callback.message.edit_text("Действие отменено. Данные в сохранности! 😌")
    await callback.answer()


@router.callback_query(F.data == "show_all_categories")
async def show_all_categories_handler(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await callback.answer("Ошибка авторизации", show_alert=True)
        return

    all_categories = await get_categories_db(user)

    if not all_categories:
        await callback.answer("Категорий пока нет", show_alert=True)
        return

    buttons = [
        InlineKeyboardButton(text=cat.name, callback_data=f"saveexp_{cat.id}")
        for cat in all_categories
    ]

    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    rows.append([
        InlineKeyboardButton(text="⭐ Назад к избранным", callback_data="show_favorite_categories")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

    await callback.message.edit_text(
        "<b>Выбери категорию (полный список):</b>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "show_favorite_categories")
async def show_favorite_categories_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user_by_tg_id(callback.from_user.id)

    categories = await get_favorite_categories_db(user)

    if not categories:
        await callback.answer("У тебя пока нет избранных категорий", show_alert=True)
        return

    buttons = [
        [InlineKeyboardButton(text=f"{cat.name} ⭐", callback_data=f"saveexp_{cat.id}")]
        for cat in categories
    ]

    buttons.append([
        InlineKeyboardButton(text="🔍 Показать все категории", callback_data="show_all_categories")
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.edit_text(
        "Выбери категорию (только избранные):",
        reply_markup=keyboard
    )
    await callback.answer()