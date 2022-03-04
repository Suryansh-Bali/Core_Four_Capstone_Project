# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:39:38 2022

@author: Neethu
"""

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

key_path = Path('.') / '.keys'
load_dotenv(dotenv_path = key_path)

event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

GROUP_BOT_ID = client.api_call("auth.test")['user_id']

@event_adapter.on('message')
def message(payload):
    ev = payload.get('event',{})
    channelid = ev.get('channel')
    userid = ev.get('user')
    output = ev.get('text')
    
    if GROUP_BOT_ID != userid:    
        client.chat_postMessage(channel=channelid,text=output)

if __name__ == "__main__":
    app.run()