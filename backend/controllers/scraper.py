import requests
import pandas as pd
import os
import json

page_id = "61585099347820"
post_id = "122098429155169978"
access_token = "EAAbDSoF1NBoBQYwjMOoidVPgAdJKrSaf8nVraH8rqaVW5dFyzhDIv6n3FTiAVim4J9zW8hMojZA2nwHj6950DWRXOtWdy1hwKQOd5NFDsYQ15uL097ZAuC0UPNhdSLe6l6XEIVecLqZBC9E7YUiZCBMZA2rZBKrnZBELZCHO1CIvhjzbGH7kuD3WIUF7mSfTntr5IHb9mOIR7JViuBRb1VQS"

url = f"https://graph.facebook.com/v18.0/{page_id}_{post_id}"

params = {
    "fields": "comments.limit(100){from{id,name,link},message,created_time,like_count}",
    "access_token": access_token
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=2))

comments_raw = data.get("comments", {}).get("data", [])

comments = []

for c in comments_raw:
    comments.append({
        "comment_message": c.get("message", ""),
    })

df = pd.DataFrame(comments)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes up to 'backend'
DATA_DIR = os.path.join(BASE_DIR, "data")  # points to 'backend\data'

file_path = os.path.join(DATA_DIR, "comment.xlsx")
df.to_excel(file_path, index=False)

print(f"Excel file saved as {file_path}")

print(f"Excel file saved as {file_path}")