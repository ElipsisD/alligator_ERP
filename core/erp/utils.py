from asgiref.sync import sync_to_async
from telegram import Update

from erp.models import User


async def get_user_by_update(update: Update) -> User:
    try:
        return await sync_to_async(User.objects.get)(chat_id=update.callback_query.message.chat.id)
    except AttributeError:
        return await sync_to_async(User.objects.get)(chat_id=update.message.chat.id)
