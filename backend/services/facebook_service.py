"""Facebook service for handling Graph API operations and data processing."""
import requests
import pandas as pd
from typing import Dict, Any, List
from utils import config, data_paths, logger, ErrorHandler, DataFrameOperations


class FacebookService:
    """Consolidated service for all Facebook-related operations."""
    
    def __init__(self):
        self.page_id, self.access_token = config.validate_fb_credentials()
        self.api_version = config.fb_api_version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    def get_recent_posts(self, limit: int = 20) -> Dict[str, Any]:
        """Fetch recent posts from Facebook page."""
        url = f"{self.base_url}/{self.page_id}/posts"
        params = {
            "fields": "id,message,created_time,permalink_url",
            "access_token": self.access_token,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for post in data.get("data", []):
                post_id_full = post.get("id", "")
                post_id = post_id_full.split("_")[1] if "_" in post_id_full else post_id_full
                
                posts.append({
                    "id": post_id,
                    "message": post.get("message", "")[:100],
                    "created_time": post.get("created_time", ""),
                    "permalink_url": post.get("permalink_url", "")
                })
            
            return {
                "posts": posts,
                "total": len(posts),
                "paging": data.get("paging", {})
            }
            
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle_request_error(e, "get_recent_posts")
            raise
    
    def scrape_comments(self, post_id: str) -> int:
        """Scrape comments for a specific post and save to Excel."""
        url = f"{self.base_url}/{self.page_id}_{post_id}"
        params = {
            "fields": "comments.limit(100){from{id,name,link},message,created_time,like_count}",
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            comments_raw = data.get("comments", {}).get("data", [])
            if not comments_raw:
                return 0
            
            comments = [{"Comments": c.get("message", "")} for c in comments_raw]
            
            # Save to Excel using utility
            file_path = data_paths.get_comments_file()
            return DataFrameOperations.save_comments_to_excel(comments, file_path)
            
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle_request_error(e, "scrape_comments")
            raise
    
    def scrape_comments_in_memory(self, post_id: str) -> List[Dict[str, str]]:
        """Scrape comments and return in-memory (no file I/O)."""
        url = f"{self.base_url}/{self.page_id}_{post_id}"
        params = {
            "fields": "comments.limit(100){from{id,name,link},message,created_time,like_count}",
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            comments_raw = data.get("comments", {}).get("data", [])
            return [{"Comments": c.get("message", "")} for c in comments_raw]
            
        except requests.exceptions.RequestException as e:
            ErrorHandler.handle_request_error(e, "scrape_comments_in_memory")
            raise
