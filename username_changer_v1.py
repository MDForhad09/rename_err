"""
Automated username changer script - Version 1.0
"""
import requests
import time
import sys
import os
from typing import Dict, Any
from urllib.parse import urlencode, quote_plus
from config import (
    LOGIN_ENDPOINT, CHANGE_USERNAME_ENDPOINT,
    DELAY_BETWEEN_REQUESTS, DEFAULT_HEADERS, VERIFY_SSL
)
from logger_setup import setup_logger
import user_config_v1 as user_config

class UsernameChanger:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Length": "",  # Will be set automatically by requests
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://admin.skyviewonline.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Priority": "u=0, i"
        })
        self.session.verify = VERIFY_SSL
        self.logger = setup_logger()

        # Get cookie from user configuration
        self.jsessionid = user_config.load_cookie()

        # Set session cookies
        self.session.cookies.set('JSESSIONID', self.jsessionid)
        self.session.cookies.set('maximorig', self.jsessionid)

    def change_username(self, new_username: str) -> bool:
        """Change username for the current session"""
        try:
            # Set referer header exactly as captured
            referer = f"https://admin.skyviewonline.com/mainPage.jsp?id={self.jsessionid}&cid=105066&edit_id=111493&linkname=useredit&red_link=icustomerdetails"
            self.session.headers.update({"Referer": referer})

            # Construct request body exactly as captured, maintaining parameter order
            data = (
                f"linkname=useredit-2&utype=customer&redLink=icustomerdetails&"
                f"pop_id=0&cid=105066&cust_id=1140541&fname=25yeasin&"
                f"uname={quote_plus(new_username)}&unameold=25yeasin&mobile1=01316082008&"
                f"mobile2=&nid=01316082008&cperson=&cnumber=&email=&"
                f"group_id=110&otherser=&fbid=&addr1=&house_no=01316082008&"
                f"road_no=&areaOld=&town=&district=3&cthana=270&"
                f"country=Bangladesh&zip=&int_ref=&hints=&otp_count=0&"
                f"edit_id=111493&id={self.jsessionid}"
            )

            self.logger.debug(f"Sending username change request for {new_username}")
            self.logger.debug(f"Request URL: {CHANGE_USERNAME_ENDPOINT}")
            self.logger.debug(f"Request headers: {dict(self.session.headers)}")
            self.logger.debug(f"Request cookies: {dict(self.session.cookies)}")
            self.logger.debug(f"Request data: {data}")

            # Make the request with exact cookies and data format
            response = self.session.post(
                CHANGE_USERNAME_ENDPOINT,
                data=data,
                cookies={
                    'JSESSIONID': self.jsessionid,
                    'maximorig': self.jsessionid
                },
                allow_redirects=True
            )

            # Log complete response for debugging
            self.logger.debug(f"Response status: {response.status_code}")
            self.logger.debug(f"Response headers: {dict(response.headers)}")
            self.logger.debug(f"Response content: {response.text[:1000]}")

            if response.status_code >= 400:
                self.logger.error(f"Error response {response.status_code}: {response.text}")
                return False

            # Check response for success indicators
            if "error" not in response.text.lower() and response.status_code == 200:
                self.logger.info(f"Successfully changed username to: {new_username}")
                return True
            else:
                self.logger.warning(f"Failed to change username to {new_username}. Response: {response.text[:500]}")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error changing username to {new_username}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Error response status: {e.response.status_code}")
                self.logger.error(f"Error response content: {e.response.text[:500]}")
            return False

    def run(self):
        """Main execution method"""
        # Get usernames from user configuration
        usernames = user_config.load_usernames()

        self.logger.info(f"Starting username changes for {len(usernames)} usernames with JSESSIONID: {self.jsessionid}")

        for username in usernames:
            self.logger.info(f"Processing username change to: {username}")

            if self.change_username(username):
                self.logger.info(f"Waiting {DELAY_BETWEEN_REQUESTS} seconds before next request")
                time.sleep(DELAY_BETWEEN_REQUESTS)
            else:
                self.logger.error(f"Failed to change username to {username}. Continuing with next...")

        self.logger.info("Username change automation completed")
        self.session.close()

if __name__ == "__main__":
    import os
    print("\
██████╗░███████╗███╗░░██╗░█████╗░███╗░░░███╗███████╗███████╗██████╗░██████╗░
██╔══██╗██╔════╝████╗░██║██╔══██╗████╗░████║██╔════╝██╔════╝██╔══██╗██╔══██╗
██████╔╝█████╗░░██╔██╗██║███████║██╔████╔██║█████╗░░█████╗░░██████╔╝██████╔╝
██╔══██╗██╔══╝░░██║╚████║██╔══██║██║╚██╔╝██║██╔══╝░░██╔══╝░░██╔══██╗██╔══██╗
██║░░██║███████╗██║░╚███║██║░░██║██║░╚═╝░██║███████╗███████╗██║░░██║██║░░██║
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝")

    # Offer to update existing configuration if it exists
    if os.path.exists("cookie.txt") or os.path.exists("usernames.txt"):
        print("Existing configuration found!")
        user_config.update_cookie()
        user_config.update_usernames()

    changer = UsernameChanger()
    changer.run()
