from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, filters


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

echo_filter = filters.TEXT & (~filters.COMMAND)
