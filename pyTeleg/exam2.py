# from pyexpat.errors import messages
# from re import template
from typing import Dict
# from urllib import request
# from email import message, message_from_file
import uvicorn
# from typing import List
from fastapi import FastAPI  # , Query, APIRouter, Path, BackgroundTasks
from fastapi import Response, Request
from fastapi.templating import Jinja2Templates

# import requests

import random
import os
import telebot
from telebot import types
from telebot.types import Message
import glob

import asyncio
import asyncssh
import sys
from telebot.async_telebot import AsyncTeleBot
# import paramiko

from PIL import Image


templates = Jinja2Templates(directory='/var/www/gr.tgram.ml/html')

TOKEN = '1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'
STICKER = 'CAACAgQAAxkBAAIEnWH2gp_bPNeujOzLrhUebjjVe8daAAIxAAP1mFALPtINSL0JxOAjBA'
STICKER2 = 'CAACAgIAAxkBAANsYd7QrvW61972Gz-ZEghYeF31iDQAAhcLAALuggcN6CvtTeUcCtkjBA'
PIC_1 = ''
PIC_2 = ''
PIC_cont = ''
PIC_style = ''
PHOTOPATH = '/var/www/gr.tgram.ml/html/photos/'
HOSTDIR = '/home/serg/photos/'

ssh_20GB_2GB_60rub = '195.234.208.168'  # тут будет модель
ssh_nvme_139rub = '45.130.151.35'  # этот, я тут
ssh_gramm_ml_99rub = '185.195.26.149'


async def ssh_send() -> None:
    print("ssh_send1")
    async with asyncssh.connect(host=ssh_20GB_2GB_60rub, port=22, username='serg', password='111') as conn:
        print("ssh_send2")
        async with conn.start_sftp_client() as sftp:
            # await sftp.mput('/var/www/gr.tgram.ml/html/photos/1-133420623AgACAgIAAxkBAAIDzmH1vgey9PuRVq-OfnrTSKz7JUuiAAJzuTEbY9mxSzgLdZKEwxW3AQADAgADeQADIwQ.jpg',  '/var/wwww/style/st_gr22.png')#    ('example.txt')
            print("ssh_send3")
            print(f' {PIC_cont=} \n {PIC_style= }\n {PIC_1= }\n {PIC_2= }\n ')
            await sftp.mput(PIC_1, PIC_cont)  # ('example.txt')
            print("ssh_send4")
            await sftp.mput(PIC_2, PIC_style)  # ('example.txt')
            print("ssh_send5")

    os.remove(PIC_1)
    print("ssh_send6")
    os.remove(PIC_2)
    
    print("ssh_send7")


def rename_PIC(pic_1, pic_style, user_id, chat_id):
    global PIC_1
    global PIC_2
    global PIC_cont
    global PIC_style
    pic_1_ext = pic_1.split('.')[-1]
    pic_2 = pic_1.split('.')[:-1]
    pic_style_ext = pic_style.split('.')[-1]
    pic_2style = pic_style.split('.')[:-1]
    PIC_cont = HOSTDIR + str(chat_id) + '__' + str(user_id) + '.' + pic_1_ext
    PIC_style = HOSTDIR + str(chat_id) + '__' + \
        str(user_id) + '_style.' + pic_style_ext
    PIC_1 = pic_1
    PIC_2 = pic_style


