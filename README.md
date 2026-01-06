# Social Insight Engine

> 🏆 **Winner - NCCS Business Hackathon 2026**  
> *Held January 2nd - 4th, 2026*

---

A comprehensive social media sentiment analysis platform that scrapes Facebook comments, analyzes sentiment using BERT, and generates AI-powered insights with Google Gemini. Built for businesses to understand customer feedback at scale.

## 🏆 Achievement

**NCCS Business Hackathon 2026 - Winner**  
This project won the prestigious NCCS Business Hackathon held from January 2nd to 4th, 2026, demonstrating excellence in:
- Real-world business problem solving
- AI/ML integration
- Scalable architecture
- User-friendly interface
- Innovation in social media analytics

## 📁 Project Structure

```
social_insight_engine/
├── backend/                    # FastAPI backend server
│   ├── controllers/           # API controllers
│   │   ├── classify.py        # Sentiment analysis (BERT)
│   │   ├── scraper.py         # Facebook Graph API scraper
│   │   ├── takeaway_generation.py  # Gemini AI insights
│   │   └── __init__.py
│   ├── scrapers/              # Alternative scrapers
│   │   ├── selenium_scraper.py  # Selenium-based scraper
│   │   └── __init__.py
│   ├── data/                  # Scraped data storage
│   ├── main.py                # FastAPI application entry
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API keys (create from .env.example)
│   ├── README.md              # Backend documentation
│   ├── setup.sh               # Unix setup script
│   └── start.sh               # Unix start script
├── Frontend/                  # React + TypeScript frontend
│   ├── src/
│   │   ├── services/          # API services
│   │   │   ├── sentimentService.ts
│   │   │   └── themeService.tsx
│   │   ├── types.ts           # TypeScript definitions
│   │   ├── App.tsx            # Main React component
│   │   ├── main.tsx           # React entry point
│   │   └── index.css          # Tailwind CSS
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── README.md              # Frontend documentation
│   └── start.sh               # Unix start script
├── docs/                      # Documentation
│   └── Social Insight Engine.postman_collection.json
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── run_project.cmd           # Windows batch launcher
└── start.sh                  # Master start script (Unix)
```

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.8+
- **Node.js**: 18+
- **Facebook Graph API**: Credentials (Page ID & Access Token)
- **Google Gemini API**: API key

### Option 1: Master Script (Linux/Mac) - Recommended

```bash
./start.sh
```

This automated script handles:
1. ✅ Prerequisites verification
2. ✅ Backend virtual environment setup
3. ✅ Python dependency installation
4. ✅ Node.js dependency installation
5. ✅ Server startup (backend + frontend)
6. ✅ Browser auto-launch

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env file with your API keys
./start.sh  # or: python -m uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd Frontend
npm install
npm run dev
```

### Option 3: Windows
Double-click `run_project.cmd` for one-click startup.

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `backend/.env` and configure:

```env
# Facebook Graph API
FB_PAGE_ID=your_page_id_here
FB_ACCESS_TOKEN=your_access_token_here
FB_API_VERSION=v24.0

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
```

### How to Get API Keys

#### 1. Facebook Graph API
1. Visit [Facebook Developers](https://developers.facebook.com/)
2. Create a Meta App
3. Get **Page ID** from your Facebook Page
4. Generate **Access Token** with permissions:
   - `pages_read_engagement`
   - `pages_read_user_content`

#### 2. Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key (starts with "AIza")

## 🌐 Access URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React Dashboard |
| Backend API | http://localhost:8000 | FastAPI Server |
| API Docs | http://localhost:8000/docs | Interactive Swagger UI |
| API Redoc | http://localhost:8000/redoc | Alternative API Documentation |

## 📊 Features

### Backend API Endpoints
- `POST /scrape` - Scrape Facebook comments from a post
- `GET /classify` - Analyze sentiment of scraped comments
- `GET /posts` - Fetch recent posts from Facebook page
- `GET /health` - Health check endpoint

### Frontend Dashboard
- **Settings Panel**: Configure API credentials with localStorage persistence
- **Post Selection**: Choose from recent posts or manually enter post ID
- **Sentiment Dashboard**: 
  - 📊 Pie chart for sentiment distribution
  - 📈 Bar chart for sentiment scale analysis
  - 🎯 Statistics cards (Positive/Neutral/Negative counts)
- **AI Insights**: 
  - Positive takeaways and recommendations
  - Negative concerns and improvement areas
- **Comment Browser**: 
  - Filter by sentiment (All/Positive/Neutral/Negative)
  - Pagination for large datasets
- **Search History**: 
  - Save previous analyses
  - Load historical data instantly
- **Theme Toggle**: Dark/Light mode with smooth transitions

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance web framework |
| **Uvicorn** | ASGI server |
| **Transformers** | BERTweet sentiment analysis |
| **PyTorch** | ML framework |
| **Google Gemini** | AI insights generation |
| **Pandas** | Data manipulation |
| **Pydantic** | Data validation |
| **python-dotenv** | Environment management |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **TypeScript** | Type safety |
| **Vite** | Build tool & dev server |
| **Tailwind CSS 4** | Utility-first styling |
| **Recharts** | Data visualization |
| **Lucide React** | Icon library |
| **clsx/tailwind-merge** | Class management |

## 📚 Documentation

- **Backend**: See `backend/README.md` for detailed API documentation
- **Frontend**: See `Frontend/README.md` for component architecture
- **API Collection**: `docs/Social Insight Engine.postman_collection.json`

## 🔧 Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
cd backend
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### Port Conflicts
```bash
# Backend (change port 8000 → 8001)
uvicorn main:app --port 8001

# Frontend (change port 5173 → 5174)
npm run dev -- --port 5174
```

### Model Download
- **First Run**: Downloads BERT model (~500MB)
- **Subsequent Runs**: Uses cached model (fast)

### CORS Issues
Already configured for:
- `http://localhost:5173` (Frontend)
- `http://localhost:3000` (Alternative)

## 🏆 Hackathon Highlights

**NCCS Business Hackathon 2026** - January 2-4, 2026

### Why This Project Won
1. **Real Business Impact**: Solves actual social media monitoring challenges
2. **AI-Powered**: Leverages cutting-edge BERT and Gemini models
3. **User-Friendly**: Intuitive dashboard for non-technical users
4. **Scalable Architecture**: Ready for production deployment
5. **Innovation**: Combines multiple APIs and ML models seamlessly

### Key Judging Criteria Met
- ✅ Innovation & Creativity
- ✅ Technical Complexity
- ✅ Business Viability
- ✅ User Experience
- ✅ Presentation & Documentation

## 📝 License

MIT License - Free to use and modify for personal or commercial projects.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

**Built with ❤️ for social media analysis**  
**Winner - NCCS Business Hackathon 2026** 🏆