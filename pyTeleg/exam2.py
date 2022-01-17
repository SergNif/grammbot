from pyexpat.errors import messages
from re import template
from typing import Dict
from urllib import request
# from email import message, message_from_file
import uvicorn
from typing import List
from fastapi import FastAPI, Query, APIRouter, Path
from fastapi import Response, Request
from fastapi.templating import Jinja2Templates

import requests

import random
import os
import telebot
from telebot import types
from telebot.types import Message
import json

import asyncio
from telebot.async_telebot import AsyncTeleBot
import paramiko

templates = Jinja2Templates(directory='/var/www/gr.tgram.ml/html')

TOKEN = '1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'
STICKER = 'CAACAgIAAxkBAANsYd7QrvW61972Gz-ZEghYeF31iDQAAhcLAALuggcN6CvtTeUcCtkjBA'
PIC_1 = ''
PIC_2 = ''
PHOTOPATH = '/var/www/gr.tgram.ml/html/photos/'

ssh_20GB_2GB_60rub = '195.234.208.168'  # тут будет модель
ssh_nvme_139rub = '45.130.151.35'  # этот, я тут
ssh_gramm_ml_99rub = '185.195.26.149'


def ssh_send(pic_1, pic_style, user_id):
    pic_1_ext = pic_1.split('.')[-1]
    pic_2 = pic_1.split('.')[:-1]
    pic_style_ext = pic_style.split('.')[-1]
    pic_2style = pic_style.split('.')[:-1]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_20GB_2GB_60rub, username='serg', password='111',
                look_for_keys=True, key_filename='/home/serg/.ssh/id_ed25519.pub', port=22)
    # ssh.connect(hostname = '185.195.26.149', username = 'serg', look_for_keys = True, port = 22 )
    # ssh.connect(hostname = '185.195.26.149', username = 'serg', password = '111', port = 22 )
    ftp_client = ssh.open_sftp()
    # ftp_client.chown('serg', -R /home/serg)
    # ftp_client.chmod(777 -R /home/serg)

    ftp_client.chdir('/home/serg/photos')
    # ftp_client.put('/home/serg/gram/trfile.txt', 'paramiko_files.py')
    ftp_client.put(pic_1, str(user_id) + '.' + pic_1_ext)
    ftp_client.put(pic_style, str(user_id) + '_style.' + pic_style_ext)

    print(f'{ftp_client.getcwd()=} ')
    ftp_client.close()
    ssh.close()




# tb = telebot.TeleBot(TOKEN)
tg = AsyncTeleBot(TOKEN)
# tb.remove_webhook()
# tb.set_webhook(url="https://gr.tgam.ml", certificate=open('/var/www/uvic/fullchain.pem'))
# https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/setWebhook?url=https://gr.tgram.ml/
app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)


@app.post('/')
async def lower_case(json_data: Dict):
    # text = json_data.get('text')
    # print(json_data)
    # await star_button()
    update = telebot.types.Update.de_json(json_data)
    await tg.process_new_updates([update])
    # return json_data

# tg.set_update_listener(lower_case)  #infinity_polling(interval=0, timeout=20)


@tg.message_handler(commands=['help', 'start', 'button'])
async def send_welcome(message: Message):
    if message.html_text == '/button':
        markup = types.InlineKeyboardMarkup(row_width=2)
        items_yes = types.InlineKeyboardButton(text="YES", callback_data='yes')
        items_no = types.InlineKeyboardButton(text="NO", callback_data='no')

        markup.add(items_yes, items_no)
        await tg.send_message(message.chat.id, "gggggggggggg", reply_markup=markup)
    if message.html_text == '/start':
        await tg.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")
    # print(message.html_text)
    if message.html_text == '/help':
        await tg.reply_to(message, """\
В этом боте Вы можете перенести стиль с одного изображения на другое изображение. Для этого нажимайте на соответствующие кнопки
Вам надо загрузить боту два изображения и выбрать с какого из них перенести стиль\
""")


@tg.message_handler(content_types=['new_chat_members'])
async def star_button(message: Message):
    await tg.reply_to(message, text='hello')
    markup = types.InlineKeyboardMarkup(row_width=3)
    items_talk = types.InlineKeyboardButton(text="Talk", callback_data='yes')
    items_tr_st = types.InlineKeyboardButton(
        text="Tranform style", callback_data='no')
    items_no = types.InlineKeyboardButton(text="NO", callback_data='no')

    markup.add(items_talk, items_tr_st, items_no)
    await tg.send_message(message.chat.id, "Добрый день!", reply_markup=markup)


