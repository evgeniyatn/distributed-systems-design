from flask import Flask, jsonify
import json

app = Flask(__name__)

# Завантаження сервісів з конфігураційного файлу
with open("config.json") as f:
    service_registry = json.load(f)

@app.route('/services/<service_name>', methods=['GET'])
def get_service_ips(service_name):
    if service_name in service_registry:
        return jsonify(service_registry[service_name]), 200
    return jsonify({"error": f"Service '{service_name}' not found"}), 404

if __name__ == '__main__':
    app.run(port=6000)
