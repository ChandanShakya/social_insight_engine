# Social Insight Engine

Social Insight Engine is a comprehensive tool designed for analyzing social media engagement and sentiment. It enables users to scrape comments from Facebook posts, classify them using advanced Natural Language Processing (NLP), and generate actionable insights and recommendations based on the collective feedback.

## Features

- **Facebook Comment Scraping**: Fetch comments directly from Facebook posts using the Graph API (and an alternative Selenium-based scraper).
- **Sentiment Analysis**: Categorize comments into Positive, Neutral, and Negative sentiments using a BERT-based transformer model (`bertweet-base-sentiment-analysis`).
- **AI-Powered Insights**: Generate structured takeaways, success points, areas for improvement, and specific recommendations using Gemini AI.
- **Interactive Dashboard**: A modern React-based frontend featuring charts, sentiment breakdowns, and detailed comment lists.

## Project Structure

- `backend/`: FastAPI server handling data scraping, sentiment analysis, and AI generation.
- `Frontend/`: React (Vite + TypeScript) application for the user interface.
- `3_selenium.py`: Documentation/Alternative script for Selenium-based scraping.

## Quick Start (Windows)

For Windows users, you can start both the backend and frontend simultaneously using the provided batch script:

1.  Open the project root folder.
2.  Double-click `run_project.cmd`.
3.  The backend and frontend will open in separate terminal windows.

---

## Detailed Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- Facebook Graph API Access Token (for the primary scraper)
- Gemini API Key (for takeaway generation)

### 1. Setup & Run the Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r ../requirements.txt
    ```
3.  Configure your environment variables in a `.env` file (see `backend/.env` for required keys):
    ```env
    FB_PAGE_ID=your_page_id
    FB_ACCESS_TOKEN=your_access_token
    GEMINI_API_KEY=your_gemini_key
    ```
4.  Start the FastAPI server:
    ```bash
    python -m uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

### 2. Setup & Run the Frontend

1.  Navigate to the `Frontend` directory:
    ```bash
    cd Frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:5173`.

---

## How to Use

1.  Ensure both backend and frontend are running.
2.  Open the frontend in your browser.
3.  Enter a Facebook Post ID to scrape comments.
4.  Once scraping is complete, the dashboard will automatically display the sentiment analysis and AI-generated insights.
