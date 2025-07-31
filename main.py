from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Recibir el mensaje de TradingView como texto plano
        message_text = request.data.decode("utf-8").strip()

        # Extraer chat_id si viene en el mensaje, si no usar uno por defecto
        chat_id = "-1001234567890"  # Cambia por tu canal de respaldo
        if '"chat_id":' in message_text:
            try:
                import re
                match = re.search(r'"chat_id"\s*:\s*"([^"]+)"', message_text)
                if match:
                    chat_id = match.group(1)
            except:
                pass

        # Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[TradingView] Mensaje recibido:\n{message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
