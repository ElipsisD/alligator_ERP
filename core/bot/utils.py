from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import start_keyboard, status_check_keyboard
from erp.models import User
from erp.utils import get_user_by_update


def validate_user(handler):
    """Декоратор для проверки пользователей на прохождение регистрации"""
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.callback_query:
            message = update.callback_query.message
        else:
            message = update.message
        try:
            user = await get_user_by_update(update)

            if not user.area:
                await message.edit_text(
                    'Подтверждение еще не получено!', reply_markup=status_check_keyboard
                )
            else:
                return await handler(update, context)
        except User.DoesNotExist:
            await message.edit_text(
                text="Добрый день, сотрудник!\n\n"
                     "Чтобы пройти регистрацию, нажми на кнопку ниже!",
                reply_markup=start_keyboard,
            )
    return wrapped
