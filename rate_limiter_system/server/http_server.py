from flask import Flask, request, jsonify
from rate_limiter import RateLimiter  # Importing the RateLimiter class

app = Flask(__name__)
rate_limiter_instance = RateLimiter()  # Creating an instance of RateLimiter

@app.route('/api', methods=['GET', 'POST'])
def api_endpoint():
    client_id = request.args.get('client_id')  # Assuming each client sends a unique client_id
    if rate_limiter_instance.is_request_allowed(client_id):
        # If the request is allowed by the rate limiter
        return jsonify({"message": "Request successful"}), 200
    else:
        # If the request is throttled by the rate limiter
        return jsonify({"error": "Too Many Requests"}), 429

if __name__ == '__main__':
    app.run(debug=True, port=5000)
