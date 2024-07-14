import os
import json
import requests
from urllib.parse import urlparse



class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cache = {}
        self.load_cache()

    def load_cache(self):
        """Load existing data into cache on initialization."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                    for product in data:
                        # Ensure both keys exist in the data; otherwise, skip the entry
                        if 'title' in product and 'price' in product:
                            self.cache[product['title']] = product['price']
                except json.JSONDecodeError:
                    # Handle empty or corrupted JSON file
                    print("Failed to decode JSON. The file might be empty or corrupted.")

    def save(self, products):
        """Save product data to a JSON file only if there are changes."""
        updated = False
        data = []
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
        except json.JSONDecodeError:
            print("Failed to decode JSON. Starting fresh.")
            
        for product in products:
            if (product.title not in self.cache) or (self.cache[product.title] != product.price):
                self.cache[product.title] = product.price
                updated = True
                # Only append product data if not already included
                if not any(d['title'] == product.title for d in data):
                    data.append(product.dict())

        if updated:
            with open(self.file_path, 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        return updated

    def product_changed(self, product):
        """Check if the product price has changed compared to the cache."""
        return self.cache.get(product.title) != product.price



class ImageStorage:
    def __init__(self, storage_dir='images'):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)  # Ensure the storage directory exists

    def download_image(self, image_url, title):
        """Download an image from a URL and save it under a unique filename derived from the product title."""
        if not image_url or image_url.startswith('data:image'):  # Skip placeholder images
            return "No image available"
        
        filename = self.create_filename(title, image_url)
        file_path = os.path.join(self.storage_dir, filename)
        
        # Download the image only if it does not already exist to save bandwidth
        if not os.path.exists(file_path):
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                return "Failed to download image"
        
        return file_path

    def create_filename(self, title, image_url):
        """Generate a unique filename for the image based on its URL and the product title."""
        clean_title = "".join(char if char.isalnum() else "_" for char in title)
        ext = urlparse(image_url).path.split('.')[-1]
        if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
            ext = 'jpg'  # Default to JPG if unknown
        filename = f"{clean_title}.{ext}"
        return filename


