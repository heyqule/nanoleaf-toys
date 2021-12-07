import requests
import socket


class UdpStream:
    def __init__(self, ip, port, udp_port, auth_token):
        self.ip = ip
        self.port = port
        self.udp_port = udp_port
        self.auth_token = auth_token
        self.commands = []
        self.message = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_stream(self):
        url = f"http://{self.ip}:{self.port}/api/v1/{self.auth_token}/effects"
        payload = "{\"write\" : {\"command\" : \"display\", \"animType\" : \"extControl\", \"extControlVersion\" : \"v2\"} }"
        headers = {
            'Content-Type': 'text/plain'
        }
        requests.request("PUT", url, headers=headers, data=payload)

    def stop_stream(self):
        url = f"http://{self.ip}:{self.port}/api/v1/{self.auth_token}/state/ct"
        payload = "{\"ct\" : {\"value\": 4500}}"
        headers = {
            'Content-Type': 'text/plain'
        }
        requests.request("PUT", url, headers=headers, data=payload)

    def send_command(self, panel_id, red, green, blue, white, transition_time):
        self.message = []
        self.message.append((0).to_bytes(1, byteorder='big'))
        self.convert_command_to_byteorder(panel_id, red, green, blue, white, transition_time)
        self.message[0] = (1).to_bytes(2, byteorder='big')  # total panel to process
        self.message = b''.join(self.message)
        self.sock.sendto(self.message, (self.ip, self.udp_port))
        self.clear_commands()

    def add_command(self, panel_id, red, green, blue, white, transition_time):
        self.commands.append({
            'panel_id': panel_id,
            'red': red,
            'green': green,
            'blue': blue,
            'white': white,
            'transition_time': transition_time
        })

    def send_commands(self):
        self.message = []
        self.message.append((0).to_bytes(1, byteorder='big'))

        for command in self.commands:
            self.convert_command_to_byteorder(
                command['panel_id'],
                command['red'],
                command['green'],
                command['blue'],
                command['white'],
                command['transition_time']
            )

        self.message[0] = (len(self.commands)).to_bytes(2, byteorder='big')  # total panel to process
        self.message = b''.join(self.message)
        self.sock.sendto(self.message, (self.ip, self.udp_port))
        self.clear_commands()

    def clear_commands(self):
        self.message = []
        self.commands = []

    def convert_command_to_byteorder(self, panel_id, red, green, blue, white, transition_time):
        self.message.append(panel_id.to_bytes(2, byteorder='big'))
        self.message.append(red.to_bytes(1, byteorder='big'))
        self.message.append(green.to_bytes(1, byteorder='big'))
        self.message.append(blue.to_bytes(1, byteorder='big'))
        self.message.append(white.to_bytes(1, byteorder='big'))
        self.message.append(transition_time.to_bytes(2, byteorder='big'))