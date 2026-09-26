import os
import random
import time
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

# Sample IP addresses and endpoints for simulation
IP_POOL = ["192.168.1.45", "10.0.0.12", "172.16.0.88", "192.168.1.102", "203.0.113.195"]
ENDPOINTS = ["/login", "/admin", "/api/v1/data", "/dashboard", "/config.json"]
STATUS_CODES = [200, 200, 200, 401, 403, 404, 500]

def generate_mock_logs(count=20):
    logs = []
    now = int(time.time())
    for i in range(count):
        ip = random.choice(IP_POOL)
        status = random.choice(STATUS_CODES)
        endpoint = random.choice(ENDPOINTS)
        
        # Simple anomaly flag condition
        is_anomaly = True if status in [401, 403] or endpoint == "/config.json" else False
        
        logs.append({
            "id": i + 1,
            "timestamp": time.strftime("%H:%M:%S", time.localtime(now - (count - i) * 5)),
            "ip": ip,
            "endpoint": endpoint,
            "status": status,
            "is_anomaly": is_anomaly
        })
    return logs

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/api/logs")
def get_logs():
    return jsonify(generate_mock_logs(15))

if __name__ == "__main__":
    print("Starting Security Dashboard on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)