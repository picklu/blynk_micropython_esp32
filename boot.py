"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Sketch generator:           http://examples.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to initialize your ESP8266/ESP32 board
and connect it to Blynk.

"""

import network
import machine
from credentials import *


wifi = network.WLAN(network.STA_IF)
if not wifi.isconnected():
    print("Connecting to WiFi...")
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        pass

print('IP:', wifi.ifconfig()[0])

