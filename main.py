import logging

from aiogram import Bot, Dispatcher, executor, types
from googletrans import Translator
from oxford import getDefinitions

translator = Translator()

logging.basicConfig(level=logging.INFO)

API_TOKEN = "5111092152:AAFVw7oqqu3t0qtCAM1aSa9_4cNmnS7pOKY"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Ассалому Алайкум!\n@TranslatorEasy_Bot дан фойдаланаётганингиздан хурсандмиз 🙂.")
    
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply("Бу бот 🤖 матинни инглиз (ёки ўзбек) тилига таржима қилади.")
    
@dp.message_handler()
async def own_translate(message: types.Message):
    
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = "uz" if lang == "en" else "en"
        await message.reply(translator.translate(message.text, dest).text)
    else:
        if lang=='en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text
            
        see_oxford = getDefinitions(word_id)
        if see_oxford:
            await message.reply(f"Word:    {word_id} \nDefinitions:\n{see_oxford['definitions']}")
            if see_oxford.get('audio'):
                await message.reply_voice(see_oxford['audio'])
        else:
            await message.reply("Бундай сўз топилмади 🤔")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)