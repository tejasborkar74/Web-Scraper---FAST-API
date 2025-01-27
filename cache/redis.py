from logging import Logger
import redis
import json
from models.product import Product
from typing import Union


class RedisCache:
    def __init__(self, configs, logger: Logger):
        try:
            # Create a Redis client with connection settings
            self.client = redis.StrictRedis(
                host=configs["REDIS_HOST"],
                port=configs["REDIS_PORT"],
                db=0,
                decode_responses=True
            )
            self.logger = logger
            # Test the connection to Redis server
            self.client.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            # If Redis is down or connection fails, log the error (optional) and set client to None
            self.client = None
            self.logger.error(f"Redis connection failed: {e}")

    def get_product(self, key: str) -> Union[dict, None]:
        if not self.client:
            return None 
        """Retrieve product data from Redis by key."""
        try:
            product_data = self.client.get(key)
            if product_data:
                return json.loads(product_data)
            return None
        except redis.exceptions.RedisError as e:
            # If an error occurs during Redis operation, return None
            self.logger.error(f"Redis operation failed: {e}")
            return None

    def set_product(self, key: str, product: Product):
        if not self.client:
            return None  # Redis is down, return None

        try:
            self.client.set(key, json.dumps(product.model_dump()))
        except redis.exceptions.RedisError as e:
            # If an error occurs during Redis operation, log it (optional) and return None
            self.logger.error(f"Failed to set product in Redis: {e}")
            return None