from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# 🔹 Usar variables de entorno de Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_ENV = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 1️⃣ Recibir mensaje crudo enviado por TradingView
        raw_data = request.data.decode("utf-8").strip()
        print("===== [TradingView] Datos crudos recibidos =====")
        print(raw_data)

        # 2️⃣ Intentar parsear como JSON (por si TradingView envía JSON)
        message_text = None
        chat_id = CHAT_ID_ENV

        try:
            data_json = json.loads(raw_data)
            message_text = data_json.get("message", "")
            if "chat_id" in data_json:
                chat_id = data_json.get("chat_id")
        except json.JSONDecodeError:
            # Si no es JSON, asumir que es texto plano
            message_text = raw_data

        # 3️⃣ Mostrar token y chat_id usados
        print("TOKEN usado:", TOKEN)
        print("CHAT_ID usado:", chat_id)

        # 4️⃣ Construir payload para Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }

        # 5️⃣ Enviar a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        # 6️⃣ Mostrar respuesta de Telegram
        print("===== [Telegram] Respuesta =====")
        print(resp.status_code, resp.text)

    except Exception as e:
        print("[Error]", e)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
