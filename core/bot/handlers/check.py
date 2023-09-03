from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import status_check_keyboard, start_transfer_keyboard
from erp.models import User


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.callback_query.message
    try:
        user = await sync_to_async(User.objects.get)(chat_id=message.chat_id)
        if user.area:
            await message.edit_text('Давай работать :)', reply_markup=start_transfer_keyboard)
        else:
            await message.edit_text(
                'Подтверждение еще не получено!', reply_markup=status_check_keyboard
            )
    except User.DoesNotExist:
        return
