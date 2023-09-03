import logging

from django.core.management import BaseCommand
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.config import COMMAND_HANDLERS
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

        application.run_polling()
