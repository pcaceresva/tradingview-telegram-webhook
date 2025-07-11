from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/', methods=['POST'])
def alerta():
    # Intenta leer JSON, si no hay, usa texto plano
    data = request.get_json(silent=True)
    if data and "message" in data:
        message = data["message"]
    else:
        message = request.data.decode("utf-8") or "Mensaje vacío"

    # Enviar mensaje a Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)

    print("Mensaje recibido:", message)
    print("Respuesta de Telegram:", response.text)

    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
