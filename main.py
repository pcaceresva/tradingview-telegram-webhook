from flask import Flask, request
import requests
import os
from threading import Thread

app = Flask(__name__)

# 🔹 Token del bot de Telegram (variable de entorno en Render)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# 🔹 Canales por indicador
CHAT_IDS = {
    "MACD40-1": "-1002579121705",
    "MACD40-2": "-1002579121705",
    "CRUCEEMA40-1": "-1002411599382",
    "CRUCEEMA40-2": "-1002411599382",
    "CRUCEEMA40-3": "-1002411599382",
    "SUPERTRENDRSI40-1": "-1002813953373",
    "SUPERTRENDRSI40-2": "-1002813953373",
    "SUPERTRENDRSI40-3": "-1002813953373",
    "TRENDBREAKS": "-1002956776649",
    "BB+RSI-1": "-1003613150409",
    "BB+RSI-2": "-1003613150409",
    "BB+RSI-3": "-1003613150409"
}

# 🔹 Canal fijo para SUPERTRENDEMA (prioridad absoluta)
SUPERTRENDEMA_CHAT_ID = "-1002813953373"


def send_to_telegram(raw_message: str):
    try:
        target_chat_id = None

        # 1️⃣ PRIORIDAD: SUPERTRENDEMA siempre va a su canal
        if "SUPERTRENDEMA" in raw_message:
            target_chat_id = SUPERTRENDEMA_CHAT_ID
        else:
            # 2️⃣ Resto de indicadores (lógica original)
            for key, chat_id in CHAT_IDS.items():
                if key in raw_message:
                    target_chat_id = chat_id
                    break

        # 3️⃣ Si no se asigna canal, no se pierde la alerta
        if not target_chat_id:
            print("[WARN] Mensaje sin canal asignado, se ignora:")
            print(raw_message)
            return

        payload = {
            "chat_id": target_chat_id,
            "text": raw_message  # Texto EXACTO desde TradingView
        }

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload, timeout=10)

        print(f"[Telegram] {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Telegram ERROR] {e}")


@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_message = request.data.decode("utf-8", errors="ignore").strip()
        print(f"[TradingView] {raw_message}")

        # Responder inmediato a TradingView
        send_to_telegram(raw_message)
        return "ok", 200

    except Exception as e:
        print(f"[Webhook ERROR] {e}")
        return "error", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

