from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Usar el token de Telegram desde variable de entorno en Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Recibir el JSON enviado por TradingView
        data = request.get_data(as_text=True).strip()
        print(f"[TradingView] Mensaje recibido crudo: {data}")

        # Intentar parsear JSON
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            return "Invalid JSON", 400

        # Validar que tenga los campos correctos
        if "message" not in payload or "chat_id" not in payload:
            return "Missing fields", 400

        chat_id = payload["chat_id"]
        message = payload["message"]

        # Preparar payload para Telegram
        tg_payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        # Enviar mensaje a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=tg_payload)

        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

        return "ok", 200

    except Exception as e:
        print(f"[Error] {e}")
        return "error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
