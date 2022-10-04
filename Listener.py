import configparser
import json
import pytesseract
from PIL import Image
import re
import os
from telethon.errors import SessionPasswordNeededError
import asyncio
from telethon import TelegramClient
from telethon import events
from telethon import sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)

tes = open("OCR_location.txt", "r")
tessa = tes.readline()
pytesseract.pytesseract.tesseract_cmd = tessa
tes.close()

f = open("input.txt", "r")
api_id = f.readline()
api_hash = f.readline()
f.close()

client = TelegramClient('listen', api_id, api_hash)
g = open("channel.txt", "r")
user_input_channel = g.readline()
spec_username = g.readline()
g.close()
c = open("receiver.txt", "r")
receiving_chat = c.readline()
c.close()


w = open("keywords.txt", "r")
words = w.read().splitlines()
w.close()


@client.on(events.NewMessage(chats=user_input_channel))
async def newMessageListener(event):
    newMessage = event.message
    user_id = await event.get_sender()
    if user_id.username == spec_username:
        if newMessage.photo:
            await newMessage.download_media('test.png')
            imageText = pytesseract.image_to_string(Image.open('test.png'))
            imageText = imageText.lower()
            if re.compile('|'.join(words), re.IGNORECASE).search(imageText):
                await client.send_message(entity=receiving_chat, message=event.message)
            os.remove("test.png")



with client:
    client.run_until_disconnected()
