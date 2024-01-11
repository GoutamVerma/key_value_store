# create micromicerser 
# set {key:value}
# get {key} return value
# delete {key}
# get_all return all data

# distributed 

import time
import threading
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

data = {}
lock = threading.Lock()


def delete_thread():
    while True:
        with lock:
            for key in data:
                if data[key]['time_out'] < datetime.now():
                    del data[key]
        time.sleep(10)


@app.route('/get', methods=['GET'])
def get_value():
    key = request.args.get('key')
    with lock:
        if key in data:
            stored_data = data[key]
            current_time = datetime.now()
            if stored_data['time_out'] > current_time:
                return jsonify({'value': stored_data['value'], 'time_out': stored_data['time_out'], 'current_time': current_time})
            else:
                data.pop(key)
                return jsonify({'error': 'Data not found'})
        else:
            return jsonify({'error': 'Data not found'})


@app.route('/set', methods=['GET'])
def set_value():
    key = request.args.get('key')
    value = request.args.get('value')
    store_time = datetime.now()
    timeout = int(request.args.get('timeout'))
    timeout_timestamp = store_time + timedelta(seconds=timeout)
    with lock:
        data[key] = {'value': value, 'time_out': timeout_timestamp}
    return jsonify({'message': 'Value set successfully', 'key': key, 'value': value, 'timeout': timeout_timestamp})


@app.route('/delete', methods=['GET'])
def delete_value():
    key = request.args.get('key')
    with lock:
        if key in data:
            del data[key]
            return jsonify({'message': 'Value deleted successfully'})
        else:
            return jsonify({'error': 'Key not found'})


@app.route('/all', methods=['GET'])
def get_all_data():
    with lock:
        return jsonify(data)


if __name__ == '__main__':
    delete_thread = threading.Thread(target=delete_thread)
    delete_thread.start()
    app.run(debug=True)
