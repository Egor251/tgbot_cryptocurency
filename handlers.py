from aiogram import Router
import asyncio
from aiogram.types import Message
from aiogram.filters import Command
import db
import config
from coinmarketcap import Crypto


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Инструкция по использованию:\n\n"
                     "Для добавления сигнала к валютной паре напиши например: add BTC min 64000\n\n"
                     "Тогда бот пришлёт уведомление при падении курса ниже 64 000 usd\n\n"
                     "Чтобы удалить сигнал введи: remove BTC\n\n"
                     "Чтобы увидеть уже существующие сигналы введи: Show\n\n"
                     "Чтобы снова увидеть это сообщение напиши /start")
    while True:
        result = 1
        data = db.DB().select('SELECT * FROM main_db')
        if len(data) != 0:
            for item in data:
                result = 1
                price = Crypto().get_price(item[0])
                if item[1] == 'min':
                    result = price - float(item[2])
                else:
                    result = float(item[2]) - price
                if result < 0:
                    await msg.answer(f'Signal price for {item[0]} was reached! Current price is {price} USD')
                    sql = f"DELETE FROM main_db WHERE crypto='{item[0]}' AND value='{item[2]}'"
                    db.DB().exec(sql)
        await asyncio.sleep(float(config.time))


@router.message()
async def message_handler(msg: Message):
    text = msg.text.split(' ')

    two = ['min', 'max']

    if text[0].lower() == 'show':
        all_signals = db.DB().select('SELECT * FROM main_db')
        await msg.answer(f"Current signals are: \n {all_signals}")
    else:
        if text[0].lower() == 'add':
            if text[2].lower() not in two or len(text) != 4:
                await msg.answer(f"Wrong command! Try again.")
            else:
                db.DB().insert(text[1].upper(), text[2].lower(), text[3].lower())
                await msg.answer(f"Signal for {text[1]} was added\n"
                                 f"Parameters: {text[2]}: {text[3]} USD")
        elif text[0].lower() == 'remove':
            if len(text) != 2:
                await msg.answer(f"Wrong command! Try again.")
            else:
                db.DB().exec(f"DELETE FROM main_db WHERE crypto='{text[1].upper()}'")
        else:
            await msg.answer(f"Wrong command! Try again.")
    #await msg.answer(f"Твой ID: {msg.from_user.id}")
    #await msg.answer(type(msg))