def resize_image(image_path,
                 user_id,
                 ext,
                 fixed_width=180):
    img = Image.open(image_path)
    width, height = img.size
    # output_image_path.replace(PHOTOPATH+)
    print(f'The original image size is {width} x {height} \n {image_path= } ')

    # получаем процентное соотношение
    # старой и новой ширины
    width_percent = (fixed_width / float(img.size[0]))
    # на основе предыдущего значения
    # вычисляем новую высоту
    height_size = int((float(img.size[1]) * float(width_percent)))
    # меняем размер на полученные значения
    new_image = img.resize((fixed_width, height_size))
    width, height = new_image.size
    print('The resized image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
    # new_image.show()
    if image_path[len(PHOTOPATH):len(PHOTOPATH) + 2] == '1-':
        output_name = '1-' + user_id + '.' + ext
    if image_path[len(PHOTOPATH):len(PHOTOPATH) + 2] == '2-':
        output_name = '2-' + user_id + '.' + ext
    new_image.save(output_name)


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
    print(json_data)
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
        await tg.send_message(message.chat.id, "Хотите узнать свой ник или ID?", reply_markup=markup)
    if message.html_text == '/start':
        await tg.reply_to(message, """\
Привет, я - бот.
Попробуй отправить мне смайлик!\
Напиши мне любое слово, а угадаю твой возраст!
""")
    # print(message.html_text)
    if message.html_text == '/help':
        await tg.reply_to(message, """\
В этом боте Вы можете перенести стиль с одного изображения на другое изображение. Чтобы начать, нажмите на значок скрепки и загрузите два изображения. Затем выберите которое из них будет Style
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
        await tg.send_message(call.message.chat.id, 'Нажмите одну из кнопок...', reply_markup=markup_reply)

    elif call.data == 'no':
        # , reply_markup=markup_reply)
        await tg.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="_")
        await tg.send_message(call.message.chat.id, 'I`m shut up', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == '1':
        rename_PIC(PIC_1, PIC_2, call.message.from_user.id,
                   call.message.chat.id)
        # ssh_send()#PIC_1, PIC_2, call.message.from_user.id, call.message.chat.id)
        await as_main()
        await tg.send_message(call.message.chat.id, 'Ok 1 - style, wait...', reply_markup=types.ReplyKeyboardRemove())
    elif call.data == '2':
        rename_PIC(PIC_2, PIC_1, call.message.from_user.id,
                   call.message.chat.id)
        # ssh_send()#PIC_2, PIC_1, call.message.from_user.id, call.message.chat.id)
        await as_main()
        await tg.send_message(call.message.chat.id, 'Ok 2 - style, wait...', reply_markup=types.ReplyKeyboardRemove())
      # picture 1 is style

    await tg.answer_callback_query(callback_query_id=call.id)


@tg.message_handler(content_types=['text', 'photo', 'sticker'])
@tg.edited_message_handler(content_types=['text'])
async def gettext(message: Message):
    # print(f'{message.content_type=}')
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
        # print(f' {src=}')
        with open(src, 'wb') as f:
            f.write(download_file)
            resize_image(src, str(message.from_user.id), file_ext)
        if src[len(PHOTOPATH):len(PHOTOPATH)+2] == '2-':
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup2 = types.InlineKeyboardMarkup(row_width=1)
            items_1pic = types.InlineKeyboardButton(
                text="THis Pic Style", callback_data='1')
            markup.add(items_1pic)
            print('send 1')
            print(f'{PIC_1=}')
            await tg.send_photo(message.chat.id, photo=open('1-'+str(message.from_user.id) + '.' + file_ext, 'rb'), caption='выбор фото с которого будет взят стиль', reply_markup=markup)

            items_2pic = types.InlineKeyboardButton(
                text="THis Pic Style", callback_data='2')
            markup2.add(items_2pic)
            print('send 2')
            print(f'{PIC_2=}')
            await tg.send_photo(message.chat.id, photo=open('2-'+str(message.from_user.id) + '.' + file_ext, 'rb'), caption='выбор фото с которого будет взят стиль', reply_markup=markup2)
            for f in glob.glob('/home/serg/*' + str(message.from_user.id) + '*'):
                os.remove(f)

        # file_info.file_path[-4:]
        # print(message)
    if message.content_type not in ['text', 'photo']:
        print(message)
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


@ app.get('/')
async def main(request: Request):
    pass
    # print(' get ')
    # meassage = response#.set_cookie(key="user_nonce", value="")
    # print(response)
    # print(message)
    return templates.TemplateResponse('index.html', {'request': request})


async def as_main():
    task1 = asyncio.create_task(ssh_send())
    # планируем одновременные вызовы:
    await asyncio.gather(task1)


if __name__ == "__main__":
    # asyncio.run(as_main())
    uvicorn.run("exam2:app", host="0.0.0.0", workers=3,  port=443, log_level="debug",  reload=True,  ssl_keyfile="/etc/letsencrypt/live/gr.tgram.ml/privkey.pem",
                ssl_certfile="/etc/letsencrypt/live/gr.tgram.ml/fullchain.pem")  # , reload_dirs = ["/var/www/gr.tgram.ml/html/$
