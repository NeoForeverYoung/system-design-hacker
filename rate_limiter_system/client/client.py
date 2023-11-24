# Implementing the client example in 'client.py'.
# This script will send requests to our HTTP server and handle responses.

import requests
import time

def send_request(client_id):
    url = "http://localhost:5000/api"
    params = {'client_id': client_id}
    response = requests.get(url, params=params)
    return response

def simulate_requests(client_id, request_count):
    for _ in range(request_count):
        response = send_request(client_id)
        if response.status_code == 200:
            print(f"Request successful: {response.json()}")
        elif response.status_code == 429:
            print("Request throttled: Too Many Requests")
        time.sleep(1)  # Wait for 1 second between requests

if __name__ == "__main__":
    CLIENT_ID = "client_1"
    REQUEST_COUNT = 20  # Number of requests to send

    simulate_requests(CLIENT_ID, REQUEST_COUNT)

# This client will send a series of requests to the HTTP server and display the response.
# It handles both successful and throttled (429) responses.

# Next, you can test the entire system by running the Redis server, our HTTP server, and the client.
# Observe how the rate limiter behaves under different request rates.

# Please type 'next' or 'continue' for further instructions or if you have any other questions! 😄
