from flask import Flask, request, jsonify
import hazelcast
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

p = subprocess.Popen(["hz", "start"])

hz = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[])
logs_msg = hz.get_map("messages").blocking()

app = Flask(__name__)


@app.route('/logs', methods=['POST', 'GET'])
def task():
   
    if request.method == 'POST':
        msg_id = request.form.get('id')
        msg =  request.form.get('msg')
        if not (msg_id or msg):
            return jsonify('No id or text'), 400
            
        logs_msg.put(msg_id, msg)
        print('Message:', msg)
        return jsonify('Logged'), 201
   
    elif request.method == 'GET':
    	all_msg = {key: logs_msg.get(key) for key in logs_msg.key_set()}
    	return jsonify(all_msg), 200
   
    else:
        return jsonify('Method not allowed'), 405

if __name__ == '__main__':
    app.run(port=args.port)
