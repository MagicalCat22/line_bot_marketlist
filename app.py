import pygsheets #googl sheet 套件
from flask import Flask, request
# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
# 載入 json 標準函式庫，處理回傳的資料格式
import requests, json, time
import re
app = Flask(__name__)

gc = pygsheets.authorize(service_account_file='credentials.json')
survey_url = 'https://docs.google.com/spreadsheets/d/14BAuBkfQLYq5Sl4I_Bbfyi-FQMloJx6Ie6mINIWvKkM/'
sh = gc.open_by_url(survey_url)
sheet = sh.worksheet_by_title('marketlist')
line_bot_api = LineBotApi('Wg40vOOYOFM/eXhmrkZdaPorCLe6ttldlysmZ3GUsivHoZApZLCExGbxJZBTa0bd+rKGkzIi0nfKrV2rtAAd/1/7PHGSPXI8VTsIKrtvcZCcm1ZxzewovA+vzeHWyGIDXGbspuynFPWsCrovpQenpgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('019098f7a352d178b5317bca91292452')
count = 0

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        reply_token = json_data['events'][0]['replyToken']      # 取得 reply token
        msg_type = json_data['events'][0]['message']['type']    # 取得 message 的類型
        msg = json_data['events'][0]['message']['text'] #取得使用者文字
        if msg_type == 'text':
            if msg == '!list'or msg == '！list' :
                line_bot_api.reply_message(reply_token,TextSendMessage('今日購買清單:\n'+read()))
            elif msg == '!clear' or msg == '！clear':
                clear()
                line_bot_api.reply_message(reply_token,TextSendMessage('已將表單清除'))  # 回傳訊息
            elif msg[0] == '!'or msg[0]=='！':
                update(msg)
                line_bot_api.reply_message(reply_token,TextSendMessage('已將:\n'+msg[1:]+'\n加入清單'))  # 回傳訊息
    except:
        print('error')
    return 'OK'
def update(item):
    item = item[1:]
    item = re.split(r'[\s\n]',item)
    item = item.strip(' ')
    count = len(item)
    i=1
    j=0
    while count!=0:   
        if sheet.get_value('A'+str(i)) =='':
            sheet.update_value('A'+str(i),item[j])
            count-=1
            j+=1
        i+=1
        
def clear():
    sheet.clear('A')
def read():
    i=1
    item = ''
    if sheet.get_value('A1')=='':
        return '今日還未新增品項喔'
    else:
        while(sheet.get_value('A'+str(i+1))!=''):
            item += sheet.get_value('A'+str(i))
            item += '\n'
            i+=1
        item += sheet.get_value('A'+str(i))
        return item
    # item = ''
    # for i in range(sheet.getLastRow()+1):
    #     item += sheet.get_value('A'+str(i+1))
    #     item += '\n'
    # item += sheet.get_value('A'+str(sheet.getLastRow()))
    # return item 
    
