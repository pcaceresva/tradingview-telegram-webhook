from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Leer datos crudos que envía TradingView
        raw_data = request.data.decode("utf-8").strip()
        print(f"[Render] Datos crudos recibidos: {raw_data}")

        # Intentar parsear como JSON
        try:
            data_json = json.loads(raw_data)
            message_text = data_json.get("message", raw_data)
            chat_id = data_json.get("chat_id", None)
            print("[Render] Interpretado como JSON correctamente")
        except json.JSONDecodeError:
            # No es JSON → usar texto plano y chat fijo
            message_text = raw_data
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            print("[Render] Interpretado como TEXTO plano")

        # Verificar que tengamos chat_id
        if not chat_id:
            print("[Error] No se recibió chat_id ni está configurado en variable de entorno")
            return "missing chat_id", 400

        # Enviar mensaje a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)
        print(f"[Telegram] Status: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")
        return "error", 500

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
