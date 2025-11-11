import os
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")  # optional

def check_auth(req):
    if not AUTH_TOKEN:
        return True
    return req.headers.get("X-Auth-Token") == AUTH_TOKEN or req.args.get("token") == AUTH_TOKEN

@app.route("/", methods=["GET"])
def home():
    return "RemoteOutput is running!", 200

@app.route("/handshake", methods=["GET"])
def handshake():
    if not check_auth(request):
        return "Forbidden", 403
    return "OK", 200

@app.route("/log", methods=["POST"])
def receive_log():
    if not check_auth(request):
        return "Forbidden", 403

    data = request.get_json(silent=True)
    if data is None:
        data = {"raw": request.get_data(as_text=True)}

    app.logger.info("---- ROBLOX LOG ----")
    app.logger.info("%s", data)
    app.logger.info("--------------------")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
