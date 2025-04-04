import asyncio
import os
from parser import Parser

import torch
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from PIL import Image
from safetensors.torch import load_file
from transformers import ViTForImageClassification, ViTImageProcessor

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

class_names = {
    0: "Балтика 3",
    1: "Балтика 7",
    2: "Budweiser",
    3: "Gosser",
    4: "Guinness",
    5: "Жигулевское",
    6: "Клинское",
    7: "Kozel",
    8: "Крушовице",
    9: "Оболонь",
    10: "Сибирская Корона",
    11: "Staropramen",
    12: "Stella Artois",
    13: "Tuborg",
    14: "Heineken",
    15: "Хамовники",
    16: "Spaten",
    17: "Efes",
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
user_states = {}
welcome_message = "Привет! Я бот для распознавания и описания пива. Сфотографируй бутылку и узнай о ней всё!"
info_message = "Отправь фото бутылки, и я расскажу про пиво."
menu_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Запросить информацию о пиве")]],
    resize_keyboard=True,
)

model_path = "beer_model/model.safetensors"
model_weights = load_file(model_path)
new_model = ViTForImageClassification.from_pretrained(
    "google/vit-base-patch16-224-in21k", num_labels=18
)
model_dict = new_model.state_dict()
model_dict.update(model_weights)
new_model.load_state_dict(model_dict)

model = new_model
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
parser = Parser()


def prepare_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return processor(images=image, return_tensors="pt").pixel_values


def predict_image(image_path):
    inputs = prepare_image(image_path)
    with torch.no_grad():
        outputs = model(inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0, predicted_class].item()
    if confidence < 0.35:
        return "Фото не относится ни к одному из известных классов", None
    return class_names.get(predicted_class, "Неизвестный класс"), confidence


@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_states[message.from_user.id] = "new"
    await message.answer(welcome_message, reply_markup=menu_markup)


@dp.message(lambda msg: msg.text == "Запросить информацию о пиве")
async def beer_request(message: types.Message):
    user_states[message.from_user.id] = "waiting_for_photo"
    await message.answer(info_message)


@dp.message(lambda msg: msg.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "waiting_for_photo":
        user_states[user_id] = "processing_photo"
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await message.answer("Фото получено. Обрабатываю...")

        await bot.download_file(file_path, "user_image.jpg")

        predicted_class, confidence = predict_image("user_image.jpg")

        if confidence is None:
            beer_info = predicted_class
        else:
            beer_data = parser.get_data(predicted_class)
            if beer_data:
                beer_info = (
                    f"Предсказанный класс: {predicted_class}\n"
                    f"Страна: {beer_data.country}\n"
                    f"Тип: {beer_data.beer_type}\n"
                    f"Цена: {beer_data.cost} руб.\n"
                    f"Рейтинг: {beer_data.score}\n"
                    f"Крепость: {beer_data.strength}%\n"
                    f"Описание: {beer_data.conclusion}"
                )
            else:
                beer_info = "Информация о предсказанном классе отсутствует."

        await message.answer(beer_info)

        user_states[user_id] = "finished"
    else:
        await message.answer("Используй кнопку меню, чтобы начать новый запрос.")


async def main():
    await bot.delete_webhook()
    print("Bot started")
    await dp.start_polling(bot)
    print("Bot finished")


if __name__ == "__main__":
    asyncio.run(main())
