import os
import csv
import re
import time
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    StaleElementReferenceException, ElementClickInterceptedException
)

class FacebookSeleniumScraper:
    def __init__(self, email, password, headless=False):
        """
        Initialize the Facebook scraper
        
        Args:
            email: Facebook login email
            password: Facebook login password
            headless: Run browser in background (True/False)
        """
        self.email = email
        self.password = password
        
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # Additional options to avoid detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=options)
        
        # Execute CDP commands to avoid detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.wait = WebDriverWait(self.driver, 200)
        self.scroll_pause_time = 2
        self.data = []
        
    def login(self):
        """Login to Facebook"""
        print("🔐 Logging into Facebook...")
        
        try:
            # Go to Facebook
            self.driver.get("https://www.facebook.com")
            time.sleep(3)
            
            # Check if already logged in
            try:
                if "facebook.com/?sk=welcome" in self.driver.current_url:
                    print("✅ Already logged in")
                    return True
            except:
                pass
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            time.sleep(1)
            
            # Enter password
            password_input = self.driver.find_element(By.NAME, "pass")
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(1)
            
            # Click login button
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()
            time.sleep(5)
            
            # Check for suspicious login attempt
            if "suspicious" in self.driver.page_source.lower() or "checkpoint" in self.driver.current_url:
                print("⚠️  Facebook detected suspicious login. Please check your account.")
                input("⚠️  Please complete the verification manually, then press Enter to continue...")
                time.sleep(5)
            
            # Wait for login to complete
            time.sleep(5)
            
            # Verify login success
            if "login" not in self.driver.current_url:
                print("✅ Login successful")
                return True
            else:
                print("❌ Login failed")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def extract_phone_numbers(self, text):
        """Extract phone numbers from text using regex patterns"""
        if not text:
            return []
        
        # More comprehensive phone number patterns
        patterns = [
            r'\b\d{10}\b',  # 10-digit numbers
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
            r'\b\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US with country code
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b',  # Other formats
            r'\b\d{5}[-.\s]?\d{5}\b',  # 5+5 format
            r'\b\d{3}[-.\s]?\d{4}[-.\s]?\d{4}\b',  # 3-4-4 format
            r'\b\+?91[-\s]?\d{5}[-\s]?\d{5}\b',  # Indian format
            r'\b\+?44[-\s]?\d{4}[-\s]?\d{6}\b',  # UK format
        ]
        
        phone_numbers = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean the number
                cleaned = re.sub(r'[^\d+]', '', match)
                # Accept numbers with 10+ digits (including country code)
                if len(cleaned) >= 10:
                    # Format nicely
                    if cleaned.startswith('+'):
                        phone_numbers.add(cleaned)
                    elif len(cleaned) == 10:
                        phone_numbers.add(cleaned[:3] + '-' + cleaned[3:6] + '-' + cleaned[6:])
                    else:
                        phone_numbers.add(cleaned)
        
        return list(phone_numbers)
    
    def scroll_page(self, scroll_pause_time=2, max_scrolls=50):
        """Scroll the page to load more content"""
        print("📜 Scrolling to load more comments...")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                # Try clicking "See more comments" if available
                try:
                    see_more_buttons = self.driver.find_elements(By.XPATH, "//div[@role='button' and contains(text(), 'See more comments')]")
                    for button in see_more_buttons:
                        try:
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(1)
                        except:
                            pass
                except:
                    pass
                
                # Check for "View more comments" buttons
                try:
                    view_more_buttons = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'View more comments')]")
                    for button in view_more_buttons:
                        try:
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(1)
                        except:
                            pass
                except:
                    pass
            
            last_height = new_height
            scrolls += 1
            
            # Progress indicator
            if scrolls % 5 == 0:
                print(f"   Scrolled {scrolls} times...")
    
    def extract_comment_data(self, comment_element):
        """Extract data from a single comment element"""
        try:
            # Get comment text
            comment_text = ""
            try:
                # Try multiple selectors for comment text
                selectors = [
                    "div[data-ad-preview='message']",
                    "div[dir='auto']",
                    "span[dir='auto']",
                    "div.userContent",
                    ".ecm0bbzt.e5nlhep0.a8c37x1j"
                ]
                
                for selector in selectors:
                    try:
                        text_elements = comment_element.find_elements(By.CSS_SELECTOR, selector)
                        for elem in text_elements:
                            text = elem.text.strip()
                            if text and len(text) > 2:  # Avoid empty or very short texts
                                comment_text = text
                                break
                        if comment_text:
                            break
                    except:
                        continue
            except:
                comment_text = ""
            
            # Get user name
            user_name = ""
            try:
                # Multiple selectors for user name
                name_selectors = [
                    "a[role='link'][tabindex='-1']",
                    "a[href*='/'] span",
                    "strong a",
                    "h3 a",
                    ".oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.c1et5uql.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.iv3no6db.jq4qci2q.a3bd9o3v.b1v8xokw.oo9gr5id.hzawbc8m",
                    "a[class*='profile']"
                ]
                
                for selector in name_selectors:
                    try:
                        name_elements = comment_element.find_elements(By.CSS_SELECTOR, selector)
                        for elem in name_elements:
                            name = elem.text.strip()
                            if name and len(name) > 1:  # Avoid single characters
                                user_name = name
                                # Try to get profile URL from this element
                                try:
                                    profile_url = elem.get_attribute('href')
                                except:
                                    profile_url = ""
                                break
                        if user_name:
                            break
                    except:
                        continue
            except:
                user_name = ""
            
            # Get profile URL
            profile_url = ""
            if not profile_url:  # If not already got from name element
                try:
                    # Look for profile links
                    profile_links = comment_element.find_elements(By.CSS_SELECTOR, "a[href*='/']")
                    for link in profile_links:
                        href = link.get_attribute('href')
                        if href and ('/profile.php' in href or '/user/' in href or '/people/' in href or re.search(r'/[\w.]+/?$', href)):
                            profile_url = href
                            break
                except:
                    profile_url = ""
            
            # Extract phone numbers
            phone_numbers = self.extract_phone_numbers(comment_text)
            
            # Get timestamp
            timestamp = ""
            try:
                time_elements = comment_element.find_elements(By.CSS_SELECTOR, "a[aria-label*='ago'], span[data-tooltip-content]")
                for elem in time_elements:
                    time_text = elem.text.strip() or elem.get_attribute('aria-label') or elem.get_attribute('data-tooltip-content')
                    if time_text and ('ago' in time_text.lower() or 'hr' in time_text.lower() or 'min' in time_text.lower()):
                        timestamp = time_text
                        break
            except:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                'user_name': user_name,
                'comment_text': comment_text,
                'phone_numbers': ', '.join(phone_numbers) if phone_numbers else '',
                'profile_url': profile_url,
                'timestamp': timestamp,
                'has_phone': bool(phone_numbers)
            }
            
        except StaleElementReferenceException:
            return None
        except Exception as e:
            print(f"Error extracting comment: {e}")
            return None
    
    def scrape_post_comments(self, post_url, max_comments=1000):
        """
        Scrape comments from a Facebook post
        
        Args:
            post_url: URL of the Facebook post
            max_comments: Maximum number of comments to scrape
        """
        print(f"🔗 Opening post: {post_url}")
        
        try:
            # Navigate to the post
            self.driver.get(post_url)
            time.sleep(5)
            
            # Accept cookies if prompted (EU)
            try:
                accept_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept') or contains(text(), '同意')]")
                accept_button.click()
                time.sleep(2)
            except:
                pass
            
            # Scroll to load comments
            self.scroll_page()
            
            # Find all comment elements
            print("🔍 Searching for comments...")
            
            # Multiple selectors for comments (Facebook changes these often)
            comment_selectors = [
                "div[data-commentid]",
                "div[role='article']",
                "div[data-ad-comet-preview='comment']",
                "div[class*='comment']",
                "div[class*='userContent']",
                ".ecm0bbzt.e5nlhep0.a8c37x1j",
                "div[data-sigil='comment']",
                "div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0"
            ]
            
            all_comments = []
            
            for selector in comment_selectors:
                try:
                    comment_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(comment_elements) > 5:  # If we found a reasonable number
                        all_comments = comment_elements
                        print(f"✅ Found {len(all_comments)} potential comment elements using selector: {selector}")
                        break
                except:
                    continue
            
            if not all_comments:
                print("❌ No comments found with standard selectors. Trying alternative approach...")
                
                # Alternative approach: look for any divs with text
                all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                all_comments = [div for div in all_divs if len(div.text) > 10]  # Filter for meaningful content
                print(f"✅ Found {len(all_comments)} div elements with text")
            
            # Process comments
            processed_comments = 0
            comments_with_data = []
            
            print(f"📊 Processing {len(all_comments)} comments...")
            
            for i, comment_element in enumerate(all_comments):
                try:
                    # Skip if too many comments processed
                    if processed_comments >= max_comments:
                        break
                    
                    # Extract data from comment
                    comment_data = self.extract_comment_data(comment_element)
                    
                    if comment_data:
                        comments_with_data.append(comment_data)
                        processed_comments += 1
                        
                        # Progress indicator
                        if processed_comments % 20 == 0:
                            print(f"   Processed {processed_comments} comments...")
                            
                            # Save progress periodically
                            if processed_comments % 100 == 0:
                                self.save_progress(comments_with_data, "progress_save.csv")
                
                except StaleElementReferenceException:
                    # Element became stale, skip it
                    continue
                except Exception as e:
                    print(f"Error processing comment {i}: {e}")
                    continue
            
            # Filter for comments with phone numbers
            comments_with_phones = [c for c in comments_with_data if c['has_phone']]
            
            print(f"\n📈 SCRAPING SUMMARY:")
            print(f"   Total comments found: {len(comments_with_data)}")
            print(f"   Comments with phone numbers: {len(comments_with_phones)}")
            
            self.data = comments_with_data
            
            return comments_with_data
            
        except Exception as e:
            print(f"❌ Error scraping post: {e}")
            return []
    
    def save_progress(self, data, filename):
        """Save progress to CSV"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Progress saved to {filename}")
        except Exception as e:
            print(f"Error saving progress: {e}")
    
    def export_data(self, data=None, filename_prefix=None):
        """Export data to CSV, Excel, and JSON"""
        if data is None:
            data = self.data
        
        if not data:
            print("❌ No data to export")
            return
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if filename_prefix:
            base_filename = f"{filename_prefix}_{timestamp}"
        else:
            base_filename = f"facebook_comments_{timestamp}"
        
        # Filter for comments with phone numbers only
        data_with_phones = [d for d in data if d['has_phone']]
        
        if not data_with_phones:
            print("⚠️  No comments with phone numbers found. Exporting all comments...")
            data_to_export = data
        else:
            data_to_export = data_with_phones
        
        # Create DataFrame
        df = pd.DataFrame(data_to_export)
        
        # Remove the helper column
        if 'has_phone' in df.columns:
            df = df.drop('has_phone', axis=1)
        
        # Export to CSV
        csv_filename = f"{base_filename}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"✅ CSV saved: {csv_filename}")
        
        # Export to Excel
        excel_filename = f"{base_filename}.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"✅ Excel saved: {excel_filename}")
        
        # Export to JSON
        json_filename = f"{base_filename}.json"
        df.to_json(json_filename, orient='records', indent=2, force_ascii=False)
        print(f"✅ JSON saved: {json_filename}")
        
        # Print summary
        print(f"\n📊 EXPORT SUMMARY:")
        print(f"   Total records exported: {len(df)}")
        print(f"   Columns: {', '.join(df.columns.tolist())}")
        
        # Show preview
        print(f"\n📋 DATA PREVIEW (first 5 rows):")
        print("-" * 80)
        if len(df) > 0:
            print(df.head().to_string())
        else:
            print("No data to preview")
        
        return {
            'csv': csv_filename,
            'excel': excel_filename,
            'json': json_filename,
            'total_records': len(df)
        }
    
    def scrape_multiple_posts(self, post_urls, max_comments_per_post=500):
        """Scrape comments from multiple posts"""
        all_data = []
        
        for i, post_url in enumerate(post_urls):
            print(f"\n{'='*60}")
            print(f"📝 Processing post {i+1}/{len(post_urls)}")
            print(f"📌 URL: {post_url}")
            print(f"{'='*60}")
            
            try:
                comments = self.scrape_post_comments(post_url, max_comments_per_post)
                all_data.extend(comments)
                
                # Save progress after each post
                self.save_progress(all_data, f"progress_post_{i+1}.csv")
                
                # Wait between posts to avoid detection
                if i < len(post_urls) - 1:
                    wait_time = 10
                    print(f"\n⏳ Waiting {wait_time} seconds before next post...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"❌ Failed to scrape post {i+1}: {e}")
                continue
        
        self.data = all_data
        return all_data
    
    def close(self):
        """Close the browser"""
        print("\n👋 Closing browser...")
        try:
            self.driver.quit()
        except:
            pass


# ================================================
# MAIN EXECUTION
# ================================================

def main():
    print("=" * 70)
    print("🔥 FACEBOOK COMMENT SCRAPER WITH PHONE NUMBER EXTRACTION 🔥")
    print("=" * 70)
    
    # ================================================
    # CONFIGURATION - EDIT THESE VALUES
    # ================================================
    
    # Facebook login credentials - load from environment variables
    FACEBOOK_EMAIL = os.getenv("FB_EMAIL") or input("Enter your Facebook email: ")
    FACEBOOK_PASSWORD = os.getenv("FB_PASSWORD") or input("Enter your Facebook password: ")

    # Post URLs to scrape (can be one or multiple)
    POST_URLS = [
        "https://www.facebook.com/reel/1432280715189258",  # ← REPLACE WITH ACTUAL POST URL
        # "https://www.facebook.com/YourPageName/posts/987654321098765",  # Add more if needed
    ]
    
    # ================================================
    # MAIN EXECUTION
    # ================================================
    
    # Create scraper instance
    scraper = FacebookSeleniumScraper(
        email=FACEBOOK_EMAIL,
        password=FACEBOOK_PASSWORD,
        headless=False  # Set to True to run in background
    )
    
    try:
        # Step 1: Login
        if not scraper.login():
            print("❌ Login failed. Exiting...")
            return
        
        # Wait a moment after login
        time.sleep(3)
        
        # Step 2: Scrape single post or multiple posts
        if len(POST_URLS) == 1:
            print(f"\n🎯 Scraping single post...")
            data = scraper.scrape_post_comments(POST_URLS[0], max_comments=1000)
        else:
            print(f"\n🎯 Scraping {len(POST_URLS)} posts...")
            data = scraper.scrape_multiple_posts(POST_URLS, max_comments_per_post=500)
        
        # Step 3: Export results
        if data:
            print(f"\n{'='*60}")
            print("📦 EXPORTING RESULTS")
            print(f"{'='*60}")
            
            results = scraper.export_data(
                data=data,
                filename_prefix="facebook_scraped_data"
            )
            
            print(f"\n🎉 SCRAPING COMPLETE!")
            print(f"📊 Total comments with phone numbers: {results['total_records']}")
            print(f"💾 Files saved:")
            print(f"   - {results['csv']}")
            print(f"   - {results['excel']}")
            print(f"   - {results['json']}")
            
        else:
            print("\n❌ No comments scraped. Check your post URLs and login.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
        
        # Save any progress before exiting
        if scraper.data:
            print("\n💾 Saving progress before exit...")
            scraper.export_data(filename_prefix="interrupted_scrape")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        
    finally:
        # Step 4: Close browser
        scraper.close()


# ================================================
# QUICK START SCRIPT
# ================================================

def quick_scrape():
    """Simple function for quick scraping"""
    
    # Quick configuration
    EMAIL = input("Enter your Facebook email: ")
    PASSWORD = input("Enter your Facebook password: ")
    POST_URL = input("Enter Facebook post URL: ")
    
    print("\n🚀 Starting quick scrape...")
    
    scraper = FacebookSeleniumScraper(EMAIL, PASSWORD, headless=False)
    
    try:
        if scraper.login():
            time.sleep(3)
            data = scraper.scrape_post_comments(POST_URL, max_comments=1000)
            
            if data:
                scraper.export_data(data, "quick_scrape_results")
            else:
                print("❌ No data scraped")
                
    finally:
        scraper.close()


if __name__ == "__main__":
    # Run the main function
    main()
    
    # Or for quick testing, uncomment the line below:
    # quick_scrape()