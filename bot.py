import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8427894905:AAGzwZ9d-eot8oQujYfSbvlFqG4pYBQn4nI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Купить подарок", callback_data="buy_gift")],
        [InlineKeyboardButton(text="📦 Мои заказы", callback_data="my_orders")],
    ])
    await message.answer(
        "Добро пожаловать в магазин подарков!\n"
        "У нас лучшие цены и быстрая доставка.",
        reply_markup=kb,
    )

@dp.callback_query(lambda c: c.data == "buy_gift")
async def buy_gift(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 499₽", callback_data="pay_499")],
        [InlineKeyboardButton(text="Оплатить 999₽", callback_data="pay_999")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ])
    await callback.message.edit_text(
        "Выберите подарок:\n"
        "• Стандартный — 499₽\n"
        "• Премиум — 999₽",
        reply_markup=kb,
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("pay_"))
async def pay(callback: types.CallbackQuery):
    amount = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Для оплаты {amount}₽ переведите сумму на карту:\n"
        "`2200 0000 0000 0000`\n"
        "После оплаты отправьте чек сюда.",
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "my_orders")
async def my_orders(callback: types.CallbackQuery):
    await callback.message.edit_text("У вас пока нет заказов.")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await start(callback.message)
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())