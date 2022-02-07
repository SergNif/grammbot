from typing import Dict
from email import message
import uvicorn
from typing import List
from fastapi import FastAPI, Query, APIRouter, Path
from fastapi import Response

import requests

import random
import os
import telebot
from telebot import types
from telebot.types import Message
import json

import asyncio
from telebot.async_telebot import AsyncTeleBot

TOKEN = '1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'
STICKER = 'CAACAgIAAxkBAANsYd7QrvW61972Gz-ZEghYeF31iDQAAhcLAALuggcN6CvtTeUcCtkjBA'


# tb = telebot.TeleBot(TOKEN)
tg = AsyncTeleBot(TOKEN)
# tb.remove_webhook()
# tb.set_webhook(url="https://tlg.gramm.ml", certificate=open('/var/www/uvic/fullchain.pem'))
# https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/setWebhook?url=https://tlg.gramm.ml/1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/
app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

@app.post('/')
async def lower_case(json_data: Dict):
    # text = json_data.get('text')
    print(json_data)
    update = telebot.types.Update.de_json(json_data)
    await tg.process_new_updates([update])
    # return json_data

# tg.set_update_listener(lower_case)  #infinity_polling(interval=0, timeout=20)

@tg.message_handler(commands=['help', 'start', 'button'])
async def send_welcome(message: Message):
    print(message)
    if message.html_text == '/button':
        markup = types.InlineKeyboardMarkup(row_width = 2)
        items_yes = types.InlineKeyboardButton(text="YES", callback_data='yes')
        items_no = types.InlineKeyboardButton(text="NO", callback_data='no')

        markup.add(items_yes, items_no)
        await tg.send_message(message.chat.id, "gggggggggggg", reply_markup=markup)
    if message.html_text == '/start':
        await tg.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@tg.callback_query_handler(func=lambda call: True)
async def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        items_id = types.KeyboardButton('MyID')
        items_username = types.KeyboardButton('MyNIC')

        markup_reply.add(items_id, items_username)
        await tg.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = "_")#, reply_markup=markup_reply)
        await tg.send_message(call.message.chat.id, 'Press one of key', reply_markup=markup_reply)

    elif call.data == 'no':
        await tg.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = "_")#, reply_markup=markup_reply)
        await tg.send_message(call.message.chat.id, 'I`m shut up', reply_markup=types.ReplyKeyboardRemove())
    await tg.answer_callback_query(callback_query_id=call.id)


@tg.message_handler(content_types=['sticker'])
async def echo_message(message: Message):
    # print (message.sticker)
    await tg.send_sticker(message.chat.id, STICKER)


@tg.message_handler(content_types=['text', 'photo'])
@tg.edited_message_handler(content_types=['text'])
async def gettext(message: Message):
    if message.content_type == 'text':
        markup_remove = types.ReplyKeyboardRemove()
        if message.text == "MyID":
            await tg.send_message(message.chat.id, f'Your ID: {message.from_user.id}', reply_markup=markup_remove)
            # await tg.send_message(message.chat.id, f'Your ID: {message.from_user.id}', reply_markup=markup_remove)
        elif message.text == "MyNIC":
            await tg.send_message(message.chat.id, f'Your NIC: {message.from_user.first_name}', reply_markup=markup_remove)
        else:
            await tg.reply_to(message, str(random.randint(0, 100)))
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        # gt = json.loads(message)
        # with open('photo.json', 'w') as f:
        #     json.dump(message.json, f)

        file_info = await tg.get_file(file_id)
        file_name, file_ext = file_info.file_path.split('.')
        download_file = await tg.download_file(file_name +'.' + file_ext)
        src = os.getcwd() + '/photos/' + message.photo[0].file_unique_id + '.'+  file_ext
        # file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        with open(src, 'wb') as f:
            f.write(download_file)
        # file_info.file_path[-4:]
        # print(message)


@app.get('/')
def home():
    return{'key': 'Hello'}



if __name__ == "__main__":
    uvicorn.run("exam:app", host="0.0.0.0",  port=4443, log_level="debug", reload = True,  ssl_keyfile="/etc/letsencrypt/live/gr.tgram.ml/privkey.pem", ssl_certfile="/etc/letsencrypt/live/gr.tgram.ml/fullchain.pem") #, reload_dirs = ["/var/www/gr.tgram.ml/html/"]

# #    uvicorn.run("exam:app", host="0.0.0.0",  port=8001, log_level="debug", reload = True)
