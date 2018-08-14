import sys
import threading
import math
from murano_client.client import StoppableThread
from paho.mqtt.client import Client
from time import sleep
from exoedge.sources import waves


""" # subscribe to mosquitto daemon
c = Client()
c.connect('127.0.0.1', 1883)
def on_message(client, userdata, msg):
 print(msg)
c.on_message = on_message
c.subscribe('will')
c.loop_start()
while True:
 sleep(1)
"""

c = Client()
c.connect('127.0.0.1', 1883)
def on_publish(client, userdata, result):
    print("gateway_sim: {} published: {}".format(client.name, result))
c.on_publish = on_publish
c.loop_start()

num_channels = int(sys.argv[1]) if len(sys.argv) > 0 else 1

class ChannelSim(StoppableThread):
    def __init__(self, **kwargs):
        StoppableThread.__init__(
            self,
            name=kwargs.get('name')
        )
        self.client = kwargs.get('client')
        setattr(self.client, 'name', kwargs.get('name'))

    def run(self):
        nums = [math.pi/r for r in range(1, 100)]
        while not self.is_stopped():
            for num in nums:
                self.client.publish(
                    self.name,
                    str(waves._wave_sine(num))
                )
                if self.is_stopped():
                    break
                sleep(0.5)

for i in range(0, num_channels):
    ChannelSim(
        name=str(i),
        client=c
    ).start()

try:
    while True:
        sleep(0.5)
except KeyboardInterrupt:
    for thread in threading.enumerate():
        thread.stop()
    exit(0)
