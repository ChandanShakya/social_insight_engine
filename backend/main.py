from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.classify import classify_comments
from pydantic import BaseModel

app = FastAPI()

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
def scrape_comments(data: PostRequest):
    return {
        "message": "Comments scraped successfully",
        "total_comments": 45
    }

@app.get("/classify")
def get_classification(post_id: str):
    result = classify_comments()
    return {
        "postId": post_id,
        **result
    }
