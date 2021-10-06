import pandas as pd
import json
import requests
from flask import Flask, request, Response
import os
import seaborn as sns

# constants
TOKEN = '1964746514:AAGmnUoclbp8R1NczhX38vt8_4Da10u4uW4'

# # Info about the Bot
# https://api.telegram.org/bot1964746514:AAGmnUoclbp8R1NczhX38vt8_4Da10u4uW4/getMe
        
# # get updates
# https://api.telegram.org/bot1964746514:AAGmnUoclbp8R1NczhX38vt8_4Da10u4uW4/getUpdates

# # webhook Heroku
# https://api.telegram.org/bot1964746514:AAGmnUoclbp8R1NczhX38vt8_4Da10u4uW4/setWebhook?url=https://rossmann-predict-bot.herokuapp.com
        
# # send messages
# https://api.telegram.org/bot1964746514:AAGmnUoclbp8R1NczhX38vt8_4Da10u4uW4/sendMessage?chat_id=1105720401&text=Hi!

def send_message(chat_id, text):
    parse = 'HTML'
    url = 'https://api.telegram.org/bot{}/sendMessage'.format( TOKEN )
    
    message = {
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True,
        'chat_id': chat_id
    }
    
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print('Text: {}'.format(text))
    r = requests.post(url, json=message, headers=header)
    print('Status Code {}'.format(r.status_code))
    print('Chat ID: {}'.format(chat_id))

    return None

def send_photo(chat_id, photo_path, caption):
    url = 'https://api.telegram.org/bot{}/sendPhoto'.format( TOKEN )
    
    chart_img = os.path.expanduser('~/{}'.format(photo_path))
    
    message = {
        'photo': 'https://lh3.googleusercontent.com/t8jzr310rC5obgwRHRljXVYqpVt_LwPzoBoBknYxU9QH4sDPlItjYN_IGNbDIaK6d89pVC7XxGM87-QypJ9CmgHXSA=w640-h400-e365-rj-sc0x00ffffff',
        'caption': caption,
        'chat_id': chat_id
    }
    
    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    f = os.path.isfile(chart_img)
    if not f:
        print('Não salvou!, {}'.format(chart_img))
    else:
        print('Salvou, {}'.format(chart_img))

    
    r = requests.post(url, json=message, headers=header)
    print('Photo path: {}'.format(chart_img))
    print('Status Code {}\nResponse {}\nText {}'.format(r.status_code, r.reason, r.text))
    print('Chat ID: {}'.format(chat_id))
    
    return None

def load_dataset(store_id=None, full=False):
    # loading test dataset
    df_test_raw = pd.read_csv('test.csv')
    df_store_raw = pd.read_csv('store.csv')

    # merge test dataset with Store
    df_test = pd.merge(df_test_raw, df_store_raw, how='left', on='Store')
    
    if not full:
        # choose store for prediction
        df_test = df_test[df_test['Store'].isin(store_id)]

    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        # convert DataFrame to JSON
        data = json.dumps(df_test.to_dict(orient='records'))
        
    else:
        data = 'error'
    
    return data

def predict(data):
    # API Call
    url = 'https://das-rossmann-prediction.herokuapp.com/rossmann/predict'
    header = {'Content-type': 'application/json'}
    data = data

    r = requests.post(url, data=data, headers=header)
    print( 'Status Code {}'.format(r.status_code))

    d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())

    return d1

def get_graph(predicted_data, x_axis, y_axis, title, x_label, y_label, img_name):
        fig = sns.barplot(x=x_axis, y=y_axis, data=predicted_data)
        fig.set_title(title)
        fig.set_xlabel(x_label)
        fig.set_ylabel(y_label)
#         ylabels = ['{:,.0f}'.format(x) + 'K' for x in fig.get_yticks()/1000]
#         fig.set_yticklabels(ylabels)
        fig.figure.savefig(img_name)
        f = os.path.exists(img_name)
        if not f:
            print('Não salvou!')
        else:
            print('Salvou')

        return None

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']
    
    command = store_id.replace('/', '')
    command = store_id.replace(' ', '')
            
    return chat_id, command

