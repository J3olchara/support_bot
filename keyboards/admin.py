from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def admin_panel():
    add_sample = KeyboardButton("New sample")
    sample_list = KeyboardButton("Sample list")
    cancel_state = KeyboardButton("Cancel")
    return ReplyKeyboardMarkup(resize_keyboard=True).row(add_sample, sample_list).add(cancel_state)

def kb_remove():
    return ReplyKeyboardRemove()










