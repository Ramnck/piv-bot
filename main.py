import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from pipeline import process_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN is not set")

bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Form(StatesGroup):
    waiting_for_preference = State()
    waiting_for_photo = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Привет! Какие сорта или вкусы тебе нравятся?")
    await state.set_state(Form.waiting_for_preference)


@dp.message(Form.waiting_for_preference)
async def preference_received(message: types.Message, state: FSMContext) -> None:
    await state.update_data(preference=message.text)
    await message.answer("Отлично! Теперь пришли фотографию полки с пивом.")
    await state.set_state(Form.waiting_for_photo)


@dp.message(Form.waiting_for_photo, F.photo)
async def photo_received(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    preference: str = data.get("preference", "")

    photo = message.photo[-1]
    path = Path(f"photo_{message.from_user.id}.jpg")
    await bot.download(photo, destination=path)
    await message.answer("Изображение получено, подожди немного...")

    result = process_image(path, preference)
    await message.answer(result)

    try:
        path.unlink()
    except OSError as exc:
        logger.error("Cannot delete photo %s: %s", path, exc)

    await state.clear()


@dp.message(Form.waiting_for_photo)
async def not_photo(message: types.Message) -> None:
    await message.answer("Нужно прислать фотографию.")


async def main() -> None:
    logger.info("Bot started")
    await dp.start_polling(bot)
    logger.info("Bot finished")


if __name__ == "__main__":
    asyncio.run(main())

