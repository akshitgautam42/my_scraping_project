import requests
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry  # Corrected import
from requests.adapters import HTTPAdapter
from src.models import Product, ScrapeSettings
from src.storage import ImageStorage, JsonStorage
from urllib.parse import unquote, urlparse


class ScraperService:
    def __init__(self, base_url: str, image_folder='images'):
        self.base_url = base_url
        self.image_storage = ImageStorage(image_folder)  # Initialize ImageStorage for handling image downloads

    def fetch_page(self, page_number: int, proxy=None):
        session = requests.Session()
        if proxy:
            session.proxies.update({
                'http': proxy,
                'https': proxy
            })
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        url = f"{self.base_url}/page/{page_number}"
        response = session.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        return BeautifulSoup(response.text, 'html.parser')

    def scrape_products(self, settings:ScrapeSettings):
        products = []
        json_storage = JsonStorage('../products.json')
        for page in range(1, settings.pages + 1):
            soup = self.fetch_page(page)
            items = soup.find_all('div', class_='product-inner')
            for item in items:
                product_link_element = item.find('div', class_='mf-product-thumbnail').find('a', href=True)
                product_link = product_link_element['href']
                title = self.extract_title_from_url(product_link)
                
                price_span = item.find('ins')
                if price_span:
                    price_text = price_span.find('span', class_='woocommerce-Price-amount amount').get_text(strip=True)
                else:
                    price_span = item.find('span', class_='woocommerce-Price-amount amount')
                    price_text = price_span.get_text(strip=True) if price_span else "Unknown"  

                image_element = product_link_element.find('img')
                image_url = self.extract_image_url(image_element)
                local_image_path = self.image_storage.download_image(image_url, title)  # Download image and get local path
                
                if price_text != "Unknown":
                    price = self.clean_price(price_text)
                    products.append(Product(title=title, price=price, image_url=local_image_path))
        json_storage.save(products)
        return products

    def clean_price(self, price_text):
        cleaned_price = ''.join(filter(lambda x: x.isdigit() or x == '.', price_text))
        return float(cleaned_price)

    def extract_title_from_url(self, url):
        parsed_url = urlparse(url)
        path_last_part = parsed_url.path.rstrip('/').split('/')[-1]
        title = unquote(path_last_part).replace('-', ' ').title()
        return title

    def extract_image_url(self, image_element):
        if not image_element:
            return "No image available"
        
        if 'src' in image_element.attrs and not image_element['src'].startswith('data:image'):
            return image_element['src']
        
        lazy_attributes = ['data-src', 'data-lazy-src', 'data-original']
        for attr in lazy_attributes:
            if attr in image_element.attrs:
                return image_element[attr]

        return image_element['src'] if 'src' in image_element.attrs else "No image available"
