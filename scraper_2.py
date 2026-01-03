import requests
import re
import pandas as pd
from datetime import datetime

# Your credentials
PAGE_ID = "61585099347820"
ACCESS_TOKEN = "EAAbDSoF1NBoBQYwjMOoidVPgAdJKrSaf8nVraH8rqaVW5dFyzhDIv6n3FTiAVim4J9zW8hMojZA2nwHj6950DWRXOtWdy1hwKQOd5NFDsYQ15uL097ZAuC0UPNhdSLe6l6XEIVecLqZBC9E7YUiZCBMZA2rZBKrnZBELZCHO1CIvhjzbGH7kuD3WIUF7mSfTntr5IHb9mOIR7JViuBRb1VQS"
POST_ID = "122095625301169978"

# Create full post ID
FULL_POST_ID = f"{PAGE_ID}_{POST_ID}"

def extract_phone_numbers(text):
    """Extract phone numbers using regex patterns - FIXED to avoid duplicates"""
    if not text:
        return []
    
    # First, find ALL possible phone number matches with their positions
    all_matches = []
    
    # Pattern 1: 10-digit numbers
    pattern1 = r'\b\d{10}\b'
    for match in re.finditer(pattern1, text):
        phone = match.group()
        all_matches.append((match.start(), match.end(), phone))
    
    # Pattern 2: 3-3-4 format with separators
    pattern2 = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    for match in re.finditer(pattern2, text):
        phone = re.sub(r'[^\d]', '', match.group())  # Clean to digits only
        all_matches.append((match.start(), match.end(), phone))
    
    # Pattern 3: US format with country code
    pattern3 = r'\b\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    for match in re.finditer(pattern3, text):
        phone = re.sub(r'[^\d+]', '', match.group())  # Keep + if present
        all_matches.append((match.start(), match.end(), phone))
    
    # Remove duplicates by position overlap
    unique_phones = []
    seen_positions = []
    
    for start, end, phone in sorted(all_matches, key=lambda x: x[0]):  # Sort by start position
        # Check if this overlaps with a previously found number
        overlap = False
        for seen_start, seen_end in seen_positions:
            if not (end <= seen_start or start >= seen_end):  # If they overlap
                overlap = True
                break
        
        if not overlap:
            # Clean and validate the phone number
            cleaned = phone.lstrip('+')  # Remove leading + for comparison
            if len(cleaned) >= 10:
                # Format for consistency
                if len(cleaned) == 10:
                    formatted = f"{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
                else:
                    formatted = phone
                
                # Add to unique list if not already there
                if formatted not in unique_phones:
                    unique_phones.append(formatted)
                    seen_positions.append((start, end))
    
    return unique_phones

def extract_phone_numbers_simple(text):
    """Simpler version - find all 10+ digit sequences and deduplicate"""
    if not text:
        return []
    
    # Find all sequences of 10 or more consecutive digits
    digit_sequences = re.findall(r'\d{10,}', text)
    
    # Also find formatted numbers and clean them
    formatted_patterns = [
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # 3-3-4 format
        r'\d{4}[-.\s]?\d{3}[-.\s]?\d{3}',  # 4-3-3 format
        r'\d{5}[-.\s]?\d{5}',  # 5-5 format
    ]
    
    for pattern in formatted_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Extract only digits
            digits = re.sub(r'\D', '', match)
            if len(digits) >= 10:
                digit_sequences.append(digits)
    
    # Remove duplicates and format
    unique_phones = set()
    for digits in digit_sequences:
        # Take only first 10 digits if longer (ignore extra digits)
        if len(digits) >= 10:
            clean_number = digits[:10]  # Take first 10 digits
            # Format as XXX-XXX-XXXX
            formatted = f"{clean_number[:3]}-{clean_number[3:6]}-{clean_number[6:]}"
            unique_phones.add(formatted)
    
    return sorted(list(unique_phones))

