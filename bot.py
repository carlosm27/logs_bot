import os
import logging
import telebot
from dotenv import load_dotenv
from main import index_logs
from fastapi import Request

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')



bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your chat ID: {message.chat.id}")

@bot.message_handler(commands=['logs'])
def send_welcome(message):
    message_logs = index_logs(Request)
    print(message)
    bot.reply_to(message, f"Howdy, how are you doing? This is your log: {message_logs}")

def send_logs(logs = index_logs(Request)):
    message = "This is a log"
    bot.send_message(1047727961, message)

@bot.message_handler(func=index_logs(Request))
def echo_all(message):
    message = index_logs(Request)
    bot.send_message(1047727961, message)

bot.infinity_polling()