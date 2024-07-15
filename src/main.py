from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from .security.api_key_security import get_api_key  # Import the security function
from .scraper_service import ScraperService
from .notification_service import ConsoleNotifier
from .models import ScrapeSettings
from .storage.json_storage import JsonStorage  # Make sure the path matches your project structure

app = FastAPI()

# Initialize services
scraper_service = ScraperService(base_url="https://dentalstall.com/shop/")
storage = JsonStorage(file_path="products.json")  # Assuming JsonStorage is correctly implemented
notify_service = ConsoleNotifier()

@app.post("/scrape/", dependencies=[Depends(get_api_key)])
async def scrape(settings: ScrapeSettings):
    products = scraper_service.scrape_products(settings)
    storage.save(products)  # Assuming save method handles the checking for changes and saving
    notify_service.send(len(products))
    return {"message": f"Scraped and stored {len(products)} products."}
