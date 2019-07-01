"""
    An ExoEdge source for interfacing with Modbus TCP devices.
"""
# pylint: disable=W1202,C0111,C0301,C0103
import sys
import time
import logging
import threading
from exoedge.sources import ExoEdgeSource
from exoedge import logger
from paho.mqtt.client import Client as MQTTClient

LOG = logger.getLogger(__name__, level=logging.getLogger('exoedge').getEffectiveLevel())

class MqttsubscriberExoEdgeSource(ExoEdgeSource):
    """ Exoedge MQTT Broker source."""
    def __init__(self, **kwargs):
        super(MqttsubscriberExoEdgeSource, self).__init__(**kwargs)
        self.mqtt_clients = {}

    def run(self):
        LOG.critical("Starting")
        mqtt_channels = {e.name: e for e in self.get_channels_by_application("MQTTSubscriber")}

        LOG.critical("mqtt_channels: {}".format(dir(mqtt_channels)))

        for channel_name, channel in mqtt_channels.items():
            LOG.critical("CHANNEL NAME: {}".format(channel_name))
            LOG.critical("CHANNEL: {}".format(dir(channel)))
            ip_address = channel.protocol_config.app_specific_config['ip_address']
            port = channel.protocol_config.app_specific_config['port']
            if ip_address not in self.mqtt_clients:
                client = MQTTClient()
                self.mqtt_clients[ip_address] = client

            if not hasattr(client, 'channels'):
                setattr(client, 'channels', {})

            self.mqtt_clients[ip_address].channels[channel.protocol_config.app_specific_config['topic']] = channel
            def on_message(client, userdata, msg):
                """ Default on_message function for tunable logging. """
                LOG.debug("userdata: {} dup: {} info: {} mid: {} payload: {} qos: {} retain: {} state: {} timestamp: {} topic: {}"
                          .format(userdata,
                                  msg.dup,
                                  msg.info,
                                  msg.mid,
                                  msg.payload,
                                  msg.qos,
                                  msg.retain,
                                  msg.state,
                                  msg.timestamp,
                                  msg.topic))
                LOG.critical("{}->{} got {}".format(client, client.channels[msg.topic].name, msg.payload))
                client.channels[msg.topic].put_sample(msg.payload)
            self.mqtt_clients[ip_address].on_message = on_message
            self.mqtt_clients[ip_address].connect(ip_address, port)

        for client in self.mqtt_clients.values():
            client.loop_start()
            for channel in client.channels.values():
                client.subscribe(channel.protocol_config.app_specific_config['topic'])

        while not self.is_stopped():
            time.sleep(0.25)

        for client in self.mqtt_clients.values():
            client.loop_stop()

        LOG.critical("{} HAS BEEN STOPPED.".format(self.name))
