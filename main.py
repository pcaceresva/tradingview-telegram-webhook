from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔹 Token del bot de Telegram (variable de entorno en Render)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# 🔹 Diccionario: palabra clave en alerta → chat_id del canal
CHAT_IDS = {
    "MACD40-1": "-1002579121705",   # Canal para indicador MACD40-1
    "EMA+MACD": "-1002411599382",   # Canal para indicador EMA+MACD
    "Supertrend": "-1002813953373"  # Canal para indicador Supertrend
}

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Mensaje recibido desde TradingView (puede ser JSON o texto plano)
        raw_message = request.data.decode("utf-8").strip()

        print(f"[TradingView] Mensaje crudo: {raw_message}")

        # Buscar a qué canal enviar según palabra clave
        target_chat_id = None
        for key, chat_id in CHAT_IDS.items():
            if key in raw_message:
                target_chat_id = chat_id
                break

        # Si no encuentra canal, loguea y no envía
        if not target_chat_id:
            print("[Error] No se encontró un canal para este mensaje.")
            return "no channel", 400

        # Enviar mensaje a Telegram
        payload = {
            "chat_id": target_chat_id,
            "text": raw_message,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")
        return "error", 500

    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
