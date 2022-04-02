from aiogram.utils import executor
from bot_config import bot, dp
from handlers import admin, client
from database.users import safe_shutdown_users, users_start
from database.message_samples import safe_shutdown_message_samples, message_samples_start
from database.admin import safe_shutdown_admin, admin_start


async def on_startup(dp):
    message_samples_start()
    users_start()
    admin_start()

    print("-------------------------------BOT IS ONLINE-------------------------------\n")


async def on_shutdown(dp):
    await safe_shutdown_message_samples()
    await safe_shutdown_users()
    await safe_shutdown_admin()
    print("-------------------------------BOT IS OFFLINE-------------------------------")


admin.register_handlers_admin(dp)
client.register_handlers_client(dp)


executor.start_polling(dp,
                      skip_updates=True,
                      on_startup=on_startup,
                      on_shutdown=on_shutdown)
