"""
    An ExoEdge source for interfacing with Modbus TCP devices.
"""
# pylint: disable=W1202,C0111
import sys
import time
import logging
import threading
from exoedge.sources import AsyncSource
import paho.mqtt.client as MQTTClient

logging.getLogger('MQTT_BROKER')
logging.basicConfig(level=logging.DEBUG)

class MQTT_Subscriber(AsyncSource):
    """ Exoedge MQTT Broker source."""
    def __init__(self, **kwargs):
        AsyncSource.__init__(self, **kwargs)
        self.configio_thread = None
        self.channels_by_topic = {}
        for thread in threading.enumerate():
            if thread.name == "ConfigIO":
                self.configio_thread = thread
        for channel_name, channel in self.configio_thread.channels.items():
            if channel['channel'].app_specific_config.get('module') == 'exoedge_mqtt_subscriber':
                the_channel = channel['channel']
                ip_address = channel.app_specific_config['parameters']['ip_address']
                port = the_channel.app_specific_config['parameters']['port']
                # topic = the_channel.positionals[0]
                # exoedge_id = '.'.join(map(str, [ip_address, port, topic]))
                # self.channels_by_exoedge_id[exoedge_id] = channel
                client = MQTTClient()
                setattr(client, 'exoedge_id', channel_name)
                setattr(the_channel, 'client', client)
                def on_message(client, userdata, msg):
                    """ Default on_message function for tunable logging. """
                    logging.info("userdata: {} dup: {} info: {} mid: {} payload: {} qos: {} retain: {} state: {} timestamp: {} topic: {}" # pylint: disable=C0301
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
                    self.configio_thread.channels[client.exoedge_id].put_data(msg.payload)
                    self.configio_thread.channels[client.exoedge_id].e_sync.set()
                the_channel.client.on_message = on_message
                the_channel.client.connect(ip_address, port)

                the_channel.client.loop_start()
                the_channel.client.subscribe(the_channel.app_specific_config['positionals'][0])

    def subscribe(self, *args, **kwargs):
        """ basically this is a no-op """
        logging.warning("subscribe params: {} :: {}".format(args, kwargs))

    def run(self):
        logging.warning("RUNNING@@@!!!")
        while not self.is_stopped():
            time.sleep(0.25)
        logging.critical("{} HAS BEEN STOPPED.".format(self.name))

# set up borg instance of async source
src = MQTT_Subscriber().get_async_source()

# get access to the current module
this_module = sys.modules[__name__]

# register all desired class methods to module
setattr(this_module, 'subscribe', src.subscribe)

logging.critical("current module methods: {}".format(dir(sys.modules[__name__])))
