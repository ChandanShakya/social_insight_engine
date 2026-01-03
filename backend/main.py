from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.classify import classify_comments
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import pandas as pd
import os
import json
import requests
app = FastAPI()
PAGE_ID = "61585099347820" 
ACCESS_TOKEN = "your_access_token"

def scrape_facebook_comments(page_id: str, post_id: str, access_token: str):
    """
    Scrapes comments from a specific Facebook post.
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}_{post_id}"
    params = {
        "fields": "comments.limit(100){from{id,name,link},message,created_time,like_count}",
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
        data = response.json()

        comments_raw = data.get("comments", {}).get("data", [])

        if not comments_raw:
            return 0  # No comments found

        comments = [{"comment_message": c.get("message", "")} for c in comments_raw]

        df = pd.DataFrame(comments)

        # --- File Saving Logic ---
        BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Adjusted to current file location
        DATA_DIR = os.path.join(BASE_DIR, "data")
        os.makedirs(DATA_DIR, exist_ok=True)  # Create the data directory if it doesn't exist

        file_path = os.path.join(DATA_DIR, "comment.xlsx")
        df.to_excel(file_path, index=False)

        print(f"Excel file saved as {file_path}")
        return len(comments)

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Facebook Graph API: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to scrape comments: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Facebook API response: {e}")
        raise HTTPException(status_code=500, detail="Error parsing data from Facebook.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    post_id: str

@app.post("/scrape")
def scrape_comments_endpoint(data: PostRequest):
    """
    API endpoint to trigger scraping of comments for a given post_id.
    """
    total_comments = scrape_facebook_comments(PAGE_ID, data.post_id, ACCESS_TOKEN)
    return {
        "message": "Comments scraped successfully",
        "total_comments": total_comments
    }

@app.get("/classify")
def get_classification(post_id: str):
    result = classify_comments()
    return {
        "postId": post_id,
        **result
    }
