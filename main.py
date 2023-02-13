from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

user_id = 'Uf78f7decc8f4f1d618aa935553c16f9c'


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user id when reply
    sender_id = event.source.user_id
    print("user_id =", sender_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='您的user ID為: '+sender_id))


@app.route("/push_function/<string:push_text_str>")
def push_message(push_text_str):
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))

    return 'OK'


@app.route("/push_to_user/<string:target_id>/<string:push_text_str>")
def push_message_to_user(target_id, push_text_str):
    line_bot_api.push_message(target_id, TextSendMessage(push_text_str))

    return 'OK'


@app.route('/')
def index():
    return 'Hello World'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
