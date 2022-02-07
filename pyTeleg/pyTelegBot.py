
import random
import telebot
from telebot import types
from telebot.types import Message


import asyncio
from telebot.async_telebot import AsyncTeleBot

TOKEN = '1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'
STICKER = 'CAACAgIAAxkBAANsYd7QrvW61972Gz-ZEghYeF31iDQAAhcLAALuggcN6CvtTeUcCtkjBA'

# tg = telebot.TeleBot(TOKEN)
tg = AsyncTeleBot(TOKEN)

# bot.set_webhook(url="http://tlg.gramm.ml", certificate=open('mycert.pem'))

# Handle '/start' and '/help'


@tg.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    markup = types.InlineKeyboardMarkup()
    items_yes = types.InlineKeyboardButton(text="YES", callback_data='yes')
    items_no = types.InlineKeyboardButton(text="NO", callback_data='no')

    markup.add(items_yes, items_no)
    await tg.send_message(message.chat.id, "gggggggggggg", reply_markup=markup)

    tg.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@tg.callback_query_handler(func=lambda call: True)
async def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        items_id = types.KeyboardButton('MyID')
        items_username = types.KeyboardButton('MyNIC')

        markup_reply.add(items_id, items_username)
        await tg.send_message(call.message.chat.id, 'Press one of key', reply_markup=markup_reply)

    elif call.data == 'no':
        await tg.send_message(call.message.chat.id, 'I`m shut up', reply_markup=types.ReplyKeyboardRemove())
    await tg.answer_callback_query(callback_query_id=call.id)


# @bot.inline_handler(lambda query: query.query == 'text')
# async def query_text(inline_query):
#     await bot.reply_to(inline_query)
#     # Query message is text

# # @bot.inline_handler(lambda query: query.query == 'text')
# # async def query_text(inline_query):
# #     print (inline_query)
# #     try:
# #         r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
# #         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
# #         await bot.answer_inline_query(inline_query.id, [r, r2])
# #     except Exception as e:
# #         print(e)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])

@tg.message_handler(content_types=['sticker'])
async def echo_message(message: Message):
    # print (message.sticker)
    await tg.send_sticker(message.chat.id, STICKER)


@tg.message_handler(content_types=['text'])
@tg.edited_message_handler(content_types=['text'])
async def gettext(message: Message):
    markup_remove = types.ReplyKeyboardRemove()
    if message.text == "MyID":
        await tg.send_message(message.chat.id, f'Your ID: {message.from_user.id}', reply_markup=markup_remove)
    elif message.text == "MyNIC":
        await tg.send_message(message.chat.id, f'Your NIC: {message.from_user.first_name}', reply_markup=markup_remove)
    else:
        await tg.reply_to(message, str(random.randint(0, 100)))


# @tg.message_handler(func=lambda message: True)
# async def echo_message(message: Message):
#     # print (message)


asyncio.run(tg.polling())
