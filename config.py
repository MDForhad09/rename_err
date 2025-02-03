# Base URL for the application
BASE_URL = "https://admin.skyviewonline.com"
LOGIN_ENDPOINT = f"{BASE_URL}/validate3.jsp"
CHANGE_USERNAME_ENDPOINT = f"{BASE_URL}/mainPage.jsp"

# Request delay in seconds
DELAY_BETWEEN_REQUESTS = 15  # Increased delay for reliability

# Request headers
DEFAULT_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9"
}

# SSL verification flag - Set to False for internal admin site
VERIFY_SSL = False