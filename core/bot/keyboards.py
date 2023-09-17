from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from erp.enums import WorkArea

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

start_work_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('ПЕРЕМЕСТИЛ', callback_data='start_transfer')],
    [InlineKeyboardButton('ИЗГОТОВИЛ', callback_data='start_production')],
])

continue_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Далее', callback_data='continue')],
    [InlineKeyboardButton('Сбросить', callback_data='cancel')],
])


def get_areas_keyboard(prefix: str, exclude_area: str = None) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(label.upper(), callback_data=f'{prefix}_{area}')]
        for area, label
        in WorkArea.choices
        if area != exclude_area
    ]
    keyboard.append([InlineKeyboardButton('Сбросить', callback_data='cancel')])
    return InlineKeyboardMarkup(keyboard)
