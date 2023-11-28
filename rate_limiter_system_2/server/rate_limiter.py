
import redis
import time
import os
from dotenv import load_dotenv


class RateLimiter:
    def __init__(self, capacity=10, refill_time=30):
        self.capacity = capacity
        # unit: second
        self.refill_time = refill_time
        # load config file
        load_dotenv()
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_password = os.getenv('REDIS_PASSWORD')
        try:
            self.redis = redis.StrictRedis(
                host=redis_host,
                port=redis_port,
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

    def is_request_allowed(self, client_id):
        key = f"rate_limit:{client_id}"
        # if the setnx return 1, it means the key does not exist.
        if self.redis.setnx(key, 1):
            # no key
            self.redis.expire(key, self.refill_time)
            # key exists
            return True
        else:
            # key exists
            count = self.redis.incr(key)
            if count > self.capacity:
                return False
            else:
                return True
