from telegram.ext import Updater, CommandHandler
import tweepy
import os
import time

# Twitter/X API credentials
TWITTER_API_KEY = "your_api_key"
TWITTER_API_SECRET = "your_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Telegram Bot Token
TELEGRAM_TOKEN = "your_telegram_bot_token"

def init_twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def check_new_follows(api, user_id, last_follows):
    user = api.get_user(user_id)
    current_follows = set(api.get_friend_ids(user_id))
    new_follows = current_follows - last_follows
    
    if new_follows:
        new_follow_users = [api.get_user(uid) for uid in new_follows]
        return new_follow_users
    return []

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Bot started! Monitoring for new follows..."
    )

def main():
    # Initialize APIs
    twitter_api = init_twitter_api()
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Start monitoring
    target_user_id = "target_twitter_user_id"
    last_follows = set(twitter_api.get_friend_ids(target_user_id))
    
    while True:
        try:
            new_follows = check_new_follows(twitter_api, target_user_id, last_follows)
            for user in new_follows:
                message = f"New follow detected: @{user.screen_name}"
                updater.bot.send_message(chat_id="your_chat_id", text=message)
            
            last_follows = set(twitter_api.get_friend_ids(target_user_id))
            time.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == '__main__':
    main()