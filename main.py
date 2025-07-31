from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Token desde Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 🔹 Parsear el JSON que manda TradingView
        data = request.get_json(force=True)

        if not data or "message" not in data or "chat_id" not in data:
            return "Bad request", 400

        message_text = data["message"]
        chat_id = data["chat_id"]

        # 🔹 Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # Logs
        print(f"[TradingView] JSON recibido: {data}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")
        return "Internal server error", 500

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
