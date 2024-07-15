from fastapi import FastAPI, Depends
from .security.api_key_security import get_api_key 
from .scraper_service import ScraperService
from .notification_service import ConsoleNotifier
from .models import ScrapeSettings
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

app = FastAPI()

scraper_service = ScraperService(base_url=base_url)
notify_service = ConsoleNotifier()

@app.post("/scrape/", dependencies=[Depends(get_api_key)])
async def scrape(settings: ScrapeSettings):
    products = scraper_service.scrape_products(settings)
    notify_service.send(len(products))
    return {"message": f"Scraped and stored {len(products)} products."}
