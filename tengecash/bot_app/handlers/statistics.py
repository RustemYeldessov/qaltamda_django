from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold, hitalic
from django.utils import timezone

from tengecash.bot_app.database import get_monthly_stats, get_user_by_tg_id

router = Router()

@router.message(Command("stats"))
async def handle_stats(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    user = await get_user_by_tg_id(tg_id)

    if not user:
        await message.answer("Сначала нужно авторизоваться, используй /login")
        return

    stats, total_period = await get_monthly_stats(user)

    today = timezone.now().date()
    response_text = [
        f"📊 {hbold('Статистика за месяц')}",
        f"{hitalic(f'с 01.{today.month:02d}.{today.year} по {today.strftime('%d.%m.%Y')}')}\n"
    ]

    for item in stats:
        category = item['category__name'] or "Без категории"
        amount = f"{item['sum']:,.0f}".replace(",", " ")
        response_text.append(f"{category}: {hbold(amount)} ₸")

    response_text.append(f"\n💰 {hbold('Итого:')} {hbold(f'{total_period:,.0f}'.replace(',', ' '))} ₸")

    await message.answer("\n".join(response_text), parse_mode="HTML")
