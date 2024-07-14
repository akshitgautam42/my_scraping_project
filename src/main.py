from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from .scraper_service import ScraperService
from .storage import JsonStorage
from .notification_service import ConsoleNotifier
from .models import ScrapeSettings

app = FastAPI()
scraper_service = ScraperService(base_url="https://dentalstall.com/shop/")
storage = JsonStorage(file_path="products.json")
notify_service = ConsoleNotifier()

@app.post("/scrape/")
async def scrape(settings: ScrapeSettings):
    products = scraper_service.scrape_products(settings)
    # storage.save(products)
    notify_service.send(len(products))
    return {"message": f"Scraped and stored {len(products)} products."}
