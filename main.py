from signal import signal, SIGABRT, SIGINT, SIGTERM
import config
import requests
import json
import socket
import datetime
import time
import random
import os


def clean(*args):
    #clean-ups, e.g shut down your nanoleaf or reset color
    os._exit(0)


def convert_byte(message, panel_id, red, green, blue, white, transition_time):
    message.append(panel_id.to_bytes(2, byteorder='big'))
    message.append(red.to_bytes(1, byteorder='big'))
    message.append(green.to_bytes(1, byteorder='big'))
    message.append(blue.to_bytes(1, byteorder='big'))
    message.append(white.to_bytes(1, byteorder='big'))
    message.append(transition_time.to_bytes(2, byteorder='big'))
    return message


for sig in (SIGABRT, SIGINT, SIGTERM):
    signal(sig, clean)

nanoleaf_ip = config.nanoleaf_ip
nanoleaf_udp_port = config.nanoleaf_udp_port
nanoleaf_port = config.nanoleaf_port
nanoleaf_auth_token = config.nanoleaf_auth_token
panels = config.panels

# start the stream mode on the nanoleaf
url = "http://" + nanoleaf_ip + ":" + str(nanoleaf_port) + "/api/v1/" + nanoleaf_auth_token + "/effects"
payload = "{\"write\" : {\"command\" : \"display\", \"animType\" : \"extControl\", \"extControlVersion\" : \"v2\"} }"
headers = {
    'Content-Type': 'text/plain'
}
response = requests.request("PUT", url, headers=headers, data=payload)

currentPanel = 0
while True:

    # get the current date / hour / minute
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second

    nbPanels = len(panels)
    message = []
    message.append((0).to_bytes(1, byteorder='big'))

    transition_time = 5

    currentPanel = currentPanel % nbPanels

    panel_id = panels[currentPanel]

    currentPanel = currentPanel + 1

    red = second * 4 + 15
    green = random.randint(1, 135) + minute * 2
    blue = random.randint(1, 255)
    white = 0

    rMESSAGE = convert_byte(message, panel_id, red, green, blue, white, transition_time)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message[0] = (1).to_bytes(2, byteorder='big')
    message = b''.join(message)
    print(f"{panel_id} - {red}, {green}, {blue}")
    sock.sendto(message, (nanoleaf_ip, nanoleaf_udp_port))

    # wait before next step
    time.sleep(1)
