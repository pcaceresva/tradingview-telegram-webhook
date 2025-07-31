from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 🔹 Capturar datos crudos
        raw_data = request.data.decode("utf-8")
        print(f"[Render] Datos crudos recibidos: {raw_data}")

        # 🔹 Intentar parsear como JSON
        try:
            data = json.loads(raw_data)
            message_text = data.get("message", "")
            chat_id = data.get("chat_id", "")
            print("[Render] Interpretado como JSON correctamente")
        except json.JSONDecodeError:
            message_text = raw_data
            chat_id = ""
            print("[Render] Interpretado como TEXTO plano")

        # 🔹 Usar chat_id del JSON o el de variable de entorno
        if not chat_id:
            chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

        # 🔹 Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[Telegram] Status: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
