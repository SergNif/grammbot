from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
from datetime import datetime
from flask_sslify import SSLify
# 1. Прием сообщений
# 2. Отправка сообщений

app = Flask(__name__)
sslify = SSLify(app)

URL = 'https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/'

def write_json( data, file_name='answer.json' ):
    with open( file_name, 'w') as f:
        json.dump( data, f, indent=2, ensure_ascii=False )


# def get_update():
#     url = URL + 'getUpdates'
#     r = requests.get( url )
#     write_json(r.json())
#     return r.json()

def send_message(chat_id, text='bla-bla-bla'):    
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post( url, json = answer)
    return r.json()


#  c985676a-047f-474c-8d4c-21bc919b17cb

# curl -H "X-CMC_PRO_API_KEY: c985676a-047f-474c-8d4c-21bc919b17cb" -H "Accept: application/json" -d "start=1&limit=5000&convert=USD" -G https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest

def get_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'c985676a-047f-474c-8d4c-21bc919b17cb',
    }
    with open('val.json') as f:
        d = json.load(f)    
    if datetime.today().day != int(d['status']['timestamp'][8:10]):
        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        #   print(data)
            write_json(data, 'val.json')
                # print(d)
            price = data['data']
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            pass
            # print(e)
            # res_price = e
    with open('val.json') as f:
        d = json.load(f)
        res_price = d['data'][0]['quote']['USD']['price']
    
    
    return round(res_price,2) if res_price else e    

#  sergNIF@#201pyth

@app.route('/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        r= request.get_json()
        # print(f'{r=} ')
        write_json(r)
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        print (message)
        if 'bitcoin' in message:
            send_message(chat_id, text = get_price())# 'очень дорогой')
        return jsonify(r)
    return '<h1>Bot 00 welcome</h1>'

#    https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/setWebhook?url=https://c3858dd79c91c0.localhost.run
#    https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/deleteWebhook
#    https://api.telegram.org/bot1618584232:AAHmGvkcP91w9gsxM9Vhw5_FdlTJlULD6vg/setWebhook?url=https://9260-85-249-167-118.ngrok.io


# def main():
#     # r = requests.get(URL + 'getMe')
#     # print (r.json())
#     # write_json(r.json())
#     # r = get_update()
#     # chat_id = r['result'][-1]['message']['chat']['id']
#     # print(f'{chat_id=} ')
#     # send_message(chat_id)
#     pass



if __name__ == '__main__':
    app.run()
    # main()
    # get_update()

