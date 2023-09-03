from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import start_keyboard
from erp.models import User


def validate_user(handler):
    """Декоратор для проверки пользователей на прохождение регистрации"""
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await sync_to_async(User.objects.get)(chat_id=update.callback_query.message.chat.id)
            await handler(update, context)
        except User.DoesNotExist:
            await update.message.edit_text(
                text="Добрый день, сотрудник!\n\n"
                     "Чтобы пройти регистрацию, нажми на кнопку ниже!",
                reply_markup=start_keyboard,
            )
    return wrapped
