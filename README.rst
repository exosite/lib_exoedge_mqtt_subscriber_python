Description
############

This project is an MQTT source for Exosite's ``ExoSense`` which uses ``ExoEdge``.

This source can be published to by any MQTT publish on ``localhost:1883``.


Example
""""""""

.. code-block::



Install
#########

From Source
""""""""""""

.. code-block::

    pip install -r requirements.txt
    python setup.py install

From PyPi
""""""""""""

The wheel for this hasn't been published yet.

.. code-block::

    pip install exoedge_mqtt_broker

ExoEdge Configuration
######################

In order to start using this MQTT Broker source, start the ``edged`` daemon with your desired parameters. For more information on ``edged`` configuration, visit `ExoEdge <https://pypi.org/project/exoedge/>`_ on PyPi.

Example
""""""""

.. code-block::

    edged -H mqtt://f5330e5s8cho0000.m2.exosite.io/ -s mqtt-broker-1 -i mqtt-broker-1.ini go


ExoSense Configuration
########################

Below is an example ``config_io`` settings that illustrates how mqtt devices or applications cat publish data into ExoEdge channels. Each channel is mapped directly to an MQTT subscription on the network (e.g. `localhost`, `192.168.254.2`).

**Important:** Modbus is a ``channels.$id.protocol_config.mode.poll`` type source. Setting the mode to ``async`` or ``async2`` will not work.

.. code-block:: json

    {
      "channels": {
        "<topic>": {
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

Schema For ``app_specific_config``
""""""""""""""""""""""""""""""""""""

**!!! TODO !!!**

.. code-block:: yaml

