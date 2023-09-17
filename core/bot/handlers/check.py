from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes


from bot.keyboards import status_check_keyboard, start_work_keyboard
from erp.models import User
from erp.utils import get_user_by_update


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.callback_query.message
    try:
        user = await get_user_by_update(update)
        if user.area:
            await message.edit_text(
                text=f"Здравствуйте, {user.first_name}!\n\n"
                     f"Какую информацию нужно внести?\n",
                reply_markup=start_work_keyboard
            )

        else:
            await message.edit_text(
                'Подтверждение еще не получено!', reply_markup=status_check_keyboard
            )
    except User.DoesNotExist:
        return
