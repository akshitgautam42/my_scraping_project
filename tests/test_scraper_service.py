import pytest
from src.scraper_service import ScraperService
from src.models import ScrapeSettings

@pytest.fixture
def scraper_service():
    return ScraperService(base_url="https://dentalstall.com/shop/")

def test_extract_title_from_url(scraper_service):
    url = "https://dentalstall.com/product/sample-product"
    title = scraper_service.extract_title_from_url(url)
    assert title == "Sample Product", "Title extraction did not work as expected"

def test_clean_price(scraper_service):
    price_text = "₹1,995.00"
    price = scraper_service.clean_price(price_text)
    assert price == 1995.0, "Price cleaning did not convert correctly"
