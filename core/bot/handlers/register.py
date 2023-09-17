from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, filters, MessageHandler, CallbackQueryHandler

from bot.handlers.start import start_keyboard
from bot.keyboards import cancel_keyboard, confirm_keyboard, status_check_keyboard, start_work_keyboard
from erp.models import User
from erp.utils import get_user_by_update

FIRST_NAME, LAST_NAME, PATRONYMIC, RESULT = range(4)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                text='Ждите подтверждения.', reply_markup=status_check_keyboard
            )
        return ConversationHandler.END
    except User.DoesNotExist:
        await message.edit_text(
            text='Введите фамилию:', reply_markup=cancel_keyboard
        )
        context.chat_data.update({'message': message})
        return LAST_NAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data.update({'last_name': update.message.text.strip().capitalize()})
    await context.chat_data['message'].edit_text(text='Введите имя:', reply_markup=cancel_keyboard)
    return FIRST_NAME


async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data.update({'first_name': update.message.text.strip().capitalize()})
    await context.chat_data['message'].edit_text(text='Введите отчество:', reply_markup=cancel_keyboard)
    return PATRONYMIC


async def patronymic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data.update({'patronymic': update.message.text.strip().capitalize()})
    full_name = f"{context.chat_data['last_name']} {context.chat_data['first_name']} {context.chat_data['patronymic']}"
    await context.chat_data['message'].edit_text(
        text=f'{full_name}\n\nВерно?',
        reply_markup=confirm_keyboard,
    )
    return RESULT


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sync_to_async(User.objects.create)(
        first_name=context.chat_data['first_name'],
        last_name=context.chat_data['last_name'],
        patronymic=context.chat_data['patronymic'],
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
        LAST_NAME: [MessageHandler(filters.Regex(r'^\w*$'), last_name)],
        FIRST_NAME: [MessageHandler(filters.Regex(r'^\w*$'), first_name)],
        PATRONYMIC: [MessageHandler(filters.Regex(r'^\w*$'), patronymic)],
        RESULT: [CallbackQueryHandler(result, 'confirm')],
    },
    fallbacks=[CallbackQueryHandler(cancel, 'cancel')],
)
