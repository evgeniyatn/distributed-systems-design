from flask import Flask, request, jsonify

app = Flask(__name__)
logs = {}


@app.route('/logs', methods=['POST', 'GET'])
def task():
   
    if request.method == 'POST':
        msg_id = request.form.get('id')
        msg =  request.form.get('msg')
        if not (msg_id or msg):
            return jsonify('No id or text'), 400
            
        if msg_id in logs:
            return jsonify('Duplicate message ignored'), 200
        
        logs[msg_id] = msg
        print('Message:', msg)
        return jsonify('Logged'), 201
   
    elif request.method == 'GET':
        return jsonify(list(logs.values())), 200
   
    else:
        return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=5001)
