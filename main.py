# main.py
import os
import logging
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Optional auth token (set as env var AUTH_TOKEN on the host or Render)
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")  # e.g. export AUTH_TOKEN="mysupersecret"

def check_auth(req):
    if not AUTH_TOKEN:
        return True
    # Allow either header X-Auth-Token or query param ?token=...
    header = req.headers.get("X-Auth-Token")
    qtoken = req.args.get("token")
    return header == AUTH_TOKEN or qtoken == AUTH_TOKEN

@app.route("/handshake", methods=["GET"])
def handshake():
    if not check_auth(request):
        return ("Forbidden", 403)
    return "OK", 200

@app.route("/log", methods=["POST"])
def receive_log():
    if not check_auth(request):
        return ("Forbidden", 403)

    # Try to parse JSON payload
    data = None
    try:
        data = request.get_json(silent=True)
    except Exception as e:
        app.logger.warning("Failed to parse JSON: %s", e)

    # Accept raw body if JSON missing
    if data is None:
        try:
            raw = request.get_data(as_text=True)
            data = {"raw": raw}
        except Exception:
            data = {"raw": "<unreadable body>"}

    # Print prettily to stdout/log (Render will expose logs)
    app.logger.info("---- ROBLOX LOG ----")
    app.logger.info("%s", data)
    app.logger.info("--------------------")

    # Optionally, you could store logs to a file or DB here
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Local development server (use PORT env var if provided)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
