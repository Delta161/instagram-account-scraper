import instaloader
import os
import requests
import random
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Set the target username
USERNAME = "NAME_TARGET_ACCOUNT"

# Your Instagram session ID (replace with your actual session ID)
SESSION_ID = "INSTAGRAM_SESSION_ID"  # <-- Replace this with your session ID

# Create a directory to store the downloaded photos
DOWNLOAD_DIR = f"{USERNAME}_posts"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# List of random User-Agents to avoid detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36",
]

# Initialize Instaloader with session ID authentication
loader = instaloader.Instaloader(download_pictures=True, download_videos=True,
                                 download_video_thumbnails=False, save_metadata=False,
                                 post_metadata_txt_pattern="")

# Set session ID for authentication
loader.context._session.cookies.set("sessionid", SESSION_ID)
print("Authenticated using session ID!")

# Adding timeout and retry strategy to avoid getting blocked
timeout = 120  # Timeout in seconds
session = loader.context._session

retry_strategy = Retry(
    total=3,  # Number of retries on failed requests
    backoff_factor=1,  # Time between retries
    status_forcelist=[500, 502, 503, 504],  # Retry on specific HTTP statuses
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

# Set a random User-Agent in session headers
session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
session.timeout = timeout

# Load profile and scrape posts
try:
    profile = instaloader.Profile.from_username(loader.context, USERNAME)
    print(f"Scraping posts from {USERNAME}...")
    
    # Download posts with random delay between requests
    for post in profile.get_posts():
        loader.download_post(post, target=DOWNLOAD_DIR)
        print(f"Downloaded: {post.shortcode}")
        time.sleep(random.uniform(2, 5))  # Random delay between 2-5 seconds

    print("Scraping complete!")
except requests.exceptions.Timeout:
    print(f"Request timed out after {timeout} seconds. You may have been blocked.")
except Exception as e:
    print(f"Error occurred: {e}")
