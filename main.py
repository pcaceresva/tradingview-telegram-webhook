from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_DEFAULT = os.getenv("TELEGRAM_CHAT_ID")  # Canal por defecto (fallback)

@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_text = request.data.decode("utf-8").strip()

        # Intentar interpretar como JSON
        try:
            data = json.loads(raw_text)
            message_text = data.get("message", "")
            chat_id = data.get("chat_id", CHAT_ID_DEFAULT)
        except json.JSONDecodeError:
            # Si no es JSON válido, lo tratamos como texto plano
            message_text = raw_text
            chat_id = CHAT_ID_DEFAULT

        # Construir payload para Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"  # O "HTML" si prefieres
        }

        # Enviar mensaje a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # Logs
        print(f"[TradingView] Recibido: {raw_text}")
        print(f"[Telegram] Enviado a chat_id={chat_id} -> {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
