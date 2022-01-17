from typing import Dict
from email import message
import uvicorn
from schemas import Book
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



# @tg.message_handler(func=lambda message: True)
# async def echo_message(message: Message):
#     # print (message)

# asyncio.run(tg.polling())

# # 1

@app.post('/1618584232%3AAAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg')
async def main(response: Response):
    print(' uuu ')
    meassage = response#.set_cookie(key="user_nonce", value="")
    print(response)
    print(message)
    return message

@app.route('/')
async def main(response: Response):
    print(' uuu ')
    meassage = response#.set_cookie(key="user_nonce", value="")
    print(response)
    print(message)
    return message

@app.get('/1618584232%3AAAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg')
async def main(response: Response):
    print(' uuu ')
    meassage = response#.set_cookie(key="user_nonce", value="")
    print(response)
    print(message)
    return message

'curl -X POST http://tlg.gramm.ml/1618584232%3AAAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'

@app.get('/')
def home():
    return{'key': 'Hello'}

@app.get('/{pk}')    
def get_item(pk: int, q: str = None):
    return {'key': pk, 'q': q}

@app.get('/user/{pk}/items/{item}/')    
def get_user_item(pk: int, item: str):
    return {'user': pk, 'item': item}

@app.post('/book')
def create_book(item: Book):
    return item

@app.get('/book')    
def get_book(q: List [str] = Query(['test1', 'test2'], min_length = 2, max_length = 5, description = "Search book" )):
    return q


@app.get('/book/{pk}')    
def get_single_book(pk: int = Path(..., gt = 3, le = 20), pages: int = Query(None, gt=10, le=500)):#, q: str = None):
    return {'key': pk, 'pages': pages}#, 'q': q}
# # 2
# api_router = APIRouter()

# # 3
# @api_router.get("/", status_code=200)
# def root() -> dict:
#     """
#     Root Get
#     """
#     return {"msg": "Hello, World!"}

# # 4
# app.include_router(api_router)


# # async def app(scope, receive, send):
#     # assert scope['type'] == 'http'
# # 
#     # await send({
#         # 'type': 'http.response.start',
#         # 'status': 200,
#         # 'headers': [
#             # [b'content-type', b'text/plain'],
#         # ],
#     # })
#     # await send({
#         # 'type': 'http.response.body',
#         # 'body': b'Hello, world!',
#     # })
# # 

#import declaration
#from fastapi import FastAPI, Form, Request
#from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
#from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
#
#from pydantic import BaseModel
#import random
#import uvicorn
#
## initialization
#app = FastAPI()
#
## mount static folder to serve static files
#app.mount("/static", StaticFiles(directory="/var/www/uvic/static"), name="static")
#
## Jinja2 template instance for returning webpage via template engine
#templates = Jinja2Templates(directory="/var/www/uvic/templatess")
#
## Pydantic data model class
#class Item(BaseModel):
#    #language: str
#    language = 'english'
#
## hello world, GET method, return string
#@app.get("/", response_class=PlainTextResponse)
#async def hello():
#    return "Hello World!"
#
## random number, GET method, return string
#@app.get('/random-number', response_class=PlainTextResponse)
#async def random_number():
#    return str(random.randrange(100))
#
## check isAlpha, GET method, query parameter, return JSON
#@app.get('/alpha')
#async def alpha(text: str):
#    result = {'text': text, 'is_alpha' : text.isalpha()}
#
#    return result
#
## create new user, POST method, form fields, return JSON
#@app.post('/create-user')
#async def create_user(id: str = Form(...), name: str = Form(...)):
#    # code for authentication, validation, update database
#    
#    data = {'id': id, 'name': name}
#    result = {'status_code': '0', 'status_message' : 'Success', 'data': data}
#
#    return result
#
## update language, PUT method, JSON input, return string
#@app.put('/update-language', response_class=PlainTextResponse)
#async def update_language(item: Item):
#    language = item.language
#
#    return "Successfully updated language to %s" % (language)
#    
## serve webpage, GET method, return HTML
#@app.get('/get-webpage', response_class=HTMLResponse)
#async def get_webpage(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request, "message": "Contact Us"})
#
## file response, GET method, return file as attachment
#@app.get('/get-language-file/{language}')
#async def get_language_file(language: str):
#    file_name = "%s.json" % (language)
#    file_path = "./static/language/" + file_name
#
#    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


if __name__ == "__main__":
    uvicorn.run("exam:app", host="0.0.0.0",workers=3,  port=443, log_level="debug",  reload = True,  ssl_keyfile="/etc/letsencrypt/live/gr.tgram.ml/privkey.pem", ssl_certfile="/etc/letsencrypt/live/gr.tgram.ml/fullchain.pem") #, reload_dirs = ["/var/www/gr.tgram.ml/html/$
# 