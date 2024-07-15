import os
import requests
from urllib.parse import urlparse
from .base_storage import BaseStorage  # Ensure this import is correct based on your project structure

class ImageStorage(BaseStorage):
    def __init__(self, storage_dir='images'):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)  # Ensure the storage directory exists

    def save(self, image_url, title):
        """Override the abstract save method to download and save an image."""
        return self.download_image(image_url, title)

    def load(self):
        """Load method is not typically needed for ImageStorage but required by the base class."""
        raise NotImplementedError("Load method is not applicable for ImageStorage")

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
