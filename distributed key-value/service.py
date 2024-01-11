import json, time, sys, fcntl, errno, threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)
data_file = 'data.json'

def delete_task():
    while True:
        time.sleep(20)
        with open(data_file, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            data = json.load(f)
            current_time = datetime.now()
            for key in list(data.keys()):
                datetime_obj = datetime.strptime(data[key]['time_out'], '%Y-%m-%dT%H:%M:%S')
                if datetime_obj < current_time:
                    del data[key]
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            fcntl.flock(f, fcntl.LOCK_UN)
        

@app.route('/set', methods=['GET'])
def set_value():
    id = request.args.get('key')
    value = request.args.get('value')
    store_time = datetime.now()
    timeout = int(request.args.get('timeout'))
    timeout_timestamp = store_time + timedelta(seconds=timeout)

    while True:
        try:
            with open(data_file, 'r+') as f:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(f)
                data[id] = {'value': value, 'time_out': timeout_timestamp.strftime('%Y-%m-%dT%H:%M:%S')}
                f.seek(0)
                f.truncate()
                json.dump(data, f)
                fcntl.flock(f, fcntl.LOCK_UN)
                break
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                time.sleep(0.1) 

    return jsonify({'message': 'Value set successfully', 'key': id, 'value': value, 'timeout': timeout_timestamp})


@app.route('/get', methods=['GET'])
def get():
    id = request.args.get('key')

    while True:
        try:
            with open(data_file, 'r+') as f:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(f)

                print("After:", json.dumps(data, indent=2)) 

                if id not in data:
                    fcntl.flock(f, fcntl.LOCK_UN)
                    return jsonify({'error': 'Data not found'})
                else:
                    stored_data = data[id]
                    current_time = datetime.now()
                    datetime_obj = datetime.strptime(stored_data['time_out'], '%Y-%m-%dT%H:%M:%S')
                    if datetime_obj > current_time:
                        fcntl.flock(f, fcntl.LOCK_UN)
                        return jsonify(stored_data)
                    else:
                        del data[id]
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f)
                        fcntl.flock(f, fcntl.LOCK_UN)
                        return jsonify({'error': 'Data not found'})
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                time.sleep(0.1)


@app.route('/delete', methods=['GET'])
def delete():
    id = request.args.get('key')

    while True:
        try:
            with open(data_file, 'r+') as f:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(f)

                if id not in data:
                    fcntl.flock(f, fcntl.LOCK_UN)
                    return jsonify({'error': 'Data not found'})
                del data[id]
                f.seek(0)
                f.truncate()
                json.dump(data, f)
                fcntl.flock(f, fcntl.LOCK_UN)
                return jsonify(data)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                time.sleep(0.1)


@app.route('/all', methods=['GET'])
def list_data():
    while True:
        try:
            with open(data_file, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                data = json.load(f)
                return jsonify(data)
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                time.sleep(0.1) 

if __name__ == '__main__':
   port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
   app.run(debug=True, port=port)
