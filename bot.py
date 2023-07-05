import os
import logging
import telebot
from dotenv import load_dotenv
from main import index_logs
from fastapi import Request
from receive import receiver
import pika, sys, os
   

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)



load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL_BASE = "https://7abf-190-120-248-136.ngrok-free.app"
WEBHOOK_URL_PATH = "/{}/".format(BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

def receiver():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='logs')

    def callback(ch, method, properties, body:dict):
        print(" [x] Received %r" % body)
        log = f"This is the body : {body}"
        bot.send_message(1047727961, log)

    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
   

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()




@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your chat ID: {message.chat.id}")



bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    
)