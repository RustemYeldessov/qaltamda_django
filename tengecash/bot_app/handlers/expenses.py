# @dp.message(Command("addexp"))
# async def handle_expense_create(message: Message, state: FSMContext):
#     tg_id = message.from_user.id
#     user = await get_user_by_tg_id(tg_id)
#
#     if not user:
#         await message.answer("Сначала нужно авторизоваться, используй /login")
#         return
#
#     await message.answer('Введи описание траты:')
#     await state.set_state(ExpenseEditStates.waiting_for_new_expense_description)