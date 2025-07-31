from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    raw_data = request.data.decode("utf-8").strip()
    print("========== NUEVA ALERTA ==========")
    print(raw_data)
    print("===================================")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
