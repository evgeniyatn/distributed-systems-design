from flask import Flask, request, jsonify
import grpc
import logging_pb2
import logging_pb2_grpc
import uuid, requests
import time

app = Flask(__name__)

logging_host = 'localhost:5001'
messages_service = 'http://localhost:5002/messages'
MAX_RETRIES = 3
RETRY_DELAY = 2

# Функція для логування повідомлення через GRPC із retry
def log_message_with_retry(msg_id, msg):
    for attempt in range(MAX_RETRIES):
        try:
            with grpc.insecure_channel(logging_host) as channel:
                stub = logging_pb2_grpc.LoggingServiceStub(channel)
                response = stub.LogMessage(logging_pb2.LogRequest(id=msg_id, msg=msg))
                return response.status
        except grpc.RpcError:
            print(f"Retry {attempt + 1}/{MAX_RETRIES}: Logging service unavailable, retrying...")
            time.sleep(RETRY_DELAY)
    return "Logging service unavailable after retries, 503"

@app.route('/', methods=['POST', 'GET'])
def handle_req():
    if request.method == 'POST':
        msg = request.form.get('msg')
        if not msg:
            return jsonify('Message not received'), 400
        msg_id = str(uuid.uuid4())

        # Викликаємо GRPC-сервіс із retry
        status = log_message_with_retry(msg_id, msg)
        return jsonify({'id': msg_id, 'msg': msg, 'status': status})
    
    elif request.method == 'GET':
        # Отримуємо логи через GRPC
        with grpc.insecure_channel(logging_host) as channel:
            stub = logging_pb2_grpc.LoggingServiceStub(channel)
            log_response = stub.GetLogs(logging_pb2.Empty())

        # Отримуємо відповідь від messages-service через HTTP
        msg_response = requests.get(messages_service)

        return jsonify({
            "logs": list(log_response.logs),  # Приведення до списку
            "message_service": msg_response.text
        }), 200



    else:
        return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=5000)
