import requests
import re
import pandas as pd
from datetime import datetime


### this code only store the coment with has the number phone ###


# Your credentials
PAGE_ID = "61585099347820"
ACCESS_TOKEN = "EAAbDSoF1NBoBQYwjMOoidVPgAdJKrSaf8nVraH8rqaVW5dFyzhDIv6n3FTiAVim4J9zW8hMojZA2nwHj6950DWRXOtWdy1hwKQOd5NFDsYQ15uL097ZAuC0UPNhdSLe6l6XEIVecLqZBC9E7YUiZCBMZA2rZBKrnZBELZCHO1CIvhjzbGH7kuD3WIUF7mSfTntr5IHb9mOIR7JViuBRb1VQS"
POST_ID = "122095625301169978"

# Create full post ID
FULL_POST_ID = f"{PAGE_ID}_{POST_ID}"

def extract_phone_numbers(text):
    """Extract phone numbers using regex patterns"""
    if not text:
        return []
    
    patterns = [
        r'\b\d{10}\b',
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        r'\b\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    ]
    
    phone_numbers = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            cleaned = re.sub(r'[^\d+]', '', match)
            if len(cleaned) >= 10:
                phone_numbers.add(cleaned)
    
    return list(phone_numbers)

def scrape_comments():
    """Simple scraper matching your working code pattern"""
    
    url = f"https://graph.facebook.com/v18.0/{FULL_POST_ID}"
    params = {
        "fields": "comments.limit(500){from{id,name},message,created_time}",
        "access_token": ACCESS_TOKEN
    }
    
    print(f"Requesting: {url}")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"Facebook API Error: {data['error']}")
            return []
        
        comments_raw = data.get("comments", {}).get("data", [])
        print(f"Found {len(comments_raw)} total comments")
        
        comments_with_phones = []
        
        for comment in comments_raw:
            message = comment.get("message", "")
            phone_numbers = extract_phone_numbers(message)
            
            if phone_numbers:
                comments_with_phones.append({
                    "commenter_name": comment.get("from", {}).get("name", "Unknown"),
                    "commenter_id": comment.get("from", {}).get("id", ""),
                    "profile_url": f"https://facebook.com/{comment.get('from', {}).get('id', '')}",
                    "phone_numbers": ", ".join(phone_numbers),
                    "message": message[:200],  # First 200 chars
                    "created_time": comment.get("created_time", "")
                })
        
        return comments_with_phones
        
    except Exception as e:
        print(f"Error: {e}")
        return []

# Run the scraper
print("Starting Facebook comment scraper...")
data = scrape_comments()

if data:
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Export to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"facebook_phones_{timestamp}.csv"
    df.to_csv(csv_filename, index=False)
    
    # Export to Excel
    excel_filename = f"facebook_phones_{timestamp}.xlsx"
    df.to_excel(excel_filename, index=False)
    
    print(f"✅ Success! Found {len(data)} comments with phone numbers")
    print(f"📁 CSV saved as: {csv_filename}")
    print(f"📁 Excel saved as: {excel_filename}")
    
    # Show preview
    print("\n📋 Preview:")
    print(df[['commenter_name', 'phone_numbers']].head())
    
else:
    print("❌ No phone numbers found in comments")