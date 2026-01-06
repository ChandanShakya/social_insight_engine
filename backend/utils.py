"""
Common utilities and configurations for the Social Insight Engine backend.
"""
import os
import logging
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    
    def __init__(self):
        self.fb_page_id = os.getenv("FB_PAGE_ID")
        self.fb_access_token = os.getenv("FB_ACCESS_TOKEN")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.fb_api_version = os.getenv("FB_API_VERSION", "v24.0")
    
    def validate_fb_credentials(self) -> tuple[str, str]:
        if not self.fb_page_id or not self.fb_access_token:
            raise ValueError("Facebook credentials not configured. Check FB_PAGE_ID and FB_ACCESS_TOKEN.")
        return self.fb_page_id, self.fb_access_token
    
    def validate_gemini_credentials(self) -> str:
        if not self.gemini_api_key:
            raise ValueError("Gemini API key not configured. Check GEMINI_API_KEY.")
        return self.gemini_api_key

class DataPaths:
    
    def __init__(self):
        self.backend_dir = Path(__file__).parent
        self.data_dir = self.backend_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def get_comments_file(self) -> Path:
        return self.data_dir / "comment.xlsx"

class ErrorHandler:
    
    @staticmethod
    def handle_request_error(e: Exception, operation: str) -> None:
        logger.error(f"Request error in {operation}: {e}", exc_info=True)
    
    @staticmethod
    def handle_data_error(e: Exception, operation: str) -> None:
        logger.error(f"Data error in {operation}: {e}", exc_info=True)
    
    @staticmethod
    def handle_file_error(e: Exception, operation: str) -> None:
        logger.error(f"File error in {operation}: {e}", exc_info=True)

class DataFrameOperations:
    
    @staticmethod
    def save_comments_to_excel(comments: list[dict[str, str]], file_path: Path) -> int:
        if not comments:
            return 0
        
        try:
            df = pd.DataFrame(comments)
            df.to_excel(file_path, index=False)
            logger.info(f"Excel file saved as {file_path}")
            return len(comments)
        except Exception as e:
            ErrorHandler.handle_file_error(e, "save_comments_to_excel")
            raise
    
    @staticmethod
    def load_comments_from_excel(file_path: Path) -> pd.DataFrame:
        if not file_path.exists():
            return pd.DataFrame()
        
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            ErrorHandler.handle_file_error(e, "load_comments_from_excel")
            raise

class FacebookAPIClient:
    
    def __init__(self, page_id: str, access_token: str, api_version: str = "v24.0"):
        self.page_id = page_id
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{api_version}"
    
    def build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"
    
    def get_posts(self, limit: int = 20) -> Dict[str, Any]:
        import requests
        
        url = self.build_url(f"{self.page_id}/posts")
        params = {
            "fields": "id,message,created_time,permalink_url",
            "access_token": self.access_token,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle_request_error(e, "get_posts")
            raise
    
    def get_post_comments(self, post_id: str, limit: int = 100) -> Dict[str, Any]:
        import requests
        
        url = self.build_url(f"{self.page_id}_{post_id}")
        params = {
            "fields": f"comments.limit({limit}){{from{{id,name,link}},message,created_time,like_count}}",
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle_request_error(e, "get_post_comments")
            raise
    
    def extract_comments_from_response(self, data: Dict[str, Any]) -> list[dict[str, str]]:
        comments_raw = data.get("comments", {}).get("data", [])
        return [{"Comments": c.get("message", "")} for c in comments_raw]

config = Config()
data_paths = DataPaths()