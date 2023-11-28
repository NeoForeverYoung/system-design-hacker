import requests
import time


def send_request(client_id):
    url = "localhost:5000/api"
    params = {"client_id": client_id}
    response = requests.get(url, params=params)
    return response


if __name__ == "__main__":
    count = 10
    client_id = "client_1"
    for _ in range(count):
        send_request(client_id)
