import json
import time
from threading import Thread, Lock
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)
lock = Lock()


def delete_thread():
    while True:
        time.sleep(20)
        with lock:
            with open('data.json', 'r') as f:
                data = json.load(f)
            current_time = datetime.now()
            for key in data:
                datetime_obj = datetime.strptime(data[key]['time_out'], '%Y-%m-%dT%H:%M:%S')
                if datetime_obj < current_time:
                    del data[key]
            with open('data.json', 'w') as f:
                json.dump(data, f)


@app.route('/set', methods=['GET'])
def set_value():
    id = request.args.get('id')
    value = request.args.get('value')
    store_time = datetime.now()
    timeout = int(request.args.get('timeout'))
    timeout_timestamp = store_time + timedelta(seconds=timeout)
    with lock:
        with open('data.json') as f:
            data = json.load(f)
        
        data[id] = {'value': value, 'time_out': timeout_timestamp.strftime('%Y-%m-%dT%H:%M:%S')}

        with open('data.json', 'w') as f:
            json.dump(data, f)

    return jsonify({'message': 'Value set successfully', 'key': id, 'value': value, 'timeout': timeout_timestamp})


@app.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    with lock:
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        if id not in data:
            return jsonify({'error': 'Data not found'})
        else:
            stored_data = data[id]
            current_time = datetime.now()
            datetime_obj = datetime.strptime(stored_data['time_out'], '%Y-%m-%dT%H:%M:%S')
            if datetime_obj > current_time:
                return jsonify(stored_data)
            else:
                del data[id]
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                return jsonify({'error': 'Data not found'})


@app.route('/delete', methods=['GET'])
def delete():
    id = request.args.get('id')
    with lock:
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        if id not in data:
            return jsonify({'error': 'Data not found'})
        
        del data[id]
        with open('data.json', 'w') as f:
            json.dump(data, f)

    return jsonify(data)


@app.route('/list', methods=['GET'])
def list_data():
    with lock:
        with open('data.json', 'r') as f:
            data = json.load(f)
    
    return jsonify(data)

if __name__ == '__main__':
    delete_thread = Thread(target=delete_thread)
    delete_thread.start()
    app.run(debug=True)