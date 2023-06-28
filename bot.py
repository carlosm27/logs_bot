import os
import logging
import telebot
from dotenv import load_dotenv

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')



bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your chat ID: {message.chat.id}")


def send_logs():
    message = "This is a log"
    bot.send_message(1047727961, message)

@bot.message_handler(func=send_logs())
def echo_all(message):
    message = "This is a log"
    bot.send_message(1047727961, message)

bot.infinity_polling()