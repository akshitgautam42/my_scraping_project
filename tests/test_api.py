import httpx
import pytest
from src.main import app

@pytest.mark.asyncio
async def test_api_scrape():
   
    api_key = "1234567890abcdef"
    headers = {
        "access_token": api_key  
    }
   
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/scrape/", json={"pages": 1}, headers=headers)
        assert response.status_code == 200
        assert "Scraped and stored" in response.json()['message']
