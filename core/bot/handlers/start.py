from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.keyboards import start_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добрый день, сотрудник!\n\n"
             "Чтобы пройти регистрацию, нажми на кнопку ниже!",
        reply_markup=start_keyboard,
    )
