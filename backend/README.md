# Backend - Social Insight Engine

> 🏆 **NCCS Business Hackathon 2026 Winner** - Backend Component

---

FastAPI backend server for social media sentiment analysis with BERT and Google Gemini integration.

## 📁 Project Structure

```
backend/
├── controllers/               # API controllers
│   ├── classify.py           # Sentiment analysis (BERTweet)
│   ├── scraper.py            # Facebook Graph API scraper
│   └── takeaway_generation.py  # Gemini AI insights
├── scrapers/                 # Alternative scrapers
│   └── selenium_scraper.py   # Selenium-based fallback
├── data/                     # Scraped data storage (JSON/Excel)
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example              # Template for .env
├── setup.sh                  # Unix setup script
├── start.sh                  # Unix start server script
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
# Automated setup
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
Create `backend/.env` file:
```env
# Facebook Graph API
FB_PAGE_ID=your_page_id_here
FB_ACCESS_TOKEN=your_access_token_here
FB_API_VERSION=v24.0

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
MAX_COMMENTS=1000
SAVE_DATA=true
```

### 3. Run Server
```bash
# Using startup script
./start.sh

# Manual startup
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📊 API Endpoints

### Core Endpoints

#### 1. Scrape Facebook Comments
```http
POST /scrape
Content-Type: application/json

{
  "post_id": "123456789",
  "max_comments": 100
}
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "id": "comment_1",
      "message": "Great product!",
      "created_time": "2024-01-01T12:00:00Z",
      "from": "User Name"
    }
  ],
  "count": 50
}
```

#### 2. Analyze Sentiment
```http
GET /classify?comments=50
```

**Response**:
```json
{
  "status": "success",
  "results": {
    "positive": 35,
    "neutral": 10,
    "negative": 5
  },
  "details": [
    {
      "comment": "Great product!",
      "sentiment": "positive",
      "confidence": 0.95
    }
  ]
}
```

#### 3. Get Recent Posts
```http
GET /posts?limit=10
```

**Response**:
```json
{
  "status": "success",
  "posts": [
    {
      "id": "123456789",
      "message": "New product launch!",
      "created_time": "2024-01-01T10:00:00Z",
      "comments_count": 150
    }
  ]
}
```

#### 4. Generate AI Insights
```http
POST /insights
Content-Type: application/json

{
  "comments": [...],
  "sentiment_results": {...}
}
```

**Response**:
```json
{
  "status": "success",
  "insights": {
    "positive_takeaways": [
      "Customers love the product quality",
      "Fast delivery appreciated"
    ],
    "negative_takeaways": [
      "Packaging needs improvement",
      "Price point concerns"
    ],
    "recommendations": [
      "Enhance packaging design",
      "Consider loyalty program"
    ]
  }
}
```

#### 5. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "services": {
    "facebook": "connected",
    "gemini": "available",
    "bert": "loaded"
  }
}
```

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104+ | Web framework |
| **Uvicorn** | 0.24+ | ASGI server |
| **Transformers** | 4.35+ | BERT sentiment analysis |
| **PyTorch** | 2.1+ | ML framework |
| **Pandas** | 2.1+ | Data manipulation |
| **Openpyxl** | 3.1+ | Excel export |
| **Pydantic** | 2.5+ | Data validation |
| **python-dotenv** | 1.0+ | Environment management |
| **Requests** | 2.31+ | HTTP client |
| **Selenium** | 4.15+ | Alternative scraper |

## 🧠 ML Models

### BERTweet Sentiment Analysis
- **Model**: `finiteautomata/bertweet-base-sentiment-analysis`
- **Purpose**: Classify comments as positive/neutral/negative
- **Download**: Auto-downloaded on first run (~500MB)
- **Cache**: Stored in `~/.cache/huggingface/`

### Google Gemini Integration
- **Model**: Gemini Pro
- **Purpose**: Generate actionable insights from sentiment data
- **Rate Limits**: Check Google AI Studio quotas

## 📂 Controllers

### classify.py
Sentiment analysis using BERTweet:
```python
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="finiteautomata/bertweet-base-sentiment-analysis"
)

results = classifier(comments)
```

### scraper.py
Facebook Graph API integration:
```python
import requests

def scrape_facebook_comments(post_id, access_token):
    url = f"https://graph.facebook.com/v24.0/{post_id}/comments"
    params = {"access_token": access_token, "limit": 100}
    response = requests.get(url, params=params)
    return response.json()
```

### takeaway_generation.py
Gemini AI insights:
```python
import google.generativeai as genai

def generate_insights(comments, sentiment_data):
    prompt = f"Analyze these comments: {comments}..."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text
```

## 🔧 Configuration

### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| `FB_PAGE_ID` | ✅ | Facebook Page ID |
| `FB_ACCESS_TOKEN` | ✅ | Facebook Access Token |
| `GEMINI_API_KEY` | ✅ | Google Gemini API Key |
| `FB_API_VERSION` | ❌ | API Version (default: v24.0) |
| `MAX_COMMENTS` | ❌ | Max comments to scrape (default: 1000) |
| `SAVE_DATA` | ❌ | Save scraped data (default: true) |

### Data Storage
- **Location**: `backend/data/`
- **Format**: JSON and Excel files
- **Naming**: `scraped_{post_id}_{timestamp}.json`
- **Retention**: Manual cleanup required

## 🔄 Workflow

```
1. User sends POST /scrape with post_id
   ↓
2. scraper.py fetches comments from Facebook API
   ↓
3. Data saved to backend/data/
   ↓
4. User sends GET /classify
   ↓
5. classify.py runs BERT analysis
   ↓
6. Results returned with sentiment counts
   ↓
7. User sends POST /insights
   ↓
8. takeaway_generation.py queries Gemini
   ↓
9. AI insights returned
```

## 🔧 Scripts

### setup.sh
```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete! Create .env file next."
```

### start.sh
```bash
#!/bin/bash
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📦 Dependencies

### Core
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
```

### ML/NLP
```
torch==2.1.0
transformers==4.35.0
```

### Data Processing
```
pandas==2.1.3
openpyxl==3.1.2
```

### Optional (Selenium)
```
selenium==4.15.2
webdriver-manager==4.0.1
```

## 🐛 Troubleshooting

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### BERT Model Download Issues
```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/transformers/
# Run classification again
```

### Facebook API Errors
- Check `FB_ACCESS_TOKEN` is valid and not expired
- Verify `FB_PAGE_ID` is correct
- Ensure permissions: `pages_read_engagement`, `pages_read_user_content`

### Gemini API Errors
- Verify `GEMINI_API_KEY` is valid
- Check quota limits in Google AI Studio
- Ensure API is enabled for your account

### CORS Issues
Already configured for:
- `http://localhost:5173` (Frontend)
- `http://localhost:3000` (Alternative)

## 📊 Performance

### Benchmarks
- **Scraping**: ~100 comments/second
- **Sentiment Analysis**: ~50 comments/second (CPU)
- **Gemini API**: ~2-3 seconds per request
- **Total Pipeline**: ~5-10 seconds for 100 comments

### Optimization Tips
- Use GPU for faster BERT inference
- Cache model loading
- Batch process comments
- Use async requests for scraping

## 🔒 Security

### Best Practices
- ✅ Never commit `.env` file
- ✅ Use environment-specific API keys
- ✅ Validate all user inputs
- ✅ Rate limit API endpoints (optional)
- ✅ Store sensitive data in environment variables

## 📝 License

MIT License - Free to use and modify.

---

**Part of NCCS Business Hackathon 2026 Winning Project** 🏆