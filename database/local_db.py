import json
import os
from typing import List
from models.product import Product
# from config.config_loader import load_config
from cache.redis import RedisCache
import logging


class DatabaseHandler:
    def __init__(self, configs):
        self.configs = configs
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def save_product_data(self, product_data: List[Product], redisClient: RedisCache):
        # Check if the file exists
        if os.path.exists(self.configs["DATABASE_URL"]):
            with open(self.configs["DATABASE_URL"], "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Convert the data in the JSON file to a dictionary keyed by product_title
        existing_product_map = {product["product_title"]: product for product in data}

        # Iterate over the product_arr to update or insert products
        for product in product_data:
            redis_key = product.product_title 
            cached_product = redisClient.get_product(redis_key)
            
            if cached_product:
                # If product exists in cache, compare price
                if float(cached_product["product_price"]) != product.product_price:
                    # Update Redis cache and mark product as updated
                    existing_product_map[product.product_title] = product
                    redisClient.set_product(redis_key, product)   
            else:
                # If product is not in cache, add to Redis and JSON
                existing_product_map[product.product_title] = product.model_dump()
                redisClient.set_product(redis_key, product)

        # Write the updated data back to the file
        with open(self.configs["DATABASE_URL"], "w") as file:
            json.dump(list(existing_product_map.values()), file, indent=4)