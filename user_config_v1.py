import os
from typing import List

def load_cookie() -> str:
    """Load or prompt for JSESSIONID cookie"""
    cookie_file = "cookie.txt"

    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            cookie = f.read().strip()
            if cookie:
                print(f"\nLoaded existing JSESSIONID cookie: {cookie[:8]}...")
                return cookie

    print("\nPlease enter your JSESSIONID cookie from the admin panel login.")
    print("You can find this by:")
    print("1. Log into admin.skyviewonline.com")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to 'Application' tab > 'Cookies'")
    print("4. Copy the value of JSESSIONID\n")

    cookie = input("Enter JSESSIONID cookie: ").strip()
    while not cookie:
        print("Cookie cannot be empty. Please try again.")
        cookie = input("Enter JSESSIONID cookie: ").strip()

    with open(cookie_file, 'w') as f:
        f.write(cookie)
    print(f"\nSaved JSESSIONID cookie: {cookie[:8]}...")

    return cookie

def load_usernames() -> List[str]:
    """Load or create username list"""
    username_file = "usernames.txt"

    if os.path.exists(username_file):
        with open(username_file, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
            if usernames:
                print(f"\nLoaded {len(usernames)} usernames from {username_file}")
                return usernames

    print("\nNo username list found. Please enter usernames (one per line)")
    print("Press Enter twice when done\n")

    usernames = []
    while True:
        username = input("Enter username (or press Enter to finish): ").strip()
        if not username:
            if usernames:  # Only break if we have at least one username
                break
            print("Please enter at least one username")
            continue
        usernames.append(username)
        print(f"Added username: {username}")

    with open(username_file, 'w') as f:
        f.write('\n'.join(usernames))

    print(f"\nSaved {len(usernames)} usernames to {username_file}")
    return usernames

def update_usernames() -> List[str]:
    """Update existing username list"""
    if os.path.exists("usernames.txt"):
        print("\nCurrent usernames:")
        with open("usernames.txt", 'r') as f:
            current = f.read()
            print(current)

    choice = input("\nDo you want to update the username list? (y/N): ").strip().lower()
    if choice == 'y':
        os.remove("usernames.txt")
        return load_usernames()

    return load_usernames()

def update_cookie() -> str:
    """Update existing cookie"""
    if os.path.exists("cookie.txt"):
        with open("cookie.txt", 'r') as f:
            current = f.read().strip()
            print(f"\nCurrent cookie: {current[:8]}...")

    choice = input("\nDo you want to update the JSESSIONID cookie? (y/N): ").strip().lower()
    if choice == 'y':
        if os.path.exists("cookie.txt"):
            os.remove("cookie.txt")
        return load_cookie()

    return load_cookie()
