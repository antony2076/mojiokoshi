import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('91F97TEl4XRd8yG8UJ5QjYfyBTplKVO6OAbdW9fAXbblrvjb/8LMHJ94xBt7MXTyovlzlW9aTzFy8W/PkvlzajWQG1fbRxCdKRTzF+e5F/qbkMUpbkgq7ReSl40ZWR1VNR8i5/cEyk70AJIkUk/OlwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('94e8ecf70fc670b4680295658568d45e')


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
    port = os.environ.get('PORT', 3333)
    app.run(
        host='0.0.0.0',
        port=port,
    )
