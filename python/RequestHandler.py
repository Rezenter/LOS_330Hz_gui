import logging
import socket

import python.subsyst.laser1064 as laser1064


def __init__():
    return


UDP_IP = "192.168.10.41"
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((UDP_IP, UDP_PORT))

laser_maxTime = 60 + 10  # seconds
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


class Handler:
    def __init__(self):
        self.HandlingTable = {
            'laser': {
                'connect': self.las_connect,
                'status': self.las_status,
                'fire': self.las_fire,
                'idle': self.las_idle
            }
        }
        self.las = laser1064.Chatter()
        self.state = {}
        return

    def handle_request(self, req):
        subsystem = req['subsystem']
        if subsystem not in self.HandlingTable:
            return {'ok': False, 'description': 'Subsystem is not listed.'}
        reqtype = req['reqtype']
        if reqtype in self.HandlingTable[subsystem]:
            return self.HandlingTable[subsystem][reqtype](req)
        else:
            return {'ok': False, 'description': 'Reqtype is not listed.'}

    def las_connect(self, req):
        self.state['las'] = self.las.connect(req['ip'])
        return self.state['las']

    def las_status(self, req):
        self.state['las'] = self.las.status()
        return self.state['las']

    def las_fire(self, req):
        self.state['las'] = self.las.set_state_3()
        return self.state['las']

    def las_idle(self, req):
        self.state['las'] = self.las.set_state_1()
        return self.state['las']
