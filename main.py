from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        message_text = request.data.decode("utf-8").strip()

        try:
            data = json.loads(message_text)
            chat_id = data.get("chat_id")
            text = data.get("message", "")
        except:
            chat_id = None
            text = message_text

        if not chat_id:
            return "No chat_id provided", 400

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[TradingView] Mensaje recibido: {message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

