import redis
import time
import os
from dotenv import load_dotenv

# setnx and expire


class RateLimiter:
    def __init__(self, redis_host='localhost', redis_port=6379, capacity=2, refill_time=1000):
        # Load environment variables
        load_dotenv()

        # Connect to the Redis server with credentials from environment variables
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        # redis_username = os.getenv('REDIS_USERNAME')
        redis_password = os.getenv('REDIS_PASSWORD')
        try:
            self.redis = redis.StrictRedis(
                host=redis_host,
                port=redis_port,
                # username=redis_username,
                password=redis_password,
                decode_responses=True
            )
            self.redis.ping()  # Attempt to connect and perform an action to check the connection
        except redis.exceptions.ConnectionError as e:
            # Handle the connection error
            print(f"Failed to connect to Redis: {e}")
            # Depending on your application's needs, you might want to:
            # - Retry the connection
            # - Exit the program
            # - Raise the exception to be handled by the caller
            raise
        except redis.exceptions.AuthenticationError as e:
            # Handle incorrect credentials
            print(f"Authentication failed: {e}")
            raise
        self.capacity = capacity  # Maximum tokens in the bucket
        self.refill_time = refill_time  # Time to refill the bucket

    # https://dev.to/astagi/rate-limiting-using-python-and-redis-58gk
    # Does this code have race condition?
    def is_request_allowed(self, client_id):
        key = f"rate_limit:{client_id}"
        if self.redis.setnx(key, 1):
            # no key
            self.redis.expire(key, self.refill_time)
            # key exists
        else:
            count = self.redis.incr(key)
            if count > self.capacity:
                return False
        return True


"""
# Usage example
rate_limiter = RateLimiter()
client_id = "client_1"
allowed = rate_limiter.is_request_allowed(client_id)
print("Allowed" if allowed else "Blocked")
"""
