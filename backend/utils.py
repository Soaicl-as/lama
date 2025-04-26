import random
import time
from instagram import InstagramBot

def send_messages(bot, recipient_usernames, message, delay_min, delay_max):
    for username in recipient_usernames:
        bot.send_message(username, message)
        delay = random.randint(delay_min, delay_max)
        time.sleep(delay)
