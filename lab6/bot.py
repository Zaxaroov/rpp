import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

# Загрузка переменных окружения
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Временное хранилище валют
currency_rates = {}

# Состояния FSM для сохранения валюты
class CurrencyStates(StatesGroup):
    waiting_for_currency_name = State()
    waiting_for_currency_rate = State()

# Состояния FSM для конвертации
class ConvertStates(StatesGroup):
    waiting_for_currency_name = State()
    waiting_for_amount = State()

# Команда /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для конвертации валют.\nДоступные команды: /save_currency, /convert, /help")

# Команда /save_currency — начало процесса сохранения валюты
@dp.message_handler(commands=["save_currency"])
async def cmd_save_currency(message: types.Message):
    await message.answer("Введите название валюты (например: Доллар):")
    await CurrencyStates.waiting_for_currency_name.set()

# Обработка названия валюты
@dp.message_handler(state=CurrencyStates.waiting_for_currency_name)
async def process_currency_name(message: types.Message, state: FSMContext):
    currency_name = message.text.strip().upper()
    await state.update_data(currency_name=currency_name)
    await message.answer(f"Введите курс валюты {currency_name} к рублю (например: 90.5):")
    await CurrencyStates.next()

# Обработка курса валюты
@dp.message_handler(state=CurrencyStates.waiting_for_currency_rate)
async def process_currency_rate(message: types.Message, state: FSMContext):
    try:
        rate = float(message.text.replace(",", "."))
        data = await state.get_data()
        currency_name = data["currency_name"]
        currency_rates[currency_name] = rate
        await message.answer(f"Курс {currency_name} сохранён: {rate} RUB")
        await state.finish()
    except ValueError:
        await message.answer("Некорректный формат курса. Введите число, например: 92.5")

# Команда /convert — начало процесса конвертации
@dp.message_handler(commands=["convert"])
async def cmd_convert(message: types.Message):
    if not currency_rates:
        await message.answer("Нет сохранённых валют. Сначала используйте /save_currency")
        return
    available = ", ".join(currency_rates.keys())
    await message.answer(f"Введите название валюты для конвертации (доступные: {available}):")
    await ConvertStates.waiting_for_currency_name.set()

# Обработка названия валюты для конвертации
@dp.message_handler(state=ConvertStates.waiting_for_currency_name)
async def process_convert_currency(message: types.Message, state: FSMContext):
    currency_name = message.text.strip().upper()
    if currency_name not in currency_rates:
        await message.answer("Такая валюта не найдена. Попробуйте ещё раз.")
        return
    await state.update_data(currency_name=currency_name)
    await message.answer(f"Введите сумму в {currency_name} для конвертации в RUB:")
    await ConvertStates.next()

# Обработка суммы для конвертации
@dp.message_handler(state=ConvertStates.waiting_for_amount)
async def process_convert_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        data = await state.get_data()
        currency_name = data["currency_name"]
        rate = currency_rates[currency_name]
        result = amount * rate
        await message.answer(f"{amount} {currency_name} = {round(result, 2)} RUB\nКурс: 1 {currency_name} = {rate} RUB")
        await state.finish()
    except ValueError:
        await message.answer("Некорректная сумма. Введите число, например: 150.5")

# Команда /help
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "/start — Запуск бота\n"
        "/save_currency — Сохранить курс валюты\n"
        "/convert — Конвертировать валюту\n"
        "/help — Помощь"
    )

# Обработка всех прочих сообщений
@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.answer("Неизвестная команда. Напишите /help для списка доступных команд.")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
