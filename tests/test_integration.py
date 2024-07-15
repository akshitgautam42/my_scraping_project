import pytest
from src.scraper_service import ScraperService
from src.models import ScrapeSettings
from src.storage.json_storage import JsonStorage

def test_scrape_and_save():
    settings = ScrapeSettings(pages=1)
    scraper = ScraperService("https://dentalstall.com/shop/")
    products = scraper.scrape_products(settings)  # No 'await' needed here
    storage = JsonStorage("test_products.json")
    storage.save(products)
    assert len(products) > 0, "No products were scraped or saved"
