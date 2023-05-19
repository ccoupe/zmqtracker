#!/usr/bin/env python3
import json
import socket
from uuid import getnode as get_mac
import os 
import sys

class Settings:

  def __init__(self, log, etcf):
    self.etcfname = etcf
    self.log = log
    self.mqtt_server = "192.168.1.7" 
    self.mqtt_port = 1883
    self.mqtt_client_name = "tracker_1"
    self.homie_device = None
    self.homie_name = None
    self.turrets = []     # list of dicts.
    # IP and MacAddr are not important (should not be important).
    if sys.platform.startswith('linux'):
      self.hostname = f'{socket.gethostname()}.local'
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      s.connect(('<broadcast>', 0))
      self.our_IP =  s.getsockname()[0]
      # from stackoverflow (of course):
      self.macAddr = ':'.join(("%012x" % get_mac())[i:i+2] for i in range(0, 12, 2))
    elif sys.platform.startswith('darwin'):
      self.hostname = socket.gethostname()
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      self.our_IP = s.getsockname()[0]
      self.macAddr = ':'.join(("%012x" % get_mac())[i:i+2] for i in range(0, 12, 2))
    else:
      self.our_IP = "192.168.1.255"
      self.macAddr = "de:ad:be:ef"
    self.macAddr = self.macAddr.upper()
    self.load_settings(self.etcfname)
    self.log.info("Settings from %s" % self.etcfname)

    
  def load_settings(self, fn):
    conf = json.load(open(fn))
    if conf["mqtt_server_ip"]:
      self.mqtt_server = conf["mqtt_server_ip"]
    if conf["mqtt_port"]:
      self.mqtt_port = conf["mqtt_port"]
    if conf["mqtt_client_name"]:
      self.mqtt_client_name = conf["mqtt_client_name"]
    if conf['homie_device']:
      self.homie_device = conf['homie_device']
    if conf['homie_name']:
      self.homie_name = conf['homie_name']
    self.image_port = conf.get('image_port', 4783)
    self.turrets = conf.get('turrets', None)
    self.confidence = conf.get('confidence', 0.40)
    self.http_port = conf.get('http_port', 4795)
    self.do_rtsp = conf.get('provide_rtsp', False)
    

  def print(self):
    self.log.info("==== Settings ====")
    self.log.info(self.settings_serialize())
  
  def settings_serialize(self):
    st = {}
    st['mqtt_server_ip'] = self.mqtt_server
    st['mqtt_port'] = self.mqtt_port
    st['mqtt_client_name'] = self.mqtt_client_name
    st['homie_device'] = self.homie_device 
    st['homie_name'] = self.homie_name
    st['image_port'] = self.image_port
    st['turrets'] = self.turrets
    st['confidence'] = self.confidence
    st['provide_rtsp'] = self.do_rtsp
    st['http_port'] = self.http_port
    return st
    
  def settings_deserialize(self, jsonstr):
    st = json.loads(jsonstr)
