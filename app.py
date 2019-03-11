import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = #page_token

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods = ['GET'])
def verify():

    #Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        #verify_token is hello
        if not request.args.get("hub.verify_token") == "hello":
            return "verification token mismatch", 430
        return request.args["hub.challenge"], 200
    return "Hello world", 200

#for processing messeges sent by fb app
@app.route('/', methods = ['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
          for entry in data['entry']:
              for messaging_event in entry['messaging']:

                  #ID's
                  sender_id = messaging_event['sender']['id']
                  recipient_id = messaging_event['recipient']['id']

                  if messaging_event.get('message'):
                      if 'text' in messaging_event['message']:
                          messaging_text = messaging_event['message']['text']
                      else:
                          messaging_text = 'no text'

                      #witbot
                      response = None

                      entity, value = wit_response(messaging_text)

                      if entity == "languageName":
                          response = "Ok, I will teach you {0}".format(str(value))
                      if entity == "location":
                          response = "Ok, you live in {0}. I will send you top headlines from your location".format(str(value))
                      if entity == "greetings":
                          response = "Hello, I am Ayush's page"
                      if entity == "name_type":
                          response = "Oh, hello {0}".format(str(value))
                      if response == None:
                          response = "Sorry, I didn't understand"
                      bot.send_text_message(sender_id, response)

    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()



if __name__ == "__main__":
    app.run(debug = True, port = 80)