def extract_phone_numbers_best(text):
    """Best version - comprehensive but avoids duplicates"""
    if not text:
        return []
    
    # Find all potential phone numbers
    patterns = [
        # International format (keep +)
        (r'\+\d{1,4}[-\s.]?\d{1,4}[-\s.]?\d{4,}', lambda x: x),
        
        # Standard US/Canada (clean and format)
        (r'\b\d{3}[-\s.]?\d{3}[-\s.]?\d{4}\b', 
         lambda x: f"{re.sub(r'\D', '', x)[:3]}-{re.sub(r'\D', '', x)[3:6]}-{re.sub(r'\D', '', x)[6:]}"),
        
        # With parentheses
        (r'\b\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}\b',
         lambda x: f"{re.sub(r'\D', '', x)[:3]}-{re.sub(r'\D', '', x)[3:6]}-{re.sub(r'\D', '', x)[6:]}"),
        
        # Plain 10-digit
        (r'\b\d{10}\b',
         lambda x: f"{x[:3]}-{x[3:6]}-{x[6:]}"),
    ]
    
    all_numbers = set()
    
    for pattern, formatter in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                formatted = formatter(match)
                # Validate it has exactly 10 digits (excluding dashes and +)
                digit_count = sum(c.isdigit() for c in formatted)
                if digit_count >= 10:
                    all_numbers.add(formatted)
            except:
                continue
    
    return sorted(list(all_numbers))

def scrape_all_comments():
    """Scrape ALL comments from the post"""
    
    url = f"https://graph.facebook.com/v18.0/{FULL_POST_ID}"
    params = {
        "fields": "comments.limit(500){from{id,name},message,created_time}",
        "access_token": ACCESS_TOKEN
    }
    
    print(f"📡 Requesting data from: {url}")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"❌ Facebook API Error: {data['error']}")
            return []
        
        comments_raw = data.get("comments", {}).get("data", [])
        print(f"✅ Found {len(comments_raw)} total comments")
        
        all_comments = []
        
        for i, comment in enumerate(comments_raw, 1):
            message = comment.get("message", "")
            phone_numbers = extract_phone_numbers_best(message)
            
            # Debug: Print if duplicates were found
            if phone_numbers and len(phone_numbers) > len(set([p.replace('-', '') for p in phone_numbers])):
                print(f"   ⚠️ Comment {i}: Found potential duplicates in: {message[:50]}...")
            
            # Create comment data for ALL comments
            comment_data = {
                "Name": comment.get("from", {}).get("name", "Unknown"),
                "User_ID": comment.get("from", {}).get("id", ""),
                "Profile_URL": f"https://facebook.com/{comment.get('from', {}).get('id', '')}",
                "Phone_Numbers": ", ".join(phone_numbers) if phone_numbers else "",
                "Has_Phone": "Yes" if phone_numbers else "No",
                "Phone_Count": len(phone_numbers),
                "Comment": message,
                "Timestamp": comment.get("created_time", ""),
                "Comment_ID": comment.get("id", "")
            }
            
            # Add to ALL comments list
            all_comments.append(comment_data)
            
            # Progress indicator
            if i % 50 == 0:
                print(f"   Processed {i} comments...")
        
        return all_comments
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# Run the scraper
print("=" * 60)
print("📱 FACEBOOK COMMENT SCRAPER (NO DUPLICATES)")
print("=" * 60)

all_comments = scrape_all_comments()

if all_comments:
    # Create DataFrame
    df = pd.DataFrame(all_comments)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"facebook_comments_{timestamp}.csv"
    
    # Export to CSV
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ SUCCESS!")
    print(f"📁 File saved: {csv_filename}")
    print(f"📊 Total comments: {len(all_comments)}")
    
    # Calculate statistics
    comments_with_phones = sum(1 for c in all_comments if c['Phone_Numbers'])
    total_phones = sum(c['Phone_Count'] for c in all_comments)
    
    print(f"📱 Comments with phone numbers: {comments_with_phones}")
    print(f"🔢 Total UNIQUE phone numbers found: {total_phones}")
    
    if all_comments:
        percentage = (comments_with_phones / len(all_comments)) * 100
        print(f"📈 Percentage with phones: {percentage:.1f}%")
        
        if comments_with_phones > 0:
            avg_phones = total_phones / comments_with_phones
            print(f"📊 Average phones per comment: {avg_phones:.1f}")
    
    # Show sample of comments with phones
    print(f"\n📋 SAMPLE OF COMMENTS WITH PHONE NUMBERS:")
    print("-" * 80)
    
    phone_comments = [c for c in all_comments if c['Phone_Numbers']]
    if phone_comments:
        for i, comment in enumerate(phone_comments[:5], 1):
            print(f"{i}. {comment['Name']}")
            print(f"   📞 {comment['Phone_Numbers']}")
            print(f"   💬 {comment['Comment'][:60]}...")
            print()
    else:
        print("No phone numbers found in any comments.")
    
    print("=" * 60)
    print("🎉 DONE! Check your CSV file for all data.")
    print("=" * 60)
    
    # Show first few rows of CSV
    print(f"\n📄 FIRST 5 ROWS OF CSV:")
    print(df.head().to_string(index=False))
    
else:
    print("\n❌ No comments found in this post")