from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
from threading import Lock

app = Flask(__name__)
CORS(app)

DATA_FILE = Path("data.json")
lock = Lock()

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return {"services": {}}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

@app.route("/", methods=["GET", "PUT"])
def main():
    with lock:
        if request.method == "GET":
            return jsonify(load_data())

        data = request.get_json(force=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON"}), 400
        save_data(data)
        return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)