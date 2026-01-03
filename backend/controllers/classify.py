from collections import defaultdict
import os
import pandas as pd
from transformers import pipeline
def classify_comments():
    sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

    base_dir = os.path.dirname(__file__)
    file_path = os.path.abspath(
        os.path.join(base_dir, "..", "data", "comment.xlsx")
    )

    df = pd.read_excel(file_path)

    LABEL_MAP = {"POS": "positive", "NEG": "negative", "NEU": "neutral"}

    grouped_comments = defaultdict(list)

    for comment in df["Comments"]:
        result = sentiment_pipeline(comment)[0]
        label = LABEL_MAP[result["label"]]
        grouped_comments[label].append(comment)

    total = sum(len(v) for v in grouped_comments.values())

    counts = {
        "positive": len(grouped_comments["positive"]),
        "neutral": len(grouped_comments["neutral"]),
        "negative": len(grouped_comments["negative"])
    }

    percentages = {
        k: round((v / total) * 100, 2) if total > 0 else 0
        for k, v in counts.items()
    }

    return {
        "total": total,
        "counts": counts,
        "percentages": percentages,
        "comments": grouped_comments
    }
