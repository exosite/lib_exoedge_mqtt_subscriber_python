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

    python setup.py install

From Wheel
""""""""""""

The wheel for this hasn't been published yet.

.. code-block::

    $ ./build.sh release
    # lots of output...
    $ pip install dist/*.whl

ExoEdge Configuration
######################

In order to start using this MQTT subscriber source, start the ``edged`` daemon with your desired parameters. For more information on ``edged`` configuration, visit `ExoEdge <https://pypi.org/project/exoedge/>`_ on PyPi.

Example
""""""""

.. code-block::

    edged -H mqtt://f5330e5s8cho0000.m2.exosite.io/ -s mqtt-subscriber-1 -i mqtt-subscriber-1.ini go


ExoSense Configuration
########################

Below is an example ``config_io`` settings that illustrates how mqtt devices or applications cat publish data into ExoEdge channels. Each channel is mapped directly to an MQTT broker and subscription on the network (e.g. ``localhost``->``device/temp``, ``192.168.254.2``->``device/pressure``).

.. code-block:: json

    {
      "channels": {
        "test": {
          "description": "Subscription to MQTT topic <topic> on gateway.",
          "display_name": "test",
          "properties": {
            "data_type": "STRING",
            "max": null,
            "min": null,
            "precision": null
          },
          "protocol_config": {
            "app_specific_config": {
              "ip_address": "localhost",
              "port": 1883,
              "topic": "test"
            },
            "application": "MQTTSubscriber",
            "report_on_change": false,
            "report_rate": 1000,
            "sample_rate": 1000
          }
        },
        "test1": {
          "description": "Subscription to MQTT topic <topic> on gateway.",
          "display_name": "test1",
          "properties": {
            "data_type": "STRING",
            "max": null,
            "min": null,
            "precision": null
          },
          "protocol_config": {
            "app_specific_config": {
              "ip_address": "localhost",
              "port": 1883,
              "topic": "test1"
            },
            "application": "MQTTSubscriber",
            "report_on_change": false,
            "report_rate": 1000,
            "sample_rate": 1000
          }
        }
      }
    }

