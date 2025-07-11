import os
from flask import Flask, request
import requests

app = Flask(__name__)

# 🔐 Obtener TOKEN y CHAT_ID desde variables de entorno
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

@app.route('/', methods=['POST'])
def alerta():
    data = request.json
    message = data.get("message", "Sin mensaje recibido de TradingView")

    # ✅ Construir la URL para enviar mensaje a Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    # ✅ Enviar mensaje
    response = requests.post(url, json=payload)

    # Log para debug si lo necesitas
    print("Mensaje recibido:", message)
    print("Respuesta de Telegram:", response.text)

    return 'ok'

if __name__ == '__main__':
    # Escuchar en todos los puertos para Render
    app.run(host='0.0.0.0', port=5000)
