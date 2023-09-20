from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, ConversationHandler

from bot.keyboards import start_keyboard, start_work_keyboard
from erp.models import User
from erp.utils import get_user_by_update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    try:
        await context.chat_data["message"].delete()
    except (KeyError, BadRequest):
        pass
    context.chat_data.clear()
    try:
        user = await get_user_by_update(update)
        mess = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Здравствуйте, {user.first_name}!\n\n"
                 f"Какую информацию нужно внести?\n",
            reply_markup=start_work_keyboard,
        )

    except User.DoesNotExist:
        mess = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добрый день, сотрудник!\n\n"
                 "Чтобы пройти регистрацию, нажмите на кнопку ниже!",
            reply_markup=start_keyboard,
        )

    context.chat_data['message'] = mess
    return ConversationHandler.END
