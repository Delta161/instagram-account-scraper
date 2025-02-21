# Instaloader Instagram Scraper

## Overview
This script uses **Instaloader** to scrape and download posts from a specified Instagram profile using a **session ID** for authentication. It avoids detection by using random **User-Agents**, **request retries**, and **random delays** between requests.

## Features
- ✅ **Session ID Authentication** (No username/password needed)
- ✅ **Random User-Agent Rotation** (Reduces bot detection risks)
- ✅ **Retry Mechanism** (Handles request failures)
- ✅ **Random Delay Between Requests** (Mimics human-like behavior)
- ✅ **Downloads Images & Videos**

## Requirements
- Python 3.x
- Instaloader (`pip install instaloader`)

## Setup Instructions

### 1️⃣ **Get Your Instagram Session ID**
1. Log in to Instagram via your web browser.
2. Open **Developer Tools** (F12 or right-click → Inspect).
3. Navigate to **Application** → **Storage** → **Cookies** → `instagram.com`.
4. Find the `sessionid` cookie and copy its value.

### 2️⃣ **Configure the Script**
1. Open `insta_scraper.py`.
2. Replace the placeholder:
   ```python
   SESSION_ID = "your_instagram_session_id_here"
   ```
   with your actual Instagram `sessionid`.

### 3️⃣ **Run the Script**
Execute the script using:
```bash
python insta_scraper.py
```

## Troubleshooting
### ❌ `AttributeError: 'InstaloaderContext' object has no attribute 'session'`
✅ Fix: Replace `session` with `_session` in the script:
```python
loader.context._session.cookies.set("sessionid", SESSION_ID)
```

### ❌ `Request timed out after X seconds. You may have been blocked.`
✅ Fix: Try a different **session ID**, **increase delay times**, or use a **VPN**.

## Disclaimer
⚠️ **Use this script responsibly!** Scraping Instagram may violate their terms of service. Avoid excessive requests to prevent getting blocked.

---
🚀 Happy Scraping! 🚀

