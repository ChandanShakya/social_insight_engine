from collections import defaultdict
import os
import pandas as pd
from transformers import pipeline
from .takeaway_generation import extract_combined_takeaways

# Cache the pipeline globally to avoid reloading on every request
_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        # Loading model once
        _sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    return _sentiment_pipeline

def classify_comments():
    sentiment_pipeline = get_sentiment_pipeline()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(
        os.path.join(base_dir, "..", "data", "comment.xlsx")
    )

    if not os.path.exists(file_path):
        return {
            "total": 0,
            "counts": {"positive": 0, "neutral": 0, "negative": 0},
            "percentages": {"positive": 0, "neutral": 0, "negative": 0},
            "comments": {"positive": [], "neutral": [], "negative": []},
            "takeaways": {"positive": [], "negative": []}
        }

    df = pd.read_excel(file_path)
    
    if df.empty or "Comments" not in df.columns:
        return {
            "total": 0,
            "counts": {"positive": 0, "neutral": 0, "negative": 0},
            "percentages": {"positive": 0, "neutral": 0, "negative": 0},
            "comments": {"positive": [], "neutral": [], "negative": []},
            "takeaways": {"positive": [], "negative": []}
        }

    LABEL_MAP = {"POS": "positive", "NEG": "negative", "NEU": "neutral"}
    grouped_comments = defaultdict(list)

    # Batch Process Sentiment Analysis - significant speed boost
    comment_list = df["Comments"].astype(str).tolist()
    
    # Run in batches of 16 (default) for efficiency
    results = sentiment_pipeline(comment_list)

    for comment, result in zip(comment_list, results):
        label = LABEL_MAP[result["label"]]
        grouped_comments[label].append(comment)

    total = len(comment_list)

    counts = {
        "positive": len(grouped_comments["positive"]),
        "neutral": len(grouped_comments["neutral"]),
        "negative": len(grouped_comments["negative"])
    }

    percentages = {
        k: round((v / total) * 100, 2) if total > 0 else 0
        for k, v in counts.items()
    }

    # Use combined call to Gemini for faster response
    takeaways = extract_combined_takeaways(
        grouped_comments["positive"], 
        grouped_comments["negative"]
    )

    return {
        "total": total,
        "counts": counts,
        "percentages": percentages,
        "comments": grouped_comments,
        "takeaways" : takeaways,
    }

