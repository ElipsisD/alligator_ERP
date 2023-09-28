from asgiref.sync import sync_to_async
from telegram import Update, constants
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime
from bot.keyboards import get_areas_keyboard, cancel_keyboard, continue_keyboard, start_work_keyboard, confirm_keyboard, \
    cancel_with_find_keyboard
from bot.utils import validate_user
from core.settings import ITEM_NUMBER_DIGIT_COUNT
from erp.enums import WorkArea
from erp.models import Transfer, ItemNumber
from erp.utils import get_user_by_update

AREA, ITEM_NUMBER, AMOUNT, COMMENT, RESULT = range(10, 15)

PATTERN = 'transfer'


@validate_user
async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data['message'] = update.callback_query.message
    user = await get_user_by_update(update)
    await update.callback_query.message.edit_text(
        text='На какой участок?', reply_markup=get_areas_keyboard(PATTERN, user.area)
    )
    return AREA


async def area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data['area'] = update.callback_query.data.split('_')[-1]
    await update.callback_query.message.edit_text(
        text=f'Введите {ITEM_NUMBER_DIGIT_COUNT} цифр номенклатурного номера:\n\n'
             f'Для включения поиска нажмите на кнопку "ПОИСК"\n',
        reply_markup=cancel_with_find_keyboard
    )
    return ITEM_NUMBER


async def item_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

    if len(update.message.text) != ITEM_NUMBER_DIGIT_COUNT:
        await context.chat_data["message"].edit_text(
            text=f'Нужно ввести {ITEM_NUMBER_DIGIT_COUNT} цифр!', reply_markup=cancel_with_find_keyboard
        )
        return ITEM_NUMBER

    context.chat_data['item_number'] = update.message.text
    await context.chat_data["message"].edit_text(
        text='Введите количество материала/заготовок:', reply_markup=cancel_keyboard
    )
    return AMOUNT


async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    context.chat_data['amount'] = int(update.message.text)
    await context.chat_data["message"].edit_text(
        text='Введите комментарий или нажмите кнопку "ДАЛЕЕ":', reply_markup=continue_keyboard
    )
    return COMMENT


async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
        context.chat_data['comment'] = update.message.text
    except AttributeError:
        context.chat_data['comment'] = ''
    item_number_object = await sync_to_async(ItemNumber.objects.get)(
        number=f'НФ-{context.chat_data["item_number"]}',
    )
    context.chat_data['item_name'] = item_number_object.name
    await context.chat_data["message"].edit_text(
        text='Все указано верно?\n\n'
             f'<b>Куда:</b> {WorkArea.get_label_by_name(context.chat_data["area"])}\n'
             f'<b>Наименование:</b> {context.chat_data["item_name"]}\n'
             f'<b>Количество:</b> {context.chat_data["amount"]}\n'
             f'<b>Комментарий:</b> {context.chat_data.get("comment", "")}\n',
        parse_mode=constants.ParseMode.HTML,
        reply_markup=confirm_keyboard
    )
    return RESULT


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user_by_update(update)
    await sync_to_async(Transfer.objects.create)(
        author=user,
        item_number_id=f'НФ-{context.chat_data["item_number"]}',
        amount=int(context.chat_data['amount']),
        comment=context.chat_data['comment'],
        sender=user.area,
        receiver=context.chat_data['area'],
    )
    await context.chat_data["message"].edit_text(
        text=f'📦<b>ПЕРЕМЕСТИЛ</b>\n'
             f'📅<b>{datetime.now().strftime("%d.%m.%Y %H:%M")}</b>\n\n'
             f'<b>Куда:</b> {WorkArea.get_label_by_name(context.chat_data["area"])}\n'
             f'<b>Наименование:</b> {context.chat_data["item_name"]}\n'
             f'<b>Количество:</b> {context.chat_data["amount"]}\n'
             + (f'<b>Комментарий:</b> {context.chat_data["comment"]}\n' if context.chat_data["comment"] != '' else ''),
        parse_mode=constants.ParseMode.HTML,
    )
    mess = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Здравствуйте, {user.first_name}!\n\n"
             f"Какую информацию нужно внести?\n",
        reply_markup=start_work_keyboard,
    )
    context.chat_data.clear()
    context.chat_data['message'] = mess
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user_by_update(update)
    await context.chat_data['message'].edit_text(
        text=f"Здравствуйте, {user.first_name}!\n\n"
             f"Какую информацию нужно внести?\n",
        reply_markup=start_work_keyboard,
    )
    context.chat_data.clear()
    return ConversationHandler.END


transfer_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(transfer, 'start_transfer')],
    states={
        AREA: [CallbackQueryHandler(area, r'^\w*_\w*$')],
        ITEM_NUMBER: [MessageHandler(filters.Regex(r'^\d*$'), item_number)],
        AMOUNT: [MessageHandler(filters.Regex(r'^0*[1-9]\d*$'), amount)],
        COMMENT: [MessageHandler(filters.Regex(r'[\d\w]*'), comment), CallbackQueryHandler(comment, 'continue')],
        RESULT: [CallbackQueryHandler(result, 'confirm')],
    },
    fallbacks=[CallbackQueryHandler(cancel, 'cancel')],
)
