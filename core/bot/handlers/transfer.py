from telegram import Update
from telegram.ext import ContextTypes

from bot.utils import validate_user


@validate_user
async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Answer')
