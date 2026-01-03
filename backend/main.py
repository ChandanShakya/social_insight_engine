from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.controllers.classify import classify_comments
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def get_classification(post_id: str):
    rows = classify_comments()

    # Aggregate counts and comments by sentiment labels (POS/NEG/NEU)
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    comments = {"positive": [], "neutral": [], "negative": []}

    for row in rows:
        raw = str(row.get("sentiments", row.get("sentiment", "")).strip().upper())
        text = str(row.get("Comments", row.get("comment", "")))
        label = "neutral"
        if raw == "POS":
            label = "positive"
        elif raw == "NEG":
            label = "negative"
        elif raw == "NEU":
            label = "neutral"
        counts[label] += 1
        if text:
            comments[label].append(text)

    total = sum(counts.values())
    def round2(n: float) -> float:
        return round(n * 100) / 100.0

    percentages = {
        "positive": round2((counts["positive"] / total) * 100) if total else 0,
        "neutral": round2((counts["neutral"] / total) * 100) if total else 0,
        "negative": round2((counts["negative"] / total) * 100) if total else 0,
    }

    return {
        "message":"Sentiment classification completed",
        "data" : result
    }