from instagrapi import Client
from pathlib import Path
import json
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration variables from environment
unFollowday = int(os.getenv('UNFOLLOW_DAY', 7))  # Number of days before unfollowing users
loginname = os.getenv('LOGIN_NAME', 'your_username')  # Instagram username
password = os.getenv('PASSWORD', 'your_password')  # Instagram password

cl = Client()

# if sessionjson exists, load it
if Path("./session.json").exists():
    cl.load_settings(Path("./session.json"))
    cl.dump_settings(Path("./session.json"))
else:
    cl.login(loginname, password)
    cl.dump_settings(Path("./session.json"))

user_id = cl.user_id_from_username(loginname)
user_info = cl.user_info(user_id)

def load_follows_data():
    """Load existing follows data from follows.json"""
    follows_file = Path("follows.json")
    if follows_file.exists():
        try:
            with open("follows.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_follow_data(user_data):
    """Save follow data to follows.json"""
    follows_data = load_follows_data()
    
    # Add timestamp
    follow_record = {
        "user_id": user_data['pk'],
        "username": user_data['username'],
        "full_name": user_data['full_name'],
        "follow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(time.time())
    }
    
    follows_data.append(follow_record)
    
    # Save to file
    with open("follows.json", "w", encoding="utf-8") as f:
        json.dump(follows_data, f, indent=2, ensure_ascii=False)
    
    return follow_record

def get_users_from_timeline():
    """Get all unique users from timeline that are not already followed"""
    timeline = cl.get_timeline_feed(user_id)
    users = []
    
    # Load existing follows to avoid following again
    existing_follows = load_follows_data()
    followed_user_ids = {str(follow['user_id']) for follow in existing_follows}
    
    for item in timeline['feed_items']:
        if 'media_or_ad' in item:
            media = item['media_or_ad']
            
            # Get main user from the post
            if 'user' in media:
                user = media['user']
                # Only add if not already following, not private, and not already followed by our bot
                if (not user.get('friendship_status', {}).get('following', False) and 
                    not user.get('is_private', True) and 
                    str(user['pk']) not in followed_user_ids):
                    users.append({
                        'pk': user['pk'], 
                        'username': user['username'],
                        'full_name': user.get('full_name', '')
                    })
            
            # Get users from coauthor_producers
            if 'coauthor_producers' in media:
                for coauthor in media['coauthor_producers']:
                    if (not coauthor.get('friendship_status', {}).get('following', False) and 
                        not coauthor.get('is_private', True) and 
                        str(coauthor['pk']) not in followed_user_ids):
                        users.append({
                            'pk': coauthor['pk'], 
                            'username': coauthor['username'],
                            'full_name': coauthor.get('full_name', '')
                        })
            
            # Get tagged users
            if 'usertags' in media and 'in' in media['usertags']:
                for tag in media['usertags']['in']:
                    tagged_user = tag['user']
                    if (not tagged_user.get('is_private', True) and 
                        str(tagged_user['pk']) not in followed_user_ids):
                        users.append({
                            'pk': tagged_user['pk'], 
                            'username': tagged_user['username'],
                            'full_name': tagged_user.get('full_name', '')
                        })
    
    # Remove duplicates based on pk
    unique_users = []
    seen_pks = set()
    for user in users:
        if user['pk'] not in seen_pks:
            unique_users.append(user)
            seen_pks.add(user['pk'])
    
    return unique_users

def follow_random_user():
    """Follow a random user from timeline"""
    try:
        users = get_users_from_timeline()
        
        if not users:
            print("No available users to follow from timeline")
            return
        
        # Pick a random user
        random_user = random.choice(users)
        
        # Follow the user
        result = cl.user_follow(random_user['pk'])
        
        if result:
            # Save follow data to JSON file
            follow_record = save_follow_data(random_user)
            print(f"✅ Successfully followed: @{random_user['username']} ({random_user['full_name']})")
            print(f"📝 Saved to follows.json at {follow_record['follow_date']}")
        else:
            print(f"❌ Failed to follow: @{random_user['username']}")
            
    except Exception as e:
        print(f"❌ Error following user: {str(e)}")

def check_and_unfollow_old_users():
    """Check for users followed more than unFollowday days ago and unfollow them"""
    try:
        follows_data = load_follows_data()
        current_time = int(time.time())
        unfollow_threshold = unFollowday * 24 * 60 * 60  # Convert days to seconds
        
        unfollowed_count = 0
        users_to_remove = []
        
        for follow_record in follows_data:
            # Check if follow is older than unFollowday days
            follow_timestamp = follow_record.get('timestamp', 0)
            time_since_follow = current_time - follow_timestamp
            
            if time_since_follow >= unfollow_threshold:
                try:
                    # Unfollow the user
                    result = cl.user_unfollow(follow_record['user_id'])
                    
                    if result:
                        # Mark for removal from JSON
                        users_to_remove.append(follow_record)
                        print(f"🔄 Unfollowed: @{follow_record['username']} (followed {unFollowday} days ago)")
                        unfollowed_count += 1
                        
                        # Add small delay between unfollows
                        time.sleep(2)
                    else:
                        print(f"❌ Failed to unfollow: @{follow_record['username']}")
                        
                except Exception as e:
                    print(f"❌ Error unfollowing @{follow_record['username']}: {str(e)}")
        
        # Remove unfollowed users from the list
        for user_to_remove in users_to_remove:
            follows_data.remove(user_to_remove)
        
        # Save updated data back to file
        if unfollowed_count > 0:
            with open("follows.json", "w", encoding="utf-8") as f:
                json.dump(follows_data, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Unfollowed and removed {unfollowed_count} users older than {unFollowday} days")
        else:
            print(f"✅ No users to unfollow (none older than {unFollowday} days)")
            
    except Exception as e:
        print(f"❌ Error during unfollow check: {str(e)}")

# Main loop - follow random users every minute
print("🤖 Starting Instagram auto-follow bot...")
print("⏰ Will follow a random person from timeline every minute")
print("🔄 Will check for unfollows every hour")
print("📝 All successful follows will be saved to follows.json")
print("⏹️  Press Ctrl+C to stop")

# Show existing follows count
existing_follows = load_follows_data()
print(f"📊 Currently following: {len(existing_follows)} users")

try:
    cl.delay_range = [1, 5]
    last_unfollow_check = time.time()
    
    while True:
        # Check if it's time for unfollow check (every hour = 3600 seconds)
        current_time = time.time()
        if current_time - last_unfollow_check >= 3600:  # 1 hour
            print("\n🔄 Running hourly unfollow check...")
            check_and_unfollow_old_users()
            last_unfollow_check = current_time
            print("✅ Unfollow check completed\n")
        
        # Follow random user
        follow_random_user()
        cl.load_settings(Path("./session.json"))
        cl.dump_settings(Path("./session.json"))
        print("⏱️  Waiting 60 seconds before next follow...")
        time.sleep(60)  # Wait 60 seconds (1 minute)
        
except KeyboardInterrupt:
    print("\n🛑 Bot stopped by user")
except Exception as e:
    print(f"❌ Bot stopped due to error: {str(e)}")

# Save final timeline for reference
timeline = cl.get_timeline_feed(user_id)
timeline_array = []
for item in timeline['feed_items']:
    timeline_array.append(item)

timeline_json = json.dumps(timeline_array)
with open("timeline.json", "w") as f:
    f.write(timeline_json)
