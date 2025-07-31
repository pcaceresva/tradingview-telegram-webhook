from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Token de Telegram desde variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_data = request.data.decode("utf-8").strip()
        print(f"[DEBUG] Datos recibidos de TradingView: {raw_data}")

        chat_id = None
        message_text = None

        # Intentar interpretar como JSON
        try:
            data = json.loads(raw_data)
            message_text = data.get("message", "").strip()
            chat_id = data.get("chat_id", "").strip()
            print("[DEBUG] Interpretado como JSON")
        except json.JSONDecodeError:
            # Si no es JSON, tratarlo como texto plano
            message_text = raw_data
            print("[DEBUG] Interpretado como texto plano (no JSON)")

        # Validar
        if not message_text:
            print("[ERROR] No se encontró texto para enviar a Telegram")
            return "ok", 200
        if not chat_id:
            print("[ERROR] No se encontró chat_id, no se puede enviar")
            return "ok", 200

        # Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # Logs
        print(f"[DEBUG] Payload enviado a Telegram: {payload}")
        print(f"[DEBUG] Respuesta Telegram: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[ERROR] {e}")

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
