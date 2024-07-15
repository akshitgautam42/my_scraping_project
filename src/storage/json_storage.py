import os
import json
from typing import List

from src.models import Product
from .base_storage import BaseStorage  # Ensure this path is correct based on your project structure

class JsonStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cache = {}
        self.load()

    def load(self):
        """Load existing data into cache on initialization."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                    for product_data in data:
                        self.cache[product_data['title']] = product_data['price']
                except json.JSONDecodeError:
                    print("Failed to decode JSON. The file might be empty or corrupted.")

    def save(self, products: List[Product]):
        """Save product data to a JSON file only if there are changes."""
        updated = False
        data = []
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
            else:
                print(f"File {self.file_path} does not exist. Creating a new one.")
        except json.JSONDecodeError:
            print("Failed to decode JSON. Starting fresh.")

        for product in products:
            product_dict = product.dict()
            if (product_dict['title'] not in self.cache) or (self.cache[product_dict['title']] != product_dict['price']):
                print(f"Updating or adding product: {product_dict['title']}")
                self.cache[product_dict['title']] = product_dict['price']
                updated = True
                if not any(d['title'] == product_dict['title'] for d in data):
                    data.append(product_dict)
            else:
                print(f"No changes for product: {product_dict['title']}")

        if updated:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Data saved to {self.file_path}")
        else:
            print("No updates to save.")

        return updated


    def product_changed(self, product: Product):
        """Check if the product price has changed compared to the cache."""
        product_dict = product.dict()  # Use Pydantic's built-in dict() method
        return self.cache.get(product_dict['title']) != product_dict['price']
