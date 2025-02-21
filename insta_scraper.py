import instaloader
import os
import requests
import random  
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Set the target username
USERNAME = "lizagacko"

# Your Instagram session ID (replace with your actual session ID)
SESSION_ID = "29474417%3AcjPfEc0BZaFvth%3A22%3AAYceq-2qPDWzu8CBnE3X5bzQOPCnAsaZ__wiwCqCmQ"  # <-- Replace this with your session ID

# Define the year of posts to scrape
TARGET_YEAR = 2024  # Change this to your desired year

# Create a directory for the specific year
YEAR_DOWNLOAD_DIR = os.path.join(f"{USERNAME}_posts", str(TARGET_YEAR))
os.makedirs(YEAR_DOWNLOAD_DIR, exist_ok=True)

# Set User-Agent to Microsoft Edge on Windows 11
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.64"

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
    total=5,  # Increase retries on failed requests
    backoff_factor=1,  # Time between retries
    status_forcelist=[500, 502, 503, 504],  # Retry on specific HTTP statuses
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

# Set a fixed User-Agent in session headers
session.headers.update({"User-Agent": USER_AGENT})
session.timeout = timeout

# Download limit settings
MAX_CALLS_PER_HOUR = 200
download_count = 0
start_time = time.time()

# Load profile and scrape posts from the specified year
try:
    profile = instaloader.Profile.from_username(loader.context, USERNAME)
    print(f"Scraping posts from {USERNAME} in the year {TARGET_YEAR}...")

    posts_to_download = []  # Store posts from the target year

    for post in profile.get_posts():
        post_year = post.date.year  # Get the year of the post

        if post_year == TARGET_YEAR:
            posts_to_download.append(post)  # Collect posts from the target year

    # Now, download all collected posts
    if posts_to_download:
        print(f"Downloading {len(posts_to_download)} posts from {TARGET_YEAR}...")

        for post in posts_to_download:
            # Check for image
            image_filename = os.path.join(YEAR_DOWNLOAD_DIR, f"{post.shortcode}.jpg")
            # Check for video
            video_filename = os.path.join(YEAR_DOWNLOAD_DIR, f"{post.shortcode}.mp4")

            # Skip post if image or video already exists
            if os.path.exists(image_filename) or os.path.exists(video_filename):
                print(f"Skipping already downloaded post: {post.shortcode}")
                continue

            # Download the post (image or video)
            loader.download_post(post, target=YEAR_DOWNLOAD_DIR)
            print(f"Downloaded: {post.shortcode}")

            download_count += 1

            # Check if download limit is reached
            if download_count >= MAX_CALLS_PER_HOUR:
                elapsed_time = time.time() - start_time
                if elapsed_time < 3600:  # Less than 1 hour
                    wait_time = 3600 - elapsed_time  # Wait for the remainder of the hour
                    print(f"Reached {MAX_CALLS_PER_HOUR} downloads, waiting for {wait_time} seconds...")
                    time.sleep(wait_time)  # Sleep until the next hour
                start_time = time.time()  # Reset the timer
                download_count = 0  # Reset the download count

            time.sleep(random.uniform(5, 10))  # Increase delay to avoid rate-limiting

    print("Scraping complete!")
except requests.exceptions.Timeout:
    print(f"Request timed out after {timeout} seconds. You may have been blocked.")
except requests.exceptions.HTTPError as err:
    if err.response.status_code == 500:
        print("Error 500: Server issue. Retrying...")
    else:
        print(f"HTTP Error: {err}")
except Exception as e:
    print(f"Error occurred: {e}")
