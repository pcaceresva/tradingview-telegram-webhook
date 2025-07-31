from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Token de Telegram desde Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 1️⃣ Recibir y parsear JSON
        data = json.loads(request.data.decode("utf-8"))

        # 2️⃣ Extraer message y chat_id enviados por TradingView
        message_text = data.get("message", "")
        chat_id = data.get("chat_id", "")

        # 3️⃣ Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # 4️⃣ Logs
        print(f"[TradingView] Mensaje recibido: {message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
