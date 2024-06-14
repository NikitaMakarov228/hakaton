from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
OURTOKEN = "6830380213:AAEYQbLKNxGa9mB5jD0nNAk_DhILRMbooIk"
bot = Bot(token=OURTOKEN)
dp = Dispatcher(bot, storage=storage)
