import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controllers.classify import classify_comments
from pydantic import BaseModel, validator
import pandas as pd
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
PAGE_ID = os.getenv("FB_PAGE_ID")
ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FB_API_VERSION = os.getenv("FB_API_VERSION", "v18.0")
# post_id = "122098429155169978"

def scrape_facebook_comments(page_id: str, post_id: str, access_token: str):
    """
    Scrapes comments from a specific Facebook post.
    """
    url = f"https://graph.facebook.com/{FB_API_VERSION}/{page_id}_{post_id}"
    params = {
        "fields": "comments.limit(100){from{id,name,link},message,created_time,like_count}",
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        comments_raw = data.get("comments", {}).get("data", [])

        if not comments_raw:
            return 0  

        comments = [{"Comments": c.get("message", "")} for c in comments_raw]

        df = pd.DataFrame(comments)

        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
        DATA_DIR = os.path.join(BASE_DIR, "data")
        os.makedirs(DATA_DIR, exist_ok=True)  

        file_path = os.path.join(DATA_DIR, "comment.xlsx")
        df.to_excel(file_path, index=False)

        logger.info(f"Excel file saved as {file_path}")
        return len(comments)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to Facebook Graph API: {e}")
        raise HTTPException(status_code=500, detail="Failed to scrape comments")
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing Facebook API response: {e}")
        raise HTTPException(status_code=500, detail="Error parsing data from Facebook.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

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
    page_id = request.headers.get("X-FB-Page-Id", "").strip() or PAGE_ID
    access_token = request.headers.get("X-FB-Access-Token", "").strip() or ACCESS_TOKEN

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
    """
    Fetch posts from a Facebook Page using credentials from headers.
    Headers: X-FB-Page-Id, X-FB-Access-Token
    """
    page_id = request.headers.get("X-FB-Page-Id")
    access_token = request.headers.get("X-FB-Access-Token")

    if not page_id or not access_token:
        raise HTTPException(status_code=400, detail="Missing credentials. Provide X-FB-Page-Id and X-FB-Access-Token headers.")

    url = f"https://graph.facebook.com/v18.0/{page_id}/posts"
    params = {
        "fields": "id,message,created_time,permalink_url",
        "access_token": access_token,
        "limit": 20
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        posts = []
        for post in data.get("data", []):
            post_id_full = post.get("id", "")
            post_id = post_id_full.split("_")[1] if "_" in post_id_full else post_id_full

            posts.append({
                "id": post_id,
                "message": post.get("message", "")[:100],  # Truncate long messages
                "created_time": post.get("created_time", ""),
                "permalink_url": post.get("permalink_url", "")
            })

        return {
            "posts": posts,
            "total": len(posts),
            "paging": data.get("paging", {})
        }

    except HTTPException:
        raise
    except requests.exceptions.Timeout:
        logger.error("Timeout fetching posts")
        raise HTTPException(status_code=504, detail="Request timed out")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch posts. Please try again later.")
    except Exception as e:
        logger.error(f"Unexpected error fetching posts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred")

@app.post("/scrape")
def scrape_comments_endpoint(data: PostRequest, request: Request):
    """
    API endpoint to trigger scraping of comments for a given post_id.
    Credentials can be passed via headers (X-FB-Page-Id, X-FB-Access-Token) or use environment variables as fallback.
    """
    try:
        page_id, access_token = get_credentials(request)
        total_comments = scrape_facebook_comments(page_id, data.post_id, access_token)
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
    """
    Classify comments for a given post_id.
    Gemini API key can be passed via X-Gemini-Api-Key header or use environment variable as fallback.
    """
    try:
        gemini_api_key = request.headers.get("X-Gemini-Api-Key", "").strip() or GEMINI_API_KEY

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

