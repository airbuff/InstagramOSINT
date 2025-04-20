#!/usr/bin/env python3
# Instagram OSINT Tool
# For educational purposes only
# Use responsibly and ethically

import argparse
from bs4 import BeautifulSoup
import json
import os
import requests
import random
import string
import sys
import time
import re

# ASCII Art Banner
banner = '''
 ___           _                                  ___  ____ ___ _   _ _____ 
|_ _|_ __  ___| |_ __ _  __ _ _ __ __ _ _ __ ___ / _ \/ ___|_ _| \ | |_   _|
 | || '_ \/ __| __/ _` |/ _` | '__/ _` | '_ ` _ \ | | \___ \| ||  \| | | |  
 | || | | \__ \ || (_| | (_| | | | (_| | | | | | | |_| |___) | || |\  | | |  
|___|_| |_|___/\__\__,_|\__, |_|  \__,_|_| |_| |_|\___/|____/___|_| \_| |_|  
                        |___/                                               
'''

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InstagramOSINT:

    def __init__(self, username, downloadPhotos):
        # Rotate user agents to avoid detection
        self.useragents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ]
                 
        self.username = username
        # Make the directory that we are putting the files into
        self.make_directory()
        print(colors.OKGREEN + f"[*] Starting Scan on {self.username}" + colors.ENDC)

        # Get the html data with the requests module
        try:
            r = requests.get(f'https://www.instagram.com/{self.username}/', 
                           headers={'User-Agent': random.choice(self.useragents)})
            
            if r.status_code == 404:
                print(colors.FAIL + f"Username {self.username} not found" + colors.ENDC)
                sys.exit()
                
            if r.status_code == 429:
                print(colors.FAIL + "Rate limited by Instagram. Try again later." + colors.ENDC)
                sys.exit()
                
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # To prevent a unicode error, we need the following line...
            soup.encode('utf-8')
            
            # Extract JSON data from the page
            shared_data = None
            
            # Method 1: Look for window._sharedData
            for script in soup.find_all('script'):
                if script.text.startswith('window._sharedData ='):
                    shared_data = json.loads(script.text.replace('window._sharedData = ', '').rstrip(';'))
                    break
                    
            # Method 2: Look for additional data loads
            if not shared_data:
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.text and 'profilePage' in script.text:
                        json_text = re.search(r'window\.__additionalDataLoaded\(\'.*?\',(.+)\);<\/script>', script.text)
                        if json_text:
                            shared_data = json.loads(json_text.group(1))
                            break
            
            # Method 3: Look for Instagram GraphQL data pattern
            if not shared_data:
                for script in soup.find_all('script', type="text/javascript"):
                    if script.text and 'window.__initialDataLoaded' in script.text:
                        match = re.search(r'window\.__initialDataLoaded\(window\._sharedData = (.+);\)', script.text)
                        if match:
                            shared_data = json.loads(match.group(1))
                            break
            
            if not shared_data:
                print(colors.FAIL + "Could not extract profile data. Instagram may have changed their page structure." + colors.ENDC)
                print(colors.WARNING + "Instagram frequently changes their API structure, which can break this script." + colors.ENDC)
                print(colors.WARNING + "Try updating the script or using a web browser." + colors.ENDC)
                sys.exit()
                
            # Try to extract user data from multiple possible locations
            try:
                user = None
                
                # Check different possible locations for user data
                if 'entry_data' in shared_data and 'ProfilePage' in shared_data['entry_data']:
                    user = shared_data['entry_data']['ProfilePage'][0]['graphql']['user']
                elif 'user' in shared_data:
                    user = shared_data['user']
                elif 'data' in shared_data and 'user' in shared_data['data']:
                    user = shared_data['data']['user']
                
                if not user:
                    raise KeyError("User data not found in expected locations")
                    
                # Basic profile information
                self.profile_data = {
                    "Username": user.get('username', 'Unknown'),
                    "Profile name": user.get('full_name', 'Unknown'),
                    "URL": f"https://www.instagram.com/{self.username}/",
                    "Followers": str(user.get('edge_followed_by', {}).get('count', 'Unknown')),
                    "Following": str(user.get('edge_follow', {}).get('count', 'Unknown')),
                    "Posts": str(user.get('edge_owner_to_timeline_media', {}).get('count', 'Unknown')),
                    "Bio": str(user.get('biography', 'No bio')),
                    "profile_pic_url": str(user.get('profile_pic_url_hd', user.get('profile_pic_url', ''))),
                    "is_business_account": str(user.get('is_business_account', 'Unknown')),
                    "connected_to_fb": str(user.get('connected_fb_page', 'Unknown')),
                    "externalurl": str(user.get('external_url', 'None')),
                    "joined_recently": str(user.get('is_joined_recently', 'Unknown')),
                    "business_category_name": str(user.get('business_category_name', 'None')),
                    "is_private": str(user.get('is_private', 'Unknown')),
                    "is_verified": str(user.get('is_verified', 'Unknown'))
                }
                
                # Additional data if available
                if user.get('highlight_reel_count'):
                    self.profile_data["Highlights"] = str(user.get('highlight_reel_count'))
                
                if user.get('is_professional_account'):
                    self.profile_data["is_professional_account"] = str(user.get('is_professional_account'))
                
                if user.get('category_name'):
                    self.profile_data["category_name"] = str(user.get('category_name'))
                
            except (KeyError, TypeError) as e:
                print(colors.FAIL + f"Error extracting profile data: {e}" + colors.ENDC)
                print(colors.WARNING + "Instagram might have changed their page structure." + colors.ENDC)
                sys.exit()
                
        except requests.exceptions.RequestException as e:
            print(colors.FAIL + f"Error connecting to Instagram: {e}" + colors.ENDC)
            sys.exit()
            
        # Save profile data
        self.save_data()
        
        # Optionally download photos
        if downloadPhotos == True:
            if self.profile_data.get('is_private', 'true').lower() != 'true':
                self.scrape_posts(user)
            else:
                print(colors.WARNING + "[*] Private profile, cannot download photos." + colors.ENDC)
            
        self.print_data()

    def scrape_posts(self, user_data):
        """Scrapes all posts and downloads thumbnails when necessary"""
        print(colors.OKGREEN + "[*] Getting Photos" + colors.ENDC)
        posts = {}
        
        try:
            edges = user_data.get('edge_owner_to_timeline_media', {}).get('edges', [])
            
            if not edges:
                print(colors.WARNING + "[*] No posts found or unable to access posts" + colors.ENDC)
                return
                
            for index, post in enumerate(edges):
                node = post.get('node', {})
                
                # Create directory for this post
                post_dir = f"{index}"
                if not os.path.exists(post_dir):
                    os.mkdir(post_dir)
                
                # Extract post data
                caption_edges = node.get('edge_media_to_caption', {}).get('edges', [])
                caption = caption_edges[0]['node']['text'] if caption_edges else 'No Caption on this post'
                
                # Collect post metadata
                post_data = {
                    "Caption": caption,
                    "Number of Comments": str(node.get('edge_media_to_comment', {}).get('count', 0)),
                    "Comments Disabled": str(node.get('comments_disabled', False)),
                    "Taken At Timestamp": str(node.get('taken_at_timestamp', 'Unknown')),
                    "Number of Likes": str(node.get('edge_liked_by', {}).get('count', 0)),
                    "Location": str(node.get('location', 'Unknown')),
                    "Accessability Caption": str(node.get('accessibility_caption', 'None'))
                }
                
                # Add shortcode if available (direct link to post)
                if node.get('shortcode'):
                    post_data["Post URL"] = f"https://www.instagram.com/p/{node.get('shortcode')}/"
                
                # Add post type if available
                if node.get('__typename'):
                    post_data["Type"] = node.get('__typename').replace('Graph', '')
                
                # Add additional data for videos
                if node.get('is_video'):
                    post_data["Is Video"] = "True"
                    post_data["Video View Count"] = str(node.get('video_view_count', 'Unknown'))
                
                posts[index] = post_data
                
                # Download thumbnail
                try:
                    # Try different methods to get the image URL
                    img_url = None
                    
                    # Method 1: Check thumbnail_resources
                    thumbnail_resources = node.get('thumbnail_resources', [])
                    if thumbnail_resources:
                        # Get the largest available thumbnail
                        img_url = thumbnail_resources[-1].get('src', '')
                    
                    # Method 2: Check display_url
                    if not img_url and node.get('display_url'):
                        img_url = node.get('display_url')
                        
                    # Method 3: Check thumbnail_src
                    if not img_url and node.get('thumbnail_src'):
                        img_url = node.get('thumbnail_src')
                    
                    if img_url:
                        random_filename = ''.join([random.choice(string.ascii_uppercase) for _ in range(random.randint(1, 9))]) + '.jpg'
                        file_path = os.path.join(post_dir, random_filename)
                        
                        # Delay the request times randomly (be nice to Instagram)
                        time.sleep(random.randint(1, 3))
                        
                        r = requests.get(img_url, headers={'User-Agent': random.choice(self.useragents)})
                        with open(file_path, 'wb') as f:
                            f.write(r.content)
                        print(colors.OKGREEN + f"[+] Downloaded image {index+1}" + colors.ENDC)
                    else:
                        print(colors.WARNING + f"[!] No image URL for post {index+1}" + colors.ENDC)
                except Exception as e:
                    print(colors.FAIL + f"[!] Error downloading image {index+1}: {e}" + colors.ENDC)
            
            # Save post data to file
            with open('posts.txt', 'w') as f:
                f.write(json.dumps(posts, indent=4))
                
        except Exception as e:
            print(colors.FAIL + f"[!] Error scraping posts: {e}" + colors.ENDC)

    def make_directory(self):
        """Makes the profile directory and changes the cwd to it"""
        try:
            if not os.path.exists(self.username):
                os.mkdir(self.username)
                os.chdir(self.username)
                return True
            else:
                num = 0
                # This is a loop to keep trying to make a new directory if a scan has already
                # been done on a profile and that directory exists
                while True:
                    dir_name = f"{self.username}{num if num > 0 else ''}"
                    if not os.path.exists(dir_name):
                        os.mkdir(dir_name)
                        os.chdir(dir_name)
                        return True
                    num += 1
        except Exception as e:
            print(colors.FAIL + f"[!] Error creating directory: {e}" + colors.ENDC)
            sys.exit()

    def save_data(self):
        """Saves the data to the username directory"""
        try:
            with open('data.txt', 'w') as f:
                f.write(json.dumps(self.profile_data, indent=4))
            
            # Downloads the profile Picture
            self.download_profile_picture()
            print(colors.OKGREEN + f"[+] Saved data to directory {os.getcwd()}" + colors.ENDC)
        except Exception as e:
            print(colors.FAIL + f"[!] Error saving data: {e}" + colors.ENDC)

    def print_data(self):
        """Prints out the data to the screen"""
        print(colors.HEADER + "---------------------------------------------" + colors.ENDC)
        print(colors.OKGREEN + f"Results: scan for {self.profile_data['Username']} on instagram" + colors.ENDC)
        for key, value in self.profile_data.items():
            print(f"{key}: {value}")
        print(colors.HEADER + "---------------------------------------------" + colors.ENDC)

    def download_profile_picture(self):
        """Downloads the profile pic and saves it to the directory"""
        try:
            if self.profile_data.get('profile_pic_url'):
                with open("profile_pic.jpg", "wb") as f:
                    time.sleep(1)
                    r = requests.get(self.profile_data['profile_pic_url'], 
                                   headers={'User-Agent': random.choice(self.useragents)})
                    if r.status_code == 200:
                        f.write(r.content)
                        print(colors.OKGREEN + "[+] Downloaded profile picture" + colors.ENDC)
                    else:
                        print(colors.WARNING + f"[!] Failed to download profile picture: HTTP {r.status_code}" + colors.ENDC)
            else:
                print(colors.WARNING + "[!] No profile picture URL found" + colors.ENDC)
        except Exception as e:
            print(colors.FAIL + f"[!] Error downloading profile picture: {e}" + colors.ENDC)


def parse_args():
    parser = argparse.ArgumentParser(description="Instagram OSINT tool")
    parser.add_argument("--username", help="profile username", required=True, nargs=1)
    parser.add_argument("--downloadPhotos", help="Downloads the users photos if their account is public", 
                       required=False, action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    print(colors.OKBLUE + banner + colors.ENDC)
    
    if args.username[0].strip() == '':
        print(colors.FAIL + "[!] Please enter the username" + colors.ENDC)
        sys.exit()
    
    # Print disclaimer
    print(colors.WARNING + "DISCLAIMER: This tool is for educational purposes only." + colors.ENDC)
    print(colors.WARNING + "Use responsibly and respect Instagram's Terms of Service." + colors.ENDC)
    print("")
    
    try:
        osint = InstagramOSINT(username=args.username[0], downloadPhotos=args.downloadPhotos)
    except KeyboardInterrupt:
        print(colors.WARNING + "\n[!] User interrupted the program" + colors.ENDC)
        sys.exit()
    except Exception as e:
        print(colors.FAIL + f"[!] An unexpected error occurred: {e}" + colors.ENDC)
        sys.exit()


if __name__ == '__main__':
    main()
