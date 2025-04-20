import time
import json

import paho.mqtt.client as paho
from paho import mqtt

class MQTTHandler:
    def __init__(self, broker, port, username, password, mongo_handler, client_id=""):
        self.client = paho.Client(
            client_id=client_id,
            protocol=paho.MQTTv5
        )
        self.client.username_pw_set(username, password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.connect(broker, port)

        self.mongo_handler = mongo_handler

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            timestamp = payload.get("timestamp")
            remaining_loops = payload.get("remaining_loops")
            chunk = payload.get("chunk")
            total_chunks = payload.get("total_chunks")
            data = payload.get("data")

            self.mongo_handler.push_data({
                "timestamp_esp": timestamp,
                "timestamp_mqtt": time.time(),
                "remaining_loops": remaining_loops,
                "chunk": chunk,
                "total_chunks": total_chunks,
                "data": data
            })

        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except KeyError as e:
            print(f"Missing key in payload: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print(f"Subscribed to topic with QoS: {granted_qos}")

    def on_publish(self, client, userdata, mid, properties=None):
        print(f"Message published with mid: {mid}")

    def subscribe(self, topic, qos=1):
        self.client.subscribe(topic, qos)

    def publish(self, topic, payload, qos=1):
        self.client.publish(topic, payload=payload, qos=qos)

    def start(self):
        self.client.loop_forever()
