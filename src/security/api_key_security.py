from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey

API_KEY = "1234567890abcdef"  # Consider using environment variables for production
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")
