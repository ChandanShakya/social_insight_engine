import requests
import json
import pandas as pd

# page_id = "61585099347820      "
# post_id = "122095625301169978 " 122098429155169978

# access_token = 'EAAVbJc3wOpYBQABzlUCMdhiCH1ZBj0lT3vrhaxAIxgdC6cuObTZBJSHCrF58D0b2uGYD5qAzTSLa3rsRieL0hLFmusg0yL07fkM0jbqigH1TgpqsYG8NuelEDujFbi8gLL7sZBkwmqZCPQcFbZAW5S3rtZBOmWkYLdayfX8vWEZBz7NqVhwYTZA82GpLRw6xie1eVXZBaB2DPX92CArw5'

# url = f'https://graph.facebook.com/v17.0/{page_id}_{post_id}?fields=created_time,message,comments{{from,message,created_time,like_count}},reactions.summary(total_count)&access_token={access_token}'

# response = requests.get(url)
# data = response.json()


# def parse_post(comment):
#     return {
#         'commenter_name': comment['from']['name'],
#         'comment_message': comment.get('message', ''),
#         'comment_created_time': comment.get('created_time', ''),
#         'comment_like_count': comment.get('like_count', 0)
#     }


# # Check if comments exist
# comments_raw = data.get('comments', {}).get('data', [])

# # Parse all comments
# comments = list(map(parse_post, comments_raw))

# # Export to Excel
# df = pd.DataFrame(comments)
# df.to_excel("comments.xlsx", index=False)

# print("Excel file saved as comments.xlsx")



# Working version  
import requests
import pandas as pd

# page_id = "61585099347820"
# post_id =  "122095625301169978"
# access_token = "EAAbDSoF1NBoBQYwjMOoidVPgAdJKrSaf8nVraH8rqaVW5dFyzhDIv6n3FTiAVim4J9zW8hMojZA2nwHj6950DWRXOtWdy1hwKQOd5NFDsYQ15uL097ZAuC0UPNhdSLe6l6XEIVecLqZBC9E7YUiZCBMZA2rZBKrnZBELZCHO1CIvhjzbGH7kuD3WIUF7mSfTntr5IHb9mOIR7JViuBRb1VQS"

# url = f"https://graph.facebook.com/v17.0/{page_id}_{post_id}"
# params = {
#     "fields": "comments{from,message,created_time,like_count}",
#     "access_token": access_token
# }

# response = requests.get(url, params=params)
# data = response.json()

# comments_raw = data.get("comments", {}).get("data", [])

# comments = []

# for c in comments_raw:
#     comments.append({
#         "commenter_name": c.get("from", {}).get("name", "Unknown"),
#         "comment_message": c.get("message", ""),
#         "comment_created_time": c.get("created_time", ""),
#         "comment_like_count": c.get("like_count", 0)
#     })

# df = pd.DataFrame(comments)
# df.to_excel("comments1.xlsx", index=False)

# print("Excel file saved as comments1.xlsx")

import requests
import pandas as pd

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
import json
print(json.dumps(response.json(), indent=2))

comments_raw = data.get("comments", {}).get("data", [])

comments = []

for c in comments_raw:
    from_obj = c.get("from", {})

    comments.append({
        "commenter_name": from_obj.get("name", "Not Available"),
        "commenter_id": from_obj.get("id", ""),
        "commenter_profile_url": from_obj.get("link", "Not Available"),
        "comment_message": c.get("message", ""),
        "comment_created_time": c.get("created_time", ""),
        "comment_like_count": c.get("like_count", 0)
    })

df = pd.DataFrame(comments)
df.to_excel("facebook_comments4.xlsx", index=False)

print("Excel file saved as facebook_comments2.xlsx")
