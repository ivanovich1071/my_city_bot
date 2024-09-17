from aiogram import Router, types
from aiogram.types import CallbackQuery
from services.db_service import get_user

router = Router()


@router.callback_query(lambda c: c.data == 'exit')
async def exit_button_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = get_user(user_id)

    if user:
        await callback_query.message.answer(f"До свидания, {user[1]}!")
    else:
        await callback_query.message.answer("До свидания!")

    await callback_query.answer()  # Закрывает окно уведомления о нажатии кнопки
