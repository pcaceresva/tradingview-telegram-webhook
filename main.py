from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Token del bot
# Eliminamos CHAT_ID fijo para permitir IDs dinámicos desde TV

@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_data = request.data.decode("utf-8").strip()
        print(f"\n[Render] Datos crudos recibidos: {raw_data}")

        # Intentar parsear como JSON
        try:
            data = json.loads(raw_data)
            print("[Render] Interpretado como JSON correctamente")
            message_text = data.get("message", "")
            chat_id = data.get("chat_id", "")

        except json.JSONDecodeError:
            print("[Render] Interpretado como TEXTO PLANO")
            message_text = raw_data
            chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Si no envían chat_id, usa el fijo

        # Validar datos
        if not chat_id:
            print("[Error] No se encontró chat_id en la alerta.")
            return "missing chat_id", 400
        if not message_text:
            print("[Error] No se encontró message en la alerta.")
            return "missing message", 400

        # Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # Mostrar respuesta exacta de Telegram
        print(f"[Telegram] Status: {resp.status_code} - {resp.text}")

        return "ok", 200

    except Exception as e:
        print(f"[Error] {e}")
        return "error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
