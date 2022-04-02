from aiogram import types
from bot_config import bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from database.admin import take_admin_list, add_new_admin, delete_from_admin
from keyboards.admin import admin_panel, kb_remove
from classes.admin import adding_sample
from handlers.client import send_user_sample
from aiogram.dispatcher import FSMContext
from database.message_samples import add_new_sample, take_all_samples, deleting_sample
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cancel_states(message: types.Message, state: FSMContext):
    admin_list = await take_admin_list()
    if message.from_user.id in admin_list:
        current_state = await state.get_state()
        if current_state is None:
            return
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "Sample adding has been canceled")
    else:
        await send_user_sample(message)


async def make_admin(message: types.Message):
    admin_list = await take_admin_list()
    if message.from_user.id not in admin_list:
        await add_new_admin(new_admin_id=message.from_user.id, username=message.from_user.username)
        await bot.send_message(message.from_user.id, "From now, you are admin", reply_markup=admin_panel())
    else:
        await bot.send_message(message.from_user.id,
                               "You are already admin. Stop trying to break bot", reply_markup=admin_panel())


async def new_sample_start(message: types.Message):
    admins = await take_admin_list()
    sample_list = await take_all_samples()
    if message.from_user.id in admins:
        if len(sample_list) <= 5:
            await adding_sample.sample_id.set()
            await bot.send_message(message.from_user.id, "Send me a number of new sample...")
        else:
            await bot.send_message(message.from_user.id, "Samples count is much than 5")
    else:
        await send_user_sample(message)


async def new_sample_id(message: types.Message, state: FSMContext):
    admins = await take_admin_list()
    if message.from_user.id in admins:
        try:
            sample_id = int(message.text)
            if sample_id in list(range(1, 6)):
                async with state.proxy() as data:
                    data["sample_id"] = sample_id
                await adding_sample.next()
                await bot.send_message(message.from_user.id, "Send me a sample message")
            else:
                await bot.send_message(message.from_user.id, "Sample id must be in range 1-5")
        except Exception:
            await bot.send_message(message.from_user.id, "it is not a number, try again")
    else:
        await send_user_sample(message)
        await state.finish()


async def new_sample_add(message: types.Message, state: FSMContext):
    admins = await take_admin_list()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            sample_id = data.get("sample_id")
        try:
            sample = message.text
            await add_new_sample(sample_id=sample_id, sample=sample)
            await bot.send_message(message.from_user.id, f"Sample with number {sample_id} has been added")
            await state.finish()
        except Exception:
            await bot.send_message(message.from_user.id, f"Sample id is already {sample_id} taken")
            await state.finish()
    else:
        await send_user_sample(message)
        await state.finish()


async def delete_admin(message: types.Message):
    admin_list = await take_admin_list()
    if message.from_user.id not in admin_list:
        await bot.send_message(message.from_user.id, "You are not an admin for this function", reply_markup=kb_remove())
    else:
        await delete_from_admin(admin_id=message.from_user.id)
        await bot.send_message(message.from_user.id, "You admin permission have been revoked", reply_markup=kb_remove())


async def get_sample_list(message: types.Message):
    sample_list = await take_all_samples()
    for sample_info in sample_list:
        sample_id = sample_info[0]
        sample = sample_info[1]
        await bot.send_message(message.from_user.id, f'sample id: {sample_id}\nsample: {sample}',
                               reply_markup=InlineKeyboardMarkup(row_width=1)
                               .add(InlineKeyboardButton('Delete sample', callback_data=f"DS {sample_id}")))


async def delete_sample(call: types.CallbackQuery):
    sample_id = call.data.replace("DS ", "")
    await deleting_sample(sample_id=sample_id)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.answer("Sample has been deleted")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_admin, commands=["ff7b9227-c365-4b09-9827-fadc1506b0cb"])
    dp.register_message_handler(make_admin, Text(equals="ff7b9227-c365-4b09-9827-fadc1506b0cb"))
    dp.register_message_handler(delete_admin, commands=["unff7b9227-c365-4b09-9827-fadc1506b0cb"])
    dp.register_message_handler(delete_admin, Text(equals="unff7b9227-c365-4b09-9827-fadc1506b0cb"))
    dp.register_message_handler(get_sample_list, commands=['sample_list'])
    dp.register_message_handler(get_sample_list, Text(equals="Sample list"))
    dp.register_message_handler(new_sample_start, Text(equals="New_sample"))
    dp.register_message_handler(cancel_states, commands=["Cancel"], state='*')
    dp.register_message_handler(cancel_states, Text(equals="Cancel"), state='*')
    dp.register_message_handler(new_sample_start, Text(equals="New sample"), state=None)
    dp.register_message_handler(new_sample_id, state=adding_sample.sample_id)
    dp.register_message_handler(new_sample_add, state=adding_sample.sample)
    dp.register_callback_query_handler(delete_sample, lambda x: x.data and x.data.startswith("DS "))
