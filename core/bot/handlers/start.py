from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.keyboards import start_keyboard, start_work_keyboard
from erp.models import User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    try:
        user = await sync_to_async(User.objects.get)(chat_id=update.message.chat.id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Здравствуйте, {user.first_name}!\n\n"
                 f"Какую информацию нужно внести?\n",
            reply_markup=start_work_keyboard,
        )

    except User.DoesNotExist:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добрый день, сотрудник!\n\n"
                 "Чтобы пройти регистрацию, нажмите на кнопку ниже!",
            reply_markup=start_keyboard,
        )
