from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/messages', methods=['GET'])
def static_mes():
    if request.method == 'GET':
        return 'Message-service not implemented yet'
    else:
        return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=5004)
