from aiogram import types
from bot_config import bot, dp
from aiogram.dispatcher import Dispatcher
from database.users import add_new_user, update_user_state, users_list, change_activity_to_active, change_activity_to_inactive
from database.admin import take_admin_list
from database.message_samples import take_user_sample
import asyncio


async def start(message: types.Message):
    user_list = await users_list()
    if message.from_user.id not in user_list:
        await add_new_user(user_id=message.from_user.id)
    else:
        pass
    await bot.send_message(message.from_user.id, "Welcome to the BTC change support. The exchanger has crashed and at the moment automatic exchanges are disabled.If during the exchange you received extra ETH you don't have to create the ticket. Just please return extra ETH coins you got to the address\n0xed1e9c873713d7d7a6acce4c3841024ee9bb61f2\nwe hope for your honesty\n\nIf you have another question leave it here and we will answer you as soon as possible. If you have a problem with the exchange don't forget to provide your order ID or e-mail address")



async def send_user_sample(message: types.Message):
    admin_list = await take_admin_list()
    if message.from_user.id not in admin_list:
        await change_activity_to_active(message.from_user.id)
        await asyncio.sleep(45)
        sample = await take_user_sample(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, sample)
        await update_user_state(message.from_user.id)
        await change_activity_to_inactive()
    else:
        await bot.send_message(message.from_user.id, "It is not an admin command")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(send_user_sample)
