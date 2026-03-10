from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tengecash.bot_app.database import get_user_by_tg_id, get_categories_db, category_delete, get_categories_db
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
