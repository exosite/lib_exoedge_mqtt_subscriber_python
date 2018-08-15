Description
############

This project is an MQTT source for Exosite's ``ExoSense`` which uses ``ExoEdge``.

With this source installed on a gateway and the ``ExoEdge`` daemon (``edged``) running, any MQTT topic can be subscribed to by specifying it in the `ExoSense Configuration`_ object.

This becomes especially useful in systems where data is published to a local MQTT broker, such as the Multitech LoRaWAN system. In this system, LoRa nodes publish data to MQTT topics on the local ``mosquitto`` daemon (e.g. ``lora/<mac-address>/down``).


Install
#########

From Source
""""""""""""

.. code-block::

    pip install -r requirements.txt
    python setup.py install

From Github
""""""""""""

The wheel for this hasn't been published yet.

.. code-block::

    pip install git+https://github.com/exosite/lib_exoedge_mqtt_subscriber_python.git

ExoEdge Configuration
######################

In order to start using this MQTT subscriber source, start the ``edged`` daemon with your desired parameters. For more information on ``edged`` configuration, visit `ExoEdge <https://pypi.org/project/exoedge/>`_ on PyPi.

Example
""""""""

.. code-block::

    edged -H mqtt://f5330e5s8cho0000.m2.exosite.io/ -s mqtt-subscriber-1 -i mqtt-subscriber-1.ini go


ExoSense Configuration
########################

Below is an example ``config_io`` settings that illustrates how mqtt devices or applications cat publish data into ExoEdge channels. Each channel is mapped directly to an MQTT subscription on the network (e.g. `localhost`, `192.168.254.2`).

**Important:** This ``ExoEdge`` source is a ``channels.$id.protocol_config.mode.sync`` type source. Setting the mode to ``poll`` or ``async2`` will not work.

.. code-block:: json

    {
      "channels": {
        "<id>": {
          "display_name": "<topic>",
          "description": "Subscription to MQTT topic <topic> on gateway.",
          "properties": {
            "max": null,
            "precision": null,
            "data_type": "STRING",
            "min": null
          },
          "protocol_config": {
            "report_on_change": true,
            "report_rate": 1000,
            "sample_rate": 1000,
            "mode": "async",
            "app_specific_config": {
              "function": "subscribe",
              "parameters": {
                "ip_address": "localhost",
                "port": 1883  ,
              },
              "positionals": ["<topic>"],
              "module": "exoedge_mqtt_subscriber"
            }
          }
        }
      }
    }