@tg.callback_query_handler(func=lambda call: True)
async def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        items_id = types.KeyboardButton('MyID')
        items_username = types.KeyboardButton('MyNIC')

        markup_reply.add(items_id, items_username)
        # , reply_markup=markup_reply)
        await tg.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="_")
        await tg.send_message(call.message.chat.id, 'Press one of key', reply_markup=markup_reply)

    elif call.data == 'no':
        # , reply_markup=markup_reply)
        await tg.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="_")
        await tg.send_message(call.message.chat.id, 'I`m shut up', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == '1':
        ssh_send(PIC_1, PIC_2, call.message.from_user.id)
        await tg.send_message(call.message.chat.id, 'Ok 1 - style, wait...', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == '2':
        ssh_send(PIC_2, PIC_1, call.message.from_user.id)
        await tg.send_message(call.message.chat.id, 'Ok 2 - style, wait...', reply_markup=types.ReplyKeyboardRemove())
      # picture 1 is style

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

# @tg.message_handler(content_types=['sticker'])
# async def echo_message(message: Message):
    # print (message.sticker)


@tg.message_handler(content_types=['text', 'photo', 'sticker'])
@tg.edited_message_handler(content_types=['text'])
async def gettext(message: Message):
    print(f'{message.content_type=}')
    if message.content_type == 'sticker':
        await tg.send_sticker(message.chat.id, STICKER)
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
        # print(file_id)
        # gt = json.loads(message)
        # with open('photo.json', 'w') as f:
        #     json.dump(message.json, f)

        file_info = await tg.get_file(file_id)
        file_name, file_ext = file_info.file_path.split('.')
        download_file = await tg.download_file(file_name + '.' + file_ext)
        tmp = str(message.from_user.id) + file_id + '.' + file_ext
        # print(f' {tmp=}')
        src = name_photo(message, tmp)
        # file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        print(f' {src=}')
        with open(src, 'wb') as f:
            f.write(download_file)
        if src[len(PHOTOPATH):len(PHOTOPATH)+2] == '2-':
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup2 = types.InlineKeyboardMarkup(row_width=1)
            items_1pic = types.InlineKeyboardButton(
                text="THis Pic Style", callback_data='1')
            markup.add(items_1pic)
            print('send 1')
            print(f'{PIC_1=}')
            await tg.send_photo(message.chat.id, photo=open(PIC_1, 'rb'), caption='выбор фото с которого будет взят стиль', reply_markup=markup)

            items_2pic = types.InlineKeyboardButton(
                text="THis Pic Style", callback_data='2')
            markup2.add(items_2pic)
            print('send 2')
            print(f'{PIC_2=}')
            await tg.send_photo(message.chat.id, photo=open(PIC_2, 'rb'), caption='выбор фото с которого будет взят стиль', reply_markup=markup2)

        # file_info.file_path[-4:]
        # print(message)
    else:
        await tg.send_sticker(message.chat.id, STICKER)


def name_photo(message, name):
    global PIC_1
    global PIC_2
    # определение текущей рабочей директории
    rez = sorted(os.listdir(PHOTOPATH))
    ln = len(str(message.from_user.id))
    fil = 0
    print(f'{rez=}')
    for n, item in enumerate(rez):
        print(f'{type(item)=} \n {item=}')
        print(f'{item[2:ln+2]=}')
        if item[:ln+2] == '1-' + str(message.from_user.id):
            fil += 1
            PIC_2 = PHOTOPATH + "2-" + name.split('/')[-1]  # item[2:]
            print(f'{PIC_2=}')
            return PIC_2
    if fil == 0:
        PIC_1 = PHOTOPATH + '1-' + name.split('/')[-1]
        return PIC_1


# @tg.message_handler(func=lambda message: True)
# async def echo_message(message: Message):
#     # print (message)

# asyncio.run(tg.polling())

# # 1

# @app.post('/')
# async def main(response: Response):
#     print(' post ')
#     meassage = response#.set_cookie(key="user_nonce", value="")
#     print(response)
#     print(message)
#     return message

# @ app.route('/')
# async def main(response: Response):
#     pass
#     # print(' route ')
#     # meassage = response#.set_cookie(key="user_nonce", value="")
#     # print(response)
#     # print(message)
#     # return message

@ app.get('/')
async def main(request: Request):
    pass
    # print(' get ')
    # meassage = response#.set_cookie(key="user_nonce", value="")
    # print(response)
    # print(message)
    return templates.TemplateResponse('index.html', {'request': request})

# 'curl -X POST http://tlg.gramm.ml/1618584232%3AAAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'

# @app.get('/')
# def home():
#     return{'key': 'Hello'}


if __name__ == "__main__":
    uvicorn.run("exam2:app", host="0.0.0.0", workers=3,  port=443, log_level="debug",  reload=True,  ssl_keyfile="/etc/letsencrypt/live/gr.tgram.ml/privkey.pem",
                ssl_certfile="/etc/letsencrypt/live/gr.tgram.ml/fullchain.pem")  # , reload_dirs = ["/var/www/gr.tgram.ml/html/$
