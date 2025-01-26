import json
import os
from typing import List
from models.product import Product
import logging


DATABASE_FILE = "database/scraped_data.json"

class DatabaseHandler:
    def __init__(self, file_name: str = DATABASE_FILE):
        self.file_name = file_name
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def save_product_data(self, product_data: List[Product]):
        # Check if the file exists
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Convert the data in the JSON file to a dictionary keyed by product_title
        product_map = {product["product_title"]: product for product in data}

        # Iterate over the product_arr to update or insert products
        for product in product_data:
            if product.product_title in product_map:
                # Update the existing product details
                product_map[product.product_title]["product_price"] = product.product_price
                product_map[product.product_title]["path_to_image"] = product.path_to_image
            else:
                # Add the new product
                product_map[product.product_title] = product.dict()

        # Write the updated data back to the file
        with open(self.file_name, "w") as file:
            json.dump(list(product_map.values()), file, indent=4)
