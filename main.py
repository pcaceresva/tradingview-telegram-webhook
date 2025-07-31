from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Token de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Mapeo de indicadores → canales
INDICATOR_CHAT_IDS = {
    "MACD40": os.getenv("TELEGRAM_CHAT_ID_MACD"),
    "EMA+MACD40": os.getenv("TELEGRAM_CHAT_ID_CRUCEEMA"),
    "SUPERTREND40": os.getenv("TELEGRAM_CHAT_ID_SUPERTREND")
}

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Recibir mensaje de TradingView
        raw_data = request.data.decode("utf-8").strip()
        print(f"[TradingView] Mensaje recibido: {raw_data}")

        # Esperamos formato: INDICADOR|Mensaje
        if "|" in raw_data:
            indicator_code, message_text = raw_data.split("|", 1)
            chat_id = INDICATOR_CHAT_IDS.get(indicator_code)
        else:
            print("[Error] Formato no válido. Falta el identificador del indicador.")
            return "Formato inválido", 400

        # Verificar que el chat_id exista
        if not chat_id:
            print(f"[Error] No se encontró chat_id para el indicador {indicator_code}")
            return "No chat_id", 400

        # Construir payload para Telegram
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }

        # Enviar a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
