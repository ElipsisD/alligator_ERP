import hashlib

from asgiref.sync import sync_to_async
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes

from erp.models import ItemNumber


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    if not query:
        return

    results = [
        InlineQueryResultArticle(
            id=hashlib.md5(f'{item.pk}'.encode()).hexdigest(),
            title=item.name,
            input_message_content=InputTextMessageContent(item.number[3:]),
            # thumb_url='http://82.148.19.72/static/autos/images/exist.ico',
            # thumb_width=100,
            # thumb_height=100,
        )
        async for item in await sync_to_async(ItemNumber.objects.filter)(name__icontains=query)
    ]

    await update.inline_query.answer(results[:50])
