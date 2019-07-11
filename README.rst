Description
############

This project is an MQTT source for Exosite's ``ExoSense`` which uses ``ExoEdge``.

With this source installed on a gateway and the ``ExoEdge`` daemon (``edged``) running, any MQTT topic can be subscribed to by specifying it in the `ExoSense Configuration`_ object.

This becomes especially useful in systems where data is published to a local MQTT broker, such as the Multitech LoRaWAN system. In this system, LoRa nodes publish data to MQTT topics on the local ``mosquitto`` daemon (e.g. ``lora/<mac-address>/down``).

The basic design behind this "source" is that each channel is effectively a different topic on the local broker.

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
The topic field can use wildcard ``#`` and ``+``

.. code-block:: json

    {
      "channels": {
        "topic0": {
          "description": "Subscription to MQTT topic <topic> on gateway.",
          "display_name": "topic0",
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
              "topic": "topic0/#"
            },
            "application": "MQTTSubscriber",
            "report_on_change": false,
            "report_rate": 1000,
            "sample_rate": 1000
          }
        },
        "topic1": {
          "description": "Subscription to MQTT topic <topic> on gateway.",
          "display_name": "topic1",
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
              "topic": "topic1"
            },
            "application": "MQTTSubscriber",
            "report_on_change": false,
            "report_rate": 1000,
            "sample_rate": 1000
          }
        }
      }
    }


Test
########################

Using the ``config_io`` above, use the following 3 terminals to test multiple topics on the same broker.

**TODO:** Test multiple brokers at differenct ``IP:PORT``s.

Terminal 1
""""""""""""

.. code-block:: bash

    mosquitto -v

Terminal 2
""""""""""""

.. code-block:: bash

    edged -i edged.ini go

Terminal 3
""""""""""""

.. code-block:: bash

    mosquitto_pub -h localhost -t topic0/zero -m "hello topic0"

.. code-block:: bash

    mosquitto_pub -h localhost -t topic1 -m "hello topic1"
