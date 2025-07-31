from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔹 Usar variables de entorno que ya configuraste en Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 1️⃣ Recibir mensaje crudo enviado por TradingView
        message_text = request.data.decode("utf-8").strip()

        # 2️⃣ Construir payload para Telegram
        payload = {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "Markdown"  # O "HTML" si usas etiquetas HTML
        }

        # 3️⃣ Enviar mensaje a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # 4️⃣ Log para depuración
        print(f"[TradingView] Mensaje recibido: {message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    # Render expone puerto en variable PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

