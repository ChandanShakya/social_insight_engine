from collections import defaultdict
import os
import pandas as pd
from transformers import pipeline
from services.takeaway_generation import extract_combined_takeaways
from utils import DataFrameOperations, data_paths

_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    return _sentiment_pipeline

def classify_comments(gemini_api_key: str = None, comments_data: list[dict] = None):
    """
    Classify comments for sentiment analysis.
    
    Args:
        gemini_api_key: API key for Gemini insights
        comments_data: Optional list of comment dictionaries in-memory. 
                      If None, reads from Excel file (backward compatibility).
    """
    sentiment_pipeline = get_sentiment_pipeline()

    if comments_data is not None:
        df = pd.DataFrame(comments_data)
    else:
        file_path = data_paths.get_comments_file()
        if not os.path.exists(file_path):
            return {
                "total": 0,
                "counts": {"positive": 0, "neutral": 0, "negative": 0},
                "percentages": {"positive": 0, "neutral": 0, "negative": 0},
                "comments": {"positive": [], "neutral": [], "negative": []},
                "takeaways": {"positive": [], "negative": []}
            }
        df = DataFrameOperations.load_comments_from_excel(file_path)

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

    comment_list = df["Comments"].astype(str).tolist()
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

    takeaways = extract_combined_takeaways(
        grouped_comments["positive"],
        grouped_comments["negative"],
        api_key=gemini_api_key
    )

    return {
        "total": total,
        "counts": counts,
        "percentages": percentages,
        "comments": grouped_comments,
        "takeaways": takeaways,
    }