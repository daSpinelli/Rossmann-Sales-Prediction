import pandas as pd
import json
import requests
import os
import seaborn as sns
import telegram
import matplotlib.ticker as mticker

from flask import Flask, request, Response
from credentials import credentials

# constants
cred = credentials()
TOKEN = cred.TOKEN

def send_msg(chat_id, text, _bot, parse='HTML'):
    _bot.send_message(chat_id, text, parse_mode=parse)

    return None

def send_img(chat_id, img_path, caption, _bot):
    _bot.send_photo(chat_id, open(img_path, 'rb'), caption=caption)
    print('Sending the file {}'.format(img_path))
    
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

def draw_chart(predicted_data, x_axis, y_axis, title, x_label, y_label, img_name, divisor, tick_format='{:,.0f}'):
        
        fig = sns.barplot(x=x_axis, y=y_axis, data=predicted_data)
        fig.set_title(title)
        fig.set_xlabel(x_label)
        fig.set_ylabel(y_label)
        
        fig.yaxis.set_major_locator(mticker.MaxNLocator(8))
        yticks = fig.get_yticks()
        fig.yaxis.set_major_locator(mticker.FixedLocator(yticks))
        
        
        ylabels = [tick_format.format(x) for x in yticks / divisor]
        fig.set_yticklabels(ylabels)
        
        fig.figure.savefig(img_name)
        
        print('Saving the file {}'.format(img_name))
        print('='*20)
        print('Params:\nx_axis: {}\ny_axis: {}\ntitle: {}\nx_label: {}\ny_label {}\nshape: {}'.format(x_axis, y_axis, title, x_label, y_label, predicted_data.shape))
        print('='*20)
        
        for d in predicted_data.values:
            print(d[0])
        
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
<b><i>n</i></b> : prediction for a single store, where n is the id of a store
<b><i>n,n,n,n</i></b> : predictions for a list of stores, where n is the id of a store

Make good use of these data! With great powers comes great responsabilities!'
   '''
    
    return msg_help

bot = telegram.Bot(token=TOKEN)

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
        print('Comando: {}'.format(command))
        # filtered prediction
        if (type(command) == list) | (type(command) == int):
            
            # reshape if there is only one store_id and convert list from string to int
            if type(command) == list:
                
                store_id = [int(x) for x in command]
                
            else:
                
                store_id = [command,]
            
            send_msg(chat_id, 'Calculating. Please wait...', bot)
            
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
                    send_msg(chat_id, msg, bot)
                
            else:
                
                send_msg(chat_id, 'Store ID do not exist', bot)

        # start
        elif (command == 'start'):
            
            msg_help = get_help()
            send_msg(chat_id, msg_help, bot)
            
        # help
        elif (command == 'help'):
            
            msg_help = get_help(False)
            send_msg(chat_id, msg_help, bot)

        # top prediction
        elif command == 'toppredictions':     
            
            send_msg(chat_id, 'Calculating. Please wait...', bot)
            
            # loading data
            data = load_dataset(full=True)
            
            # prediction
            d1 = predict(data)
            
            d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()
            
            d3 = d2.nlargest(5, 'prediction')
            
            # chart definitions
            x_ax = 'store'
            y_ax = 'prediction'
            chart_title = 'Rossmann Store highest predictions'
            x_lbl = 'Store ID'
            y_lbl = 'Prediction for next 6 weeks (Unit: K)'
            image_path = './top5_prediction.png'
            div=1000
            t_format='{:,.0f}K'
            
            draw_chart(
                d3,
                x_axis=x_ax,
                y_axis=y_ax,
                title=chart_title,
                x_label=x_lbl,
                y_label=y_lbl,
                img_name=image_path,
                divisor=div,
                tick_format=t_format
            )
                        
            send_img(chat_id, image_path, chart_title, bot)

        # top sales
#         elif command == 'topsales':
            
#             send_msg(chat_id, 'Calculating. Please wait...', bot)
            
#             # loading data
#             data = load_dataset(full=True)
            
#             # prediction
#             d1 = predict(data)
            
#             d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()
            
#             # get sales for the predicted ones
#             df_sales_raw = pd.read_csv('train.csv')          
#             df_sales_raw.columns = [col.lower() for col in df_sales_raw.columns]
#             store_predicted = d2['store'].unique()
#             df_sales = df_sales_raw.loc[df_sales_raw['store'].isin(store_predicted), ['store', 'sales']].groupby('store').sum().reset_index()

#             d3 = pd.merge(d2, df_sales, on='store', how='left')
#             d3['total'] = d3['prediction'] + d3['sales']
            
#             d3 = d3.nlargest(5, 'total')
            
#             # chart definitions
#             x_ax = 'store'
#             y_ax = 'total'
#             chart_title = 'Rossmann Store highest sales + predictions'
#             x_lbl = 'Store ID'
#             y_lbl = 'Total Sales + Prediction (Unit: K)'
#             image_path = './top5_sales.png'
#             div=1000000
#             t_format='{:,.0f}mi'
            
#             draw_chart(
#                 d3,
#                 x_axis=x_ax,
#                 y_axis=y_ax,
#                 title=chart_title,
#                 x_label=x_lbl,
#                 y_label=y_lbl,
#                 img_name=image_path,
#                 divisor=div,
#                 tick_format=t_format
#             )
                        
#             send_img(chat_id, image_path, chart_title, bot)
            
        else:
            
            msg_help = get_help(greeting = False)
            send_msg(chat_id, 'This is an invalid command!', bot)
            send_msg(chat_id, msg_help, bot)
        
        send_msg(chat_id, 'Done!', bot)
        return Response('Ok', status=200)
        
    else:
        
        return '<h1> Rossmann Telegram BOT</h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
