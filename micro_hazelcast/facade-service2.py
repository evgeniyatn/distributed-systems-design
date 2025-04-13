from flask import Flask, request, jsonify
import requests, uuid, time, random

app = Flask(__name__)


MAX_RETRIES = 3
RETRY_DELAY = 2

CONFIG_SERVER_URL = 'http://localhost:6000/services'

def get_service_ips(service_name):
    try:
        res = requests.get(f"{CONFIG_SERVER_URL}/{service_name}")
        if res.status_code == 200:
            return res.json()
    except requests.RequestException:
        pass
    return []

@app.route('/', methods=['POST', 'GET'])
def handle_req():
    if request.method == 'POST':
        msg = request.form.get('msg')
        if not msg:
            return jsonify('Message not received'), 400
        msg_id = str(uuid.uuid4())
        response = {'id': msg_id, 'msg': msg}

        # Отримати список лог-сервісів
        logging_ips = get_service_ips("logging-service")
        if not logging_ips:
            return jsonify("No logging-service instances found"), 503
        
        # Вибрати випадковий інстанс
        logging_service_url = f"{random.choice(logging_ips)}/logs"

        for attempt in range(MAX_RETRIES):
            try:
                action = requests.post(logging_service_url, data=response, timeout=5)
                if action.status_code == 201:
                    return jsonify(response), 200
            except requests.RequestException:
                time.sleep(RETRY_DELAY)

        return jsonify('Logging service unavailable after retries'), 503

    elif request.method == 'GET':
        logging_ips = get_service_ips("logging-service")
        msg_ips = get_service_ips("messages-service")

        results = []

        if logging_ips:
            try:
                log_response = requests.get(f"{random.choice(logging_ips)}/logs")
                results.append(f"logging-service: {log_response.text}")
            except:
                results.append("logging-service: error")

        if msg_ips:
            try:
                msg_response = requests.get(f"{msg_ips[0]}/messages")
                results.append(f"message-service: {msg_response.text}")
            except:
                results.append("message-service: error")

        return jsonify(results), 200

    return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=5000)
