from telegram import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Зарегистрироваться', callback_data='register')],
])

cancel_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Сбросить', callback_data='cancel')],
])

confirm_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Подтвердить', callback_data='confirm')],
    [InlineKeyboardButton('Сбросить', callback_data='cancel')],
])

status_check_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Проверить статус', callback_data='check')],
])

start_transfer_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Создать перемещение', callback_data='start_transfer')],
])
