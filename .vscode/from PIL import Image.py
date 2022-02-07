from PIL import Image
import telebot
import os

DIR = '/var/www/gr.tgram.ml/html'
IMAGE_DIR = DIR + '/Images/' 
STORAGE_DIR = DIR + '/Storage'
TOKEN = '1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg'
STICKER = 'CAACAgQAAxkBAAIEnWH2gp_bPNeujOzLrhUebjjVe8daAAIxAAP1mFALPtINSL0JxOAjBA'
STICKER2 = 'CAACAgIAAxkBAANsYd7QrvW61972Gz-ZEghYeF31iDQAAhcLAALuggcN6CvtTeUcCtkjBA'
PIC_1 = ''
PIC_2 = ''
PIC_cont = ''
PIC_style = ''
PHOTOPATH = DIR + '/photos/'
HOSTDIR = '/var/wwww/style/Images/'    #'/home/serg/photos/'
FLAG_READY_SERVER = False


SEND_DIR = '/var/wwww/style/Remov'

tg = telebot.TeleBot("TOKEN", parse_mode=None)


file_list = [f for f in os.listdir(SEND_DIR)]
for f in file_list:
    chat_id = f.replace(IMAGE_DIR,'').split('__')[0]
    tg.send_photo(chat_id, photo=open(SEND_DIR + '/' + f))
