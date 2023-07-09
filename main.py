from fastapi import FastAPI, Request
from datetime import datetime
import os
import logging
import telebot
from dotenv import load_dotenv
import pika, sys, os



logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_HOST = '<ip/domain>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_URL_BASE = "https://7abf-190-120-248-136.ngrok-free.app"
WEBHOOK_URL_PATH = "/{}/".format(BOT_TOKEN)

app = FastAPI()

bot = telebot.TeleBot(BOT_TOKEN)


def receiver():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='logs')

    def callback(ch, method, properties, body:dict):
        print(" [x] Received %r" % body)
        log = f"This is the log : {body}"
        bot.send_message(1047727961, log)

    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)
   

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



@app.post(f'/{BOT_TOKEN}/')
def process_webhook(update: dict):
    """
    Process webhook calls
    """
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return
    

            


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your chat ID: {message.chat.id}")


  
@bot.message_handler(func=receiver())
def echo_all(message):
    message = "Message sent"
    print(message)
    


bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    
)




    


if __name__ == "__main__":
    
    app.run(app,
    host="127.0.0.1",
    port=5000)

   