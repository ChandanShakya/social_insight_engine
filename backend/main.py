#main api endpoint

from controllers.classify import classify_comments
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class PostRequest(BaseModel):
    post_id : str #for safe conversion

@app.post("/scrape")
def scrape_comments(data:PostRequest):
    print("Here goes the scraper code")

    return{
        "message" : "Comments scraped successfully",
        "total_comments" : 45
    }

@app.get("/classify")
def get_classification():
    result = classify_comments()

    return {
        "message":"Sentiment classification completed",
        "data" : result
    }