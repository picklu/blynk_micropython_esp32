import network
import credentials as creds


station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(creds.ssid, creds.password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

ap_id = "newtower"
ap_password = "WhatIsThePassWord"
ap_if = network.WLAN(network.AP_IF)
ap_if.config(essid=ap_id, authmode=network.AUTH_WPA2_PSK, password=ap_password)

print('Access point (AP) is ready! Type info() to get detail of the AP')

def info():
    print(f"id: {ap_id} & password: {ap_password}")


