from flask import Flask, request, jsonify
import requests, uuid, time
from pyotp import random

app = Flask(__name__)

messages_service = 'http://localhost:5004/messages'
MAX_RETRIES = 3  # Максимальна кількість спроб
RETRY_DELAY = 2  # Час між спробами (секунди)


@app.route('/', methods=['POST', 'GET'])

def handle_req():
    if request.method == 'POST':
        msg = request.form.get('msg')
        if not msg:
            return jsonify('Message not received'), 400
        msg_id = str(uuid.uuid4())
        
        port = random.randint(5001, 5003)
        logging_service_url = f"http://localhost:{port}/logs"
        
        response = {'id': msg_id, 'msg': msg}
        
        # Реалізація механізму retry
        for attempt in range(MAX_RETRIES):
            try:
                action = requests.post(logging_service_url, data=response, timeout=5)
                if action.status_code == 201:
                    return jsonify(response), 200
            except requests.RequestException:
                print(f"Retry {attempt + 1}/{MAX_RETRIES}: Logging service unavailable, retrying...")
                time.sleep(RETRY_DELAY)
        
        return jsonify('Logging service unavailable after retries'), 503
   
    elif request.method == 'GET':
        port = random.randint(5001, 5003)
        logging_service_url = f"http://localhost:{port}/logs"
    
        log_response = requests.get(logging_service_url)
        msg_response = requests.get(messages_service)
        return [f'logging-service: {log_response.text}'[:-1], f'message-service: {msg_response.text}'], 200
   
    else:
        return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=5000)
