# test.py for ranger
# publish 4 pictures to ranger mqtt topic
# print response
import sys
import json
import argparse
import warnings
import os
import os.path
import paho.mqtt.client as mqtt
import time
from PIL import Image
import io
import base64


pub = f'homie/turret_tracker/ranger/image/set'
sub = f'homie/turret_tracker/ranger/distance/set'

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(topic, payload)
    

def image_to_byte_array(image: Image) -> bytes:
  # BytesIO is a file-like buffer stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file-like as a argument
  image.save(imgByteArr, format=image.format)
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


client = mqtt.Client("ranger test", False)
client.on_message = on_message
client.connect("stoic.local", 1883)
client.loop_start()
client.subscribe(sub)

for fpath in ["images/yes1.jpg", "images/no1.jpg", "images/no2.jpg","images/yes2.jpg"]:
  image = Image.open(fpath)
  wid = image.width
  hgt = image.height
  # convert image to bytearray
  ba = image_to_byte_array(image)
  # then base64 because it's just easier to deal with on the server
  bfr = base64.b64encode(ba)
  client.publish(pub, bfr)
  print(wid,hgt)
  time.sleep(0.5)

