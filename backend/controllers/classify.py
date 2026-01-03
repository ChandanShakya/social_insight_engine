import pandas as pd
from transformers import pipeline

#loading the model as a pipeline
#here the first parameter is the able_task that defines what the model is capable of


sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

def classify_comments():
    df = pd.read_excel("comments.xlsx")

    sentiments = []

    for comment in df["Comments"]:
        result = sentiment_pipeline(comment)[0]
        sentiments.append(result["label"])

    df["sentiments"] = sentiments

    df.to_excel("comments.xlsx",index = False)
    return df

def main():
    result = classify_comments()

if __name__ == "__main__":
    main()

