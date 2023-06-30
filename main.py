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

    log = {}
    def callback(ch, method, properties, body:dict):
        print(" [x] Received %r" % body)
        log = f"This is the body : {body}"
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
    



@app.get("/")
def index_logs():
    """Track website visitor."""
    request_time = datetime.now()

    log_visit = {"ip_address":"127.0.0.1",
            "request_url":"http://localhost:8000/",
            "request_port":8000,
            "request_path":"/",
            "request_method":"GET",
            "request_time": request_time,
            "browser_type":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "operating_system":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
    
    #log_format = f"This is the log {log_visit}"
    #bot.send_message(1047727961, log_format)

    return log_visit
            

message_logs = index_logs()

def sendlogs():
    message = "This should be a log"
   
    return message


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your chat ID: {message.chat.id}")

@bot.message_handler(commands=['logs'])
def send_welcome(message):
    bot.reply_to(message, f"Howdy, how are you doing? This is your log: {receiver()}")

  
@bot.message_handler(func=receiver())
def echo_all(message):
    message = sendlogs()
    print(message)
    bot.send_message(1047727961, message)


bot.remove_webhook()

# Set webhook
bot.set_webhook(
    url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    
)




    


if __name__ == "__main__":
    
    app.run(app,
    host="127.0.0.1",
    port=8000)

   