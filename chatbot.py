import telebot
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

# Global instances
global redis1
global chatgpt

# Load config
config = configparser.ConfigParser()
config.read('config.ini')

# Initialize bot
bot = telebot.TeleBot(config['TELEGRAM']['ACCESS_TOKEN'])

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Redis
redis1 = redis.Redis(
    host=config['REDIS']['HOST'],
    password=config['REDIS']['PASSWORD'],
    port=config['REDIS']['REDISPORT'],
    decode_responses=config['REDIS']['DECODE_RESPONSE'],
    username=config['REDIS']['USER_NAME']
)

# Initialize ChatGPT
chatgpt = HKBU_ChatGPT(config)

# ChatGPT handler for normal messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    if message.text.startswith('/'): # Skip commands
        return
    
    # Get response from ChatGPT
    reply_message = chatgpt.submit(message.text)
    logging.info(f"Message: {message}")
    bot.reply_to(message, reply_message)

# Help command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    """Send a message when the command /help is issued."""
    bot.reply_to(message, 'Helping you helping you.')

# Add command handler
@bot.message_handler(commands=['add'])
def add_command(message):
    """Send a message when the command /add is issued."""
    try:
        # Split message text to get the keyword after /add
        command_parts = message.text.split()
        if len(command_parts) < 2:
            raise IndexError
            
        msg = command_parts[1]  # Get the keyword after /add
        redis1.incr(msg)
        count = redis1.get(msg).decode('UTF-8')
        bot.reply_to(message, f'You have said {msg} for {count} times.')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Usage: /add <keyword>')

@bot.message_handler(commands=['hello'])
def hello_command(message):
    """Send a greeting when the command /hello is issued."""
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            bot.reply_to(message, 'Usage: /hello <name>')
            return
        name = command_parts[1]  
        bot.reply_to(message, f'Good day, {name}!')
    except Exception as e:
        bot.reply_to(message, 'Usage: /hello <name>')

def main():
    # Start the bot
    logging.info("Bot started...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()