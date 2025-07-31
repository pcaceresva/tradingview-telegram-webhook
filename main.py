@app.route("/", methods=["POST"])
def webhook():
    try:
        raw_data = request.data.decode("utf-8")
        print(f"[DEBUG] Datos crudos recibidos: {raw_data}")  # 👈 Esto imprimirá exactamente lo que manda TV

        data = json.loads(raw_data)
        message_text = data.get("message", "")
        chat_id = data.get("chat_id", "")

        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, json=payload)

        print(f"[TradingView] Mensaje recibido: {message_text}")
        print(f"[Telegram] Respuesta: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"[Error] {e}")

    return "ok"
