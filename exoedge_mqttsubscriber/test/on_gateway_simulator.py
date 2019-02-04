# pylint: disable=W0212,C0103,C0301
import sys
import threading
import math
import json
import random
from murano_client.client import StoppableThread
from paho.mqtt.client import Client
from time import sleep
from exoedge.sources import waves
from make_config_io import desired_payload_template
from exoedge.sources import waves
from math import pi

sim_lambdas = {
    'pm2p5': lambda t: 1000 * waves._wave_sine(pi/t),
    'pm10': lambda t: 50 * waves._wave_sine(pi/t),
    'ozone': lambda t: 45 * waves._wave_sine(pi/t),
    'carbonMonoxide': lambda t: 35 * waves._wave_sine(pi/t),
    'sulphurousOxide': lambda t: 1 * waves._wave_sine(pi/t),
    'nitrousOxide': lambda t: 1 * waves._wave_sine(pi/t),
    'temp': lambda t: 2 * waves._wave_sine(pi/t),
    'relativeHumidity': lambda t: 30 * waves._wave_sine(pi/t),
    'location': lambda t: json.dumps(
        {"lat": 43.650883+random.uniform(-0.005, 0.005),
         "lng": -96.201642+random.uniform(-0.005, 0.005)})
}


c = Client()
c.connect('127.0.0.1', 1883)
def on_publish(client, userdata, result):
    print("gateway_sim: {} published: {}".format(client.name, result))
c.on_publish = on_publish
c.loop_start()

config_io = json.loads(sys.stdin.read())

class ChannelSim(StoppableThread):
    def __init__(self, **kwargs):
        StoppableThread.__init__(
            self,
            name=kwargs.get('name')
        )
        self.client = kwargs.get('client')
        setattr(self.client, 'name', kwargs.get('name'))
        self.sim_lambda = sim_lambdas[self.name.split('/')[2]]

    def run(self):
        print("running channel simulator: {}".format(self.name))
        nums = range(1, 10)
        while not self.is_stopped():
            for num in nums:
                self.client.publish(
                    self.name,
                    str(self.sim_lambda(num))
                )
                if self.is_stopped():
                    break
                sleep(random.uniform(5.0, 15.0))

for chan in config_io['channels'].keys():
    print("starting channel simulator: {}".format(chan))
    ChannelSim(
        name=config_io['channels'][chan]['protocol_config']['app_specific_config']['positionals'][0],
        client=c
    ).start()

while True:
    try:
        sleep(1.0)
    except KeyboardInterrupt:
        for thread in threading.enumerate():
            if isinstance(thread, StoppableThread):
                thread.stop()
        exit(0)
