# Key-Value Store
This project is a key-value storage system divided into two parts:



## Simple Key-Value Store

A basic key-value store with an added feature - each key has a specified timeout (in seconds), and the value associated with the key will be automatically deleted once the timeout period elapses.

<details>
  <summary>Click to expand and see endpoints</summary>

  ## Endpoints
  1. **Get Value**
     - URL: `/get`
     - Method: `GET`
     - Parameters: `key`
     - Example: `curl -X GET "http://localhost:5000/get?key=1"`
     - Response: 
       ```json
       {
         "current_time": "Thu, 11 Jan 2024 21:09:21 GMT", 
         "time_out": "Thu, 11 Jan 2024 21:09:26 GMT", 
         "value": "hello"
       }
       ```

  2. **Set Key-Value:**
     - URL: `/set`
     - Method: `GET`
     - Parameters: `key`, `value`, `timeout` (in seconds)
     - Example: `curl -X GET "http://localhost:5000/set?key=1&value=hello&timeout=10"`
     - Response:
       ```json
       {
         "key": "1", 
         "message": "Value set successfully", 
         "timeout": "Thu, 11 Jan 2024 21:09:37 GMT", 
         "value": "hello"
       }
       ```

  3. **Delete Value:**
     - URL: `/delete`
     - Method: `GET`
     - Parameters: `key`
     - Example: `curl -X GET "http://localhost:5000/delete?key=1"`
     - Response:
       ```json
       {
         "message": "Value deleted successfully"
       }
       ```

  4. **Retrieve all data:**
     - URL: `/all`
     - Method: `GET`
     - Example: `curl -X GET "http://localhost:5000/all"`
     - Response:
       ```json
       {
         "1": {
           "time_out": "Thu, 11 Jan 2024 21:12:31 GMT", 
           "value": "hello"
         }
       }
       ```

</details>

### Getting Started

1. Clone the Repository:

    ```
    git clone https://github.com/GoutamVerma/key_value_store.git
    cd key_value_store
    ```

2. Set Up Virtual Environment:

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install Dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run Simple Key-Value Store:
    -   Navigate to the `key-value` directory.
    -   Run the service:

    ```
    python3 app.py
    ```

5. Run test cases(optional but recommended):

    ```
    python3 app.test.py
    ```


## Distributed Key-Value Store

An enhanced version of the key-value store where the data is distributed among various services. The services perform CRUD operations with a locking system, allowing only one process at a time to access the resources (similar to the concept of semaphores).

Note: Endpoints are similar to key-value 

### Getting Started

1. Clone the Repository:
    ```
    git clone https://github.com/GoutamVerma/key_value_store.git
    cd key_value_store
    ```

2. Set Up Virtual Environment:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install Dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run Distributed Key-Value Store:
    -   Navigate to the distributed key-value directory.
    -   Run the service:
    ```
    python3 service.py
    ```

5. Run test cases(optional but recommended):
    ```
    python3 test.service.py
    ```


Note: Ensure that git, python3, and pip are installed on your system. Make sure to activate the virtual environment before running the services. Run test cases to validate the functionality of the key-value stores.
