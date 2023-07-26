import os
import openai
import json

from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

# 語音轉文字相關套件
import speech_recognition as sr
# 語音轉檔相關套件
from pydub import AudioSegment

app = Flask(__name__)
# @app.route('/.well-known/pki-validation/721B0B45EEA984B83C2449B110064E0A.txt')
# def show_result():
#     try:
#         # 讀取result.txt文件的內容
#         with open('721B0B45EEA984B83C2449B110064E0A.txt', 'r') as file:
#             content = file.read()
#         # 將文件內容返回給使用者
#         return content
#     except FileNotFoundError:
#         return "File not found"
@app.route("/callback", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    # print(body)
    json_data = json.loads(body)
    # print(json_data)
    
    try:
    #line bot Channel access token
        line_bot_api = LineBotApi('35409spqhTAQH58C6hlk/mnzIKtDCPGvVGcSVmxC9OQvRWR6C8BZXXH4jJWSeeS4+ONg3zrslQWzzkWxgALtvkzDw5LZMvMz3IVRZIW+RiZQ95YOqzdOmM+ZRT+mwP3np6k2Nw1Li8tmTIkpiMIpqAdB04t89/1O/w1cDnyilFU=')
    #       line bot Channel secret(要改成自己的)
        handler = WebhookHandler('9028c1918534ce7b669b002fcb3d33d1')
        openai.api_key = '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'
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        
    #       觸發事件為加入群組
        if json_data['events'][0]['type'] == 'join':
            GroupID = json_data['events'][0]['source']['groupId']
            text_message = TextSendMessage(text="hello")
            line_bot_api.push_message(GroupID,text_message)
        
    #       觸發事件為收到訊息
        elif json_data['events'][0]['type'] == 'message':
    #       輸入內容型態
            Type = json_data['events'][0]['message']['type']
            tk = json_data['events'][0]['replyToken']
            # jsonfile = open("mentor_output.json")
            # a = json.load(jsonfile)
            # b = json.dumps(a[0])    
            reply_msg = ''

    #       處理語音輸入
            # if Type == "audio":

            #     audio_content = line_bot_api.get_message_content(json_data['events'][0]['message']['id'])
            #     path='sound.m4a'
            #     with open(path, 'wb') as fd:
            #         for chunk in audio_content.iter_content():
            #             fd.write(chunk)

            #     #進行語音轉文字處理
            #     r = sr.Recognizer()
            #     #輸入自己的ffmpeg.exe路徑(ffmpeg要額外載，只有windows可使用)
            #     AudioSegment.converter = 'ffmpeg-6.0-essentials_build/bin/ffmpeg.exe'
            #     sound = AudioSegment.from_file_using_temporary_files(path)
            #     path = os.path.splitext(path)[0]+'.wav'
            #     sound.export(path, format="wav")
            #     with sr.AudioFile(path) as source:
            #         audio = r.record(source)

            #     #recognize_google表示使用google api
            #     text = r.recognize_google(audio,language='zh-TW')
            #     print(text)
            #     reply_msg=text
            # else:
           
            msg = json_data['events'][0]['message']['text']

            # 取出文字的前五個字元，轉換成小寫
            ai_msg = msg[:6].lower()

            # 取出文字的前五個字元是 hi ai:
            if ai_msg == 'hi ai:':
                # 將第六個字元之後的訊息發送給 OpenAI
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {"role":"system", "content":b},
                        {"role":"user","content":"以上面知識回答問題:"+msg[6:]}
                    ],
                    max_tokens=256,
                    # temperature=0.5,
                )
                # 接收到回覆訊息後，移除換行符號
                # print(response)
                reply_msg = response["choices"][0]['message']["content"].strip()
            else:
                reply_msg = msg

            text_message = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(tk,text_message)
    except:
        print('error')
    return 'OK'

if __name__ == "__main__":
    # app.run(host="0.0.0.0",port="80",ssl_context=('certificate.crt', 'private.key'))
    app.run()


    # certbot certonly --email <vincent255004@gmail.com> -d <enablingport.sytes.net> --agree-tos --manual