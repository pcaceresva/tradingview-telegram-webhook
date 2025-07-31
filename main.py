from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Chat IDs para cada tipo de indicador
CHAT_IDS = {
    "MACD40-1": "-1002579121705",
    "EMA+MACD": "-100YYYYYYYYYY",
    "OtroIndicador": "-100ZZZZZZZZZZ"
}

@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_message = request.data.decode("utf-8").strip()

        # Determinar a qué canal enviar
        target_chat_id = None
        for key, chat_id in CHAT_IDS.items():
            if key in raw_message:
                target_chat_id = chat_id
                break

        if not target_chat_id:
            target_chat_id = os.getenv("TELEGRAM_CHAT_ID_DEFAULT", "")

        # Enviar a Telegram
        payload = {
            "chat_id": target_chat_id,
            "text": raw_message
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[TradingView] Recibido: {raw_message}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"
