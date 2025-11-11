from flask import Flask, request

app = Flask(__name__)

@app.route("/handshake", methods=["GET"])
def handshake():
    return "OK", 200

@app.route("/log", methods=["POST"])
def log():
    data = request.data.decode("utf-8")
    print("LOG:", data)
    return "Received", 200

@app.route("/", methods=["GET"])
def home():
    return "RemoteOutput is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
