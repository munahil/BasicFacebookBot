import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    
                    if message_text == "Send Message":
                        send_message(sender_id, "Here is your message!")
                    elif message_text == "Send File":
                        send_attachment(sender_id)
                    elif message_text == "Send Image":
                        send_image(sender_id)
                    elif message_text == "Send Audio":
                        send_audio(sender_id)
                    elif message_text == "Send Video":
                        send_video(sender_id)
                    elif message_text == "Send Carousel":
                        send_carousel(sender_id)
                    elif message_text == "Send Location":
                        send_location(sender_id)
                    else:
                        send_message(sender_id, "Sorry, didn't understand what you are saying. Available Commands are : \n - Send Message \n - Send File \n - Send Image \n - Send Audio \n - Send Video \n - Send Carousel \n - Send Location")
            
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_attachment(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "file",
                "payload": {
                    "url": "http://www.cameronmoll.com/about/cameronmoll_bio.pdf"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_image(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": "http://a.dilcdn.com/bl/wp-content/uploads/sites/6/2013/12/chewie-e1458598236638-1536x864-397101645730.jpg"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_video(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url": "http://techslides.com/demos/sample-videos/small.mp4"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_audio(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "audio",
                "payload": {
                    "url": "http://www.stephaniequinn.com/Music/Allegro%20from%20Duet%20in%20C%20Major.mp3"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_carousel(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "BB 8",
                        "subtitle": "First Object of Carousel",
                        "image_url": "http://d.ibtimes.co.uk/en/full/1435103/star-wars-bb8-robot-toy-by-sphero.jpg",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.twitter.com/",
                            "title": "Go to Twitter"
                        }, {
                            "type": "postback",
                            "title": "Postback",
                            "payload": "Payload for first element in a generic bubble",
                        }],
                    }, {
                        "title": "Darth Vader",
                        "subtitle": "Second Object of Carousel",
                        "image_url": "http://static1.comicvine.com/uploads/original/11127/111278904/5140540-vader.jpg",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.gmail.com/",
                            "title": "Go to gmail",
                        }],
                    }, {
                        "title": "Yoda",
                        "subtitle": "Third Object of Carousel",
                        "image_url": "https://a2ua.com/yoda/yoda-001.jpg",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.instagram.com",
                            "title": "Go to instagram",
                        }],
                    }]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_location(recipient_id):
    
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Please share your location:",
            "quick_replies": [{
                "content_type": "location",
            }]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
