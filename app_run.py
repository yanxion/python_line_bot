# -*- coding:utf-8 -*-
import json
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pyquery
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('os.environ.get("Channel_Access_Token", None)')
handler = WebhookHandler('os.environ.get("Channel_Secret", None)')

@app.route("/")
def index():
    res = requests.get('http://httpbin.org/ip')
    html_script = "<h1> Heroku app success !! </h1>"
    html_script += res.text
    return html_script

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()