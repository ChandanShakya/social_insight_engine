import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import os

# Import services and utilities
from services.facebook_service import FacebookService
from controllers.classify import classify_comments
from utils import config, logger

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "X-FB-Page-Id",
        "X-FB-Access-Token",
        "X-Gemini-Api-Key",
        "Content-Type"
    ],
)

def get_credentials(request: Request) -> tuple[str, str]:
    """Extract and validate credentials from headers with fallback."""
    page_id = request.headers.get("X-FB-Page-Id", "").strip() or config.fb_page_id
    access_token = request.headers.get("X-FB-Access-Token", "").strip() or config.fb_access_token

    if not page_id or not access_token:
        raise HTTPException(
            status_code=400,
            detail="Missing credentials. Provide X-FB-Page-Id and X-FB-Access-Token headers."
        )

    return page_id, access_token

class PostRequest(BaseModel):
    post_id: str

    @validator('post_id')
    def validate_post_id(cls, v):
        if not v or not v.strip():
            raise ValueError('post_id cannot be empty')
        return v.strip()

@app.get("/posts")
def get_posts(request: Request):
    """Fetch posts from Facebook page using credentials from headers."""
    try:
        page_id, access_token = get_credentials(request)
        
        # Use service instead of direct API calls
        service = FacebookService()
        service.page_id = page_id
        service.access_token = access_token
        
        return service.get_recent_posts()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching posts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred")

@app.post("/scrape")
def scrape_comments_endpoint(data: PostRequest, request: Request):
    """API endpoint to trigger scraping of comments for a given post_id."""
    try:
        page_id, access_token = get_credentials(request)
        
        # Use service instead of direct function
        service = FacebookService()
        service.page_id = page_id
        service.access_token = access_token
        
        total_comments = service.scrape_comments(data.post_id)
        
        return {
            "message": "Comments scraped successfully",
            "total_comments": total_comments
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in scrape endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred")

@app.get("/classify")
def get_classification(post_id: str, request: Request):
    """Classify comments for a given post_id."""
    try:
        gemini_api_key = request.headers.get("X-Gemini-Api-Key", "").strip() or config.gemini_api_key

        if not gemini_api_key:
            raise HTTPException(
                status_code=400,
                detail="Missing Gemini API key. Provide X-Gemini-Api-Key header."
            )

        result = classify_comments(gemini_api_key=gemini_api_key)
        return {
            "postId": post_id,
            **result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in classification: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Classification failed")