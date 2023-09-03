import logging

from django.core.management import BaseCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler

from bot.config import COMMAND_HANDLERS, HANDLERS, CONVERSATION_HANDLERS, CALLBACK_QUERY_HANDLERS
from core.settings import TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Телеграм-Бот'

    def handle(self, *args, **kwargs):

        application = ApplicationBuilder().token(TOKEN).build()

        for command_name, command_handler in COMMAND_HANDLERS.items():
            application.add_handler(CommandHandler(command_name, command_handler))

        for handler in CONVERSATION_HANDLERS:
            application.add_handler(handler)

        for handler, handler_filter in HANDLERS.items():
            application.add_handler(MessageHandler(handler_filter, handler))

        for regex, handler in CALLBACK_QUERY_HANDLERS.items():
            application.add_handler(CallbackQueryHandler(handler, regex))

        application.run_polling()
