from signal import signal, SIGABRT, SIGINT, SIGTERM
import config
import time
import os
from nanoleaf.UdpStream import *
from nanoleaf.Aurora import *


def clean(*args):
    #clean-ups, e.g shut down your nanoleaf or reset color
    nanoudp.stop_stream()
    os._exit(0)


for sig in (SIGABRT, SIGINT, SIGTERM):
    signal(sig, clean)

nanoleaf_ip = config.nanoleaf_ip
nanoleaf_udp_port = config.nanoleaf_udp_port
nanoleaf_port = config.nanoleaf_port
nanoleaf_auth_token = config.nanoleaf_auth_token

#Get Panels IDs
auroraConnector = Aurora(nanoleaf_ip, nanoleaf_port, nanoleaf_auth_token)
panels = auroraConnector.panel_ids

step = 0

nanoudp = UdpStream(nanoleaf_ip, nanoleaf_port, nanoleaf_udp_port, nanoleaf_auth_token)
nanoudp.start_stream()

while True:
    transition_time = 5

    step = step + 1

    offset = step % 3

    white = 0
    # Flash one panel
    # nanoudp.send_command(panel_id, red, green, blue, white, transition_time)

    # Flash 3 panels at a time
    panel_position = 0
    for panel in panels:
        colorset = (offset + panel_position) % 3
        if colorset == 0:
            red = 255
            green = blue = 0
        elif colorset == 1:
            green = 255
            red = blue = 0
        else:
            red = green = blue = 255

        nanoudp.add_command(panel, red, green, blue, white, transition_time)
        panel_position = panel_position + 1

    nanoudp.send_commands()

    # wait before next step
    time.sleep(1)
