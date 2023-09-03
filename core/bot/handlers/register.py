from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, filters, MessageHandler, CallbackQueryHandler

from bot.handlers.start import start_keyboard
from bot.keyboards import cancel_keyboard, confirm_keyboard, status_check_keyboard
from erp.models import User

FIRST_NAME, LAST_NAME, RESULT = range(3)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.callback_query.message
    try:
        await sync_to_async(User.objects.get)(chat_id=message.chat.id)
        await message.edit_text(text='Вы уже зарегистрированы')
        return ConversationHandler.END
    except User.DoesNotExist:
        await message.edit_text(
            text='Введите фамилию:', reply_markup=cancel_keyboard
        )
        context.chat_data.update({'message': message})
        return FIRST_NAME


async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data.update({'last_name': update.message.text})
    await context.chat_data['message'].edit_text(text='Введите имя:', reply_markup=cancel_keyboard)
    return LAST_NAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data.update({'first_name': update.message.text})
    full_name = f"{context.chat_data['last_name']} {context.chat_data['first_name']}"
    await context.chat_data['message'].edit_text(
        text=f'{full_name}\n\nВерно?',
        reply_markup=confirm_keyboard,
    )
    return RESULT


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sync_to_async(User.objects.create)(
        first_name=context.chat_data['first_name'],
        last_name=context.chat_data['last_name'],
        username=context.chat_data['message'].chat.id,
        chat_id=context.chat_data['message'].chat.id,
        telegram_username=context.chat_data['message'].chat.username,
    )
    await context.chat_data['message'].edit_text(
        text='Готово! Ждите подтверждения.', reply_markup=status_check_keyboard
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.chat_data['message'].edit_text(
        text="Добрый день, сотрудник!\n\n"
             "Чтобы пройти регистрацию, нажми на кнопку ниже!",
        reply_markup=start_keyboard,
    )
    return ConversationHandler.END


register_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(register, 'register')],
    states={
        FIRST_NAME: [MessageHandler(filters.Regex(r'^\w*$'), first_name)],
        LAST_NAME: [MessageHandler(filters.Regex(r'^\w*$'), last_name)],
        RESULT: [CallbackQueryHandler(result, 'confirm')],
    },
    fallbacks=[CallbackQueryHandler(cancel, 'cancel')],
)
