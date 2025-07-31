from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Usamos solo el token fijo del bot (este sí sigue en Render)
TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Recibir mensaje crudo de TradingView
        raw_message = request.data.decode("utf-8").strip()
        print(f"[TradingView] Mensaje recibido: {raw_message}")

        # Intentar interpretar como JSON
        try:
            data = json.loads(raw_message)
            chat_id = data.get("chat_id")
            text = data.get("message", "")
        except json.JSONDecodeError:
            # Si no es JSON, no podemos saber el chat_id → error
            return "Formato inválido: se esperaba JSON con 'message' y 'chat_id'", 400

        # Validar que tengamos chat_id
        if not chat_id:
            return "Error: No se recibió 'chat_id' en el mensaje", 400

        # Enviar a Telegram
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"  # Cambia a "HTML" si usas etiquetas HTML
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
