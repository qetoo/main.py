from flask import Flask, request, Response, jsonify
import queue
import threading
import time

app = Flask(__name__)
message_queue = queue.Queue()

@app.route("/handshake", methods=["GET"])
def handshake():
    return "OK", 200

@app.route("/send", methods=["POST"])
def send():
    """Receives log data from Roblox plugin and stores it"""
    data = request.get_json(force=True)
    message_queue.put(data)
    return "OK", 200

@app.route("/stream", methods=["GET"])
def stream():
    """Streams logs to client (EXE) in real-time"""
    def event_stream():
        while True:
            try:
                data = message_queue.get(timeout=10)
                yield f"data: {data}\n\n"
            except queue.Empty:
                # keep the connection alive
                yield ": keep-alive\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/events", methods=["GET"])
def events():
    """Fallback for clients that don't support SSE"""
    events = []
    while not message_queue.empty():
        events.append(message_queue.get())
    return jsonify(events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
