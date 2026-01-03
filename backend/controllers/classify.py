import pandas as pd
from transformers import pipeline
import os
#loading the model as a pipeline
#here the first parameter is the able_task that defines what the model is capable of


sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

def classify_comments():
    base_name = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.abspath(os.path.join(base_name,"..","data","comments.xlsx"))
    df = pd.read_excel(file_name)

    sentiments = []

    for comment in df["Comments"]:
        result = sentiment_pipeline(comment)[0]
        sentiments.append(result["label"])

    df["sentiments"] = sentiments

    df.to_excel(file_name,index = False)
    return df.to_dict(orient = "records")

def main():
    result = classify_comments()

if __name__ == "__main__":
    main()

