from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# 🔹 Token fijo desde variables de entorno
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_data = request.data.decode("utf-8").strip()
        print(f"[Render] Datos crudos recibidos: {raw_data}")

        chat_id = None
        message_text = None

        # 📌 Intentar parsear como JSON (TradingView enviando JSON)
        try:
            data_json = json.loads(raw_data)
            message_text = data_json.get("message")
            chat_id = data_json.get("chat_id")
            print("[Render] Interpretado como JSON")
        except Exception:
            # 📌 Si falla, interpretamos como texto plano
            message_text = raw_data
            print("[Render] Interpretado como TEXTO PLANO")

        # 🔹 Validaciones
        if not message_text:
            print("[Error] No se encontró mensaje para enviar a Telegram.")
            return "error", 400
        if not chat_id:
            print("[Error] No se encontró chat_id en la alerta.")
            return "error", 400

        # 🔹 Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[Telegram] Status: {resp.status_code} - {resp.text}")
        return "ok", 200

    except Exception as e:
        print(f"[Error General] {e}")
        return "error", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
