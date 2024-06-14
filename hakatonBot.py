from aiogram.utils import executor
from createBot import dp
from dops.middleware import ThrottlingMiddleware


async def on_sturtup(_):
    print("Бот вышел в онлайн!")


from handlers import regHandlers

regHandlers.register_handlers_client(dp)
dp.middleware.setup(ThrottlingMiddleware())
executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup)
