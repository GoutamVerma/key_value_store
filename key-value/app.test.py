import unittest
import threading
import time
from datetime import datetime, timedelta
import requests
from app import app, data

class TestMicroMicroservice(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_set_value(self):
        response = self.app.get('/set?key=test_key&value=test_value&timeout=60')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Value set successfully')

    def test_get_value_within_timeout(self):
        response_set = self.app.get('/set?key=test_key&value=test_value&timeout=60')
        self.assertEqual(response_set.status_code, 200)

        response_get = self.app.get('/get?key=test_key')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('value', response_get.json)
        self.assertIn('time_out', response_get.json)
        self.assertIn('current_time', response_get.json)

    def test_get_value_expired(self):
        response_set = self.app.get('/set?key=test_key&value=test_value&timeout=1')
        self.assertEqual(response_set.status_code, 200)

        time.sleep(2)  # Wait for expiration

        response_get = self.app.get('/get?key=test_key')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('error', response_get.json)
        self.assertEqual(response_get.json['error'], 'Data not found')

    def test_delete_value(self):
        response_set = self.app.get('/set?key=test_key&value=test_value&timeout=60')
        self.assertEqual(response_set.status_code, 200)

        response_delete = self.app.get('/delete?key=test_key')
        self.assertEqual(response_delete.status_code, 200)
        self.assertIn('message', response_delete.json)
        self.assertEqual(response_delete.json['message'], 'Value deleted successfully')

    def test_delete_non_existing_value(self):
        response_delete = self.app.get('/delete?key=non_existent_key')
        self.assertEqual(response_delete.status_code, 200)
        self.assertIn('error', response_delete.json)
        self.assertEqual(response_delete.json['error'], 'Key not found')

    def test_get_all_data(self):
        response_set = self.app.get('/set?key=test_key&value=test_value&timeout=60')
        self.assertEqual(response_set.status_code, 200)

        response_all = self.app.get('/all')
        self.assertEqual(response_all.status_code, 200)
        
        actual_timestamp = response_all.json['test_key']['time_out']
        expected_response = {'test_key': {'value': 'test_value', 'time_out': actual_timestamp}}

        self.assertEqual(response_all.json, expected_response)


    def test_concurrent_set_and_get(self):
        def set_value():
            response_set = self.app.get('/set?key=test_key&value=test_value&timeout=60')
            self.assertEqual(response_set.status_code, 200)
            print(f"Set response: {response_set.json}")

        def get_value():
            response_get = self.app.get('/get?key=test_key')
            self.assertEqual(response_get.status_code, 200)
            print(f"Get response: {response_get.json}")
            self.assertIn('value', response_get.json)

        # Simulate concurrent set and get requests
        threads = []
        for func in [set_value, get_value]:
            thread = threading.Thread(target=func)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Ensure that the final data is consistent
        response_all = self.app.get('/all')
        self.assertEqual(response_all.status_code, 200)
        print(f"All data response: {response_all.json}")

        # Extract the timestamp from the actual response and update the expected response
        actual_timestamp = response_all.json['test_key']['time_out']
        expected_response = {'test_key': {'value': 'test_value', 'time_out': actual_timestamp}}

        self.assertEqual(response_all.json, expected_response)




if __name__ == '__main__':
    unittest.main()