def get_help(greeting=True):
    msg_help_g = ''
    if greeting:

        linkedin_link = 'https://linkedin.com/in/dennydaspinelli'
        github_link = 'https://github.com/daSpinelli/dsEmProd'

        msg_help_g  = '''Hello!

Welcome to Rossmann Stores Sales Prediction!
A project developd by <a href="{}">Denny de Almeida Spinelli</a>.
For full info, go to the <a href="{}">project github</a>.

Through this telegram bot you will access sales preditions of Rossmann Stores.


'''.format(linkedin_link, github_link)
        
    msg_help = msg_help_g + '''<b><u>Here are you options</u></b>

<b><i>start</i></b> : project info
<b><i>help</i></b> : available commands
<b><i>top predictions</i></b> : a bar graph with the top 5 predictions
<b><i>top sales</i></b> : a bar graph with the top sales + predictions
<b><i>n</i></b> : prediction for a single store, where n is the id of a store
<b><i>n,n,n,n</i></b> : predictions for a list of stores, where n is the id of a store

Make good use of these data! With great powers comes great responsabilities!'
   '''
    
    return msg_help

# API initialize
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        message = request.get_json()
        
        chat_id, command = parse_message(message)
        
        try:
            command = command.lower()
        except ValueError:
            command = command
        
        try:
            command = int(command)
        except ValueError:
            command = command
        
        if type(command) != int:
            command = command.split(',') if command.find(',') >= 0 else command
        
        # filtered prediction
        if (type(command) == list) | (type(command) == int):
            # reshape if there is only one store_id and convert list from string to int
            if type(command) == list:
                store_id = [int(x) for x in command]
            else:
                store_id = [command,]
                
            # loading data
            data = load_dataset(store_id)

            if data != 'error':
                
                # prediction
                d1 = predict(data)
                
                # calculation
                d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()

                for i in range(len(d2)):
                # send message
                    msg = 'Store Number {} will sell R${:,.2f} in the next 6 weeks'.format(
                        d2.loc[i, 'store'],
                        d2.loc[i, 'prediction']
                    )
                    send_message( chat_id, msg )
                    print('return message: {}'.format(msg))
                    #return Response('Ok', status=200)
                
            else:
                send_message(chat_id, 'Store ID do not exist')
                #return Response('Ok', status=200)

        # start
        elif (command == 'start'):
            msg_help = get_help()
            send_message(chat_id, msg_help)
            #return Response('Ok', status=200)
            
        # help
        elif (command == 'help'):
            msg_help = get_help(False)
            send_message(chat_id, msg_help)
            #return Response('Ok', status=200)

        # top prediction
        elif command == 'toppredictions':
            print('top predictions')            
            
            # loading data
            data = load_dataset(full=True)
            
            # prediction
            d1 = predict(data)
            
            d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()
            
            d3 = d2.nlargest(5, 'prediction')
            
            # graph definitions
            x_ax = 'store'
            y_ax = 'prediction'
            graph_title = 'Rossmann Sales Store Highest Predictions'
            x_lbl = 'Store ID'
            y_lbl = 'Predicion for next 6 weeks (Unit: K)'
            image_path = 'top5_prediction.png'
            
            get_graph(
                d3,
                x_axis=x_ax,
                y_axis=y_ax,
                title=graph_title,
                x_label=x_lbl,
                y_label=y_lbl,
                img_name=image_path
            )
                        
            send_photo(chat_id, image_path, graph_title)
            #return Response('Ok', status=200)

        # top sales
        elif command == 'topsales':
            print('top sales')
            send_message(chat_id, 'top 5 sales')
            #return Response('Ok', status=200)            
            
        else:
            msg_help = get_help(greeting = False)
            send_message(chat_id, 'This is an invalid command!')
            send_message(chat_id, msg_help)
            #return Response('Ok', status=200)
        
        send_message(chat_id, 'Done!')
        return Response('Ok', status=200)
        
    else:
        return '<h1> Rossmann Telegram BOT</h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
