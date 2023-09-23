import network
import binascii
import socket
from time import sleep
import machine

ssid = 'Mobile bill ni ayya kadthada'
password = 'sriyank12'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

try:
    wlan = network.WLAN() #  network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan() # list with tupples with 6 fields ssid, bssid, channel, RSSI, security, hidden
    i=0
    networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
    for w in networks:
          i+=1
          print(i,w[0].decode(),binascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5])
    connect()
except KeyboardInterrupt:
    machine.reset()