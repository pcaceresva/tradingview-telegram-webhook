from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔹 Usa el token de Telegram desde variables de entorno en Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 1️⃣ Recibir texto enviado por TradingView
        message_text = request.data.decode("utf-8").strip()

        # 2️⃣ Extraer chat_id del mensaje si viene incluido (opcional)
        chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Valor por defecto
        if message_text.startswith("chat_id="):
            first_line, rest = message_text.split("\n", 1)
            chat_id = first_line.replace("chat_id=", "").strip()
            message_text = rest.strip()

        # 3️⃣ Construir payload para Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"  # o "HTML" si prefieres
        }

        # 4️⃣ Enviar a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # 5️⃣ Logs
        print(f"[TradingView] Mensaje recibido: {message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

        return "ok", 200

    except Exception as e:
        print(f"[Error] {e}")
        return "error", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
