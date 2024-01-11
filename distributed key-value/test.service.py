import concurrent.futures
import subprocess
import time
import json
import requests

# Function to start a replica
def start_replica(replica_number, port_number):
    command = ["python3", "service.py", str(port_number)]
    process = subprocess.Popen(command)
    print(f"Replica {replica_number} started on port {port_number} with PID {process.pid}")
    return process

# Function to perform concurrent operations on a replica
def perform_operations(replica_number, port_number):
    base_url = f"http://localhost:{port_number}"
    keys_to_insert = [f"key{i}" for i in range(replica_number, replica_number + 10)]
    
    # Insert keys
    insert_responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, f"{base_url}/set?id={key}&value=value&timeout=60") for key in keys_to_insert]
        insert_responses = [future.result() for future in futures]

    # Read keys
    read_responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, f"{base_url}/get?id={key}") for key in keys_to_insert]
        read_responses = [future.result() for future in futures]

    # Delete keys
    delete_responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, f"{base_url}/delete?id={key}") for key in keys_to_insert]
        delete_responses = [future.result() for future in futures]

    print(f"Replica {replica_number} on port {port_number} - Insert Responses: {insert_responses}")
    print(f"Replica {replica_number} on port {port_number} - Read Responses: {read_responses}")
    print(f"Replica {replica_number} on port {port_number} - Delete Responses: {delete_responses}")

# Start multiple replicas
replica_processes = []
port_number = 5000
for i in range(1, 10):
    replica_processes.append(start_replica(i, port_number))
    port_number += 1

print("Waiting for replicas to start...")    
time.sleep(10)

# Perform concurrent operations on each replica
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(perform_operations, i, port_number) for i, port_number in enumerate(range(5000, 5003), start=1)]
    results = [future.result() for future in futures]

# Terminate all replicas
for process in replica_processes:
    process.terminate()
    process.wait()

print("Test completed.")
