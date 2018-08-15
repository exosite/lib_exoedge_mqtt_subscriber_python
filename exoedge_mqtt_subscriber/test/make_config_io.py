# pylint: disable=W0212,C0103
import json
import random

def randomMacAddress():
    """Returns a completely random Mac Address"""
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ''.join(map(lambda x: "%02x" % x, mac))

channel_template = {
    "display_name": "",
    "description": "",
    "properties": {
        "max": None,
        "precision": None,
        "data_type": "STRING",
        "min": None
    },
    "protocol_config": {
        "report_on_change": False,
        "report_rate": 1000,
        "sample_rate": 1000,
        "mode": "async",
        "app_specific_config": {
            "function": "subscribe",
            "parameters": {
                "ip_address": "localhost",
                "port": 1883
            },
            "positionals": ["1"],
            "module": "exoedge_mqtt_subscriber"
        }
    }
}

config_io = {'channels':{}}

desired_payload_template = {
    "pm2p5": None, # ug/m^3 range (h/l/mean): 591x10^6,0,688
    "pm10": None, # ug/m^3 range (h/l/mean): 150,35,54.7
    "ozone": None, # ppm 100,40,45
    "carbonMonoxide": None, # ppm 200,1,35
    "sulphurousOxide": None, # ppm
    "nitrousOxide": None, # ppm
    "temp": None, # Celsius 30,-40,2
    "relativeHumidity": None, # 100,20,30
    "location": {
        "latitude": 44.9778,
        "longitude": 93.2650
    }
}

for i in range(0,4):
    node_id = randomMacAddress()
    for index, (key, value) in enumerate(desired_payload_template.items()):
        chanid = '{}{}'.format(i, index)
        # print("{} {} {}".format(node_id, chanid, key))
        config_io['channels'][chanid] = {
            "display_name": "{}".format(key),
            "description": "Node {} metric for {}.".format(node_id, key),
            "properties": {
                "max": None,
                "precision": None,
                "data_type": "NUMBER" if key != "location" else "LOCATION",
                "min": None
            },
            "protocol_config": {
                "report_on_change": True,
                "report_rate": 1000,
                "sample_rate": 1000,
                "mode": "async",
                "app_specific_config": {
                    "function": "subscribe",
                    "parameters": {
                        "ip_address": "localhost",
                        "port": 1883
                    },
                    "positionals": ["sim/{}/{}".format(node_id, key)],
                    "module": "exoedge_mqtt_subscriber"
                }
            }
        }

if __name__ == '__main__':
    print(json.dumps(config_io))
