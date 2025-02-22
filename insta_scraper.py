import instaloader
import os
import time
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Instagram Scraper: Scrape Reels, Posts, or Stories")
parser.add_argument("-u", "--username", required=True, help="Target Instagram username")
parser.add_argument("-s", "--session", required=True, help="Instagram session ID")
parser.add_argument("-t", "--type", choices=["reels", "posts", "stories"], required=True, help="Type of content to scrape")
parser.add_argument("-y", "--year", type=int, help="Target year for filtering posts or reels")
args = parser.parse_args()

USERNAME = args.username
SESSION_ID = args.session
SCRAPE_TYPE = args.type
TARGET_YEAR = args.year if args.year else None

# Create the main directory for the target user
MAIN_DIR = f"{USERNAME}"
if not os.path.exists(MAIN_DIR):
    os.makedirs(MAIN_DIR)
    print(f"Folder for user {USERNAME} has been created: {MAIN_DIR}")

# Initialize Instaloader with session ID authentication
loader = instaloader.Instaloader(download_pictures=True, download_videos=True,
                                 download_video_thumbnails=False, save_metadata=False,
                                 post_metadata_txt_pattern="")
loader.context._session.cookies.set("sessionid", SESSION_ID)
print("Authenticated using session ID!")

# Load profile
try:
    profile = instaloader.Profile.from_username(loader.context, USERNAME)
    
    if SCRAPE_TYPE == "stories":
        USER_DOWNLOAD_DIR = os.path.join(MAIN_DIR, "Stories")
        if not os.path.exists(USER_DOWNLOAD_DIR):
            os.makedirs(USER_DOWNLOAD_DIR)
        print(f"Downloading active stories from {USERNAME}...")
        for story in loader.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                loader.download_storyitem(item, target=USER_DOWNLOAD_DIR)
                print(f"⬇️ Downloaded story {item.shortcode}")
        print("✅ Story download complete!")
    
    elif SCRAPE_TYPE in ["reels", "posts"]:
        USER_DOWNLOAD_DIR = os.path.join(MAIN_DIR, SCRAPE_TYPE.capitalize())
        if not os.path.exists(USER_DOWNLOAD_DIR):
            os.makedirs(USER_DOWNLOAD_DIR)
        print(f"Scanning {SCRAPE_TYPE} from {USERNAME}...")
        for post in profile.get_posts():
            if SCRAPE_TYPE == "reels" and (not post.is_video or post.typename != "GraphVideo"):
                continue  # Skip non-video posts when scraping reels
            if TARGET_YEAR and post.date.year != TARGET_YEAR:
                continue  # Skip posts/reels not in the target year
            loader.download_post(post, target=USER_DOWNLOAD_DIR)
            print(f"⬇️ Downloaded {SCRAPE_TYPE} from {post.date.strftime('%Y-%m-%d')} - {post.shortcode}")
        print(f"✅ {SCRAPE_TYPE.capitalize()} scraping complete!")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print(f"❌ {SCRAPE_TYPE.capitalize()} scraping terminated due to an error.")
