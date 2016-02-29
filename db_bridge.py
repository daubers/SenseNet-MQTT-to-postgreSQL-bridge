from paho.mqtt import client
import models
from models.store import Store

import paho.mqtt.client as mqtt
from threading import Thread


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")


class WriteMessage(Thread):
    def __init__(self, topic, payload):
        Thread.__init__(self)
        self.topic = topic
        self.payload = payload

    def run(self):
        session = models.get_session()
        store_entry = Store()
        store_entry.payload = self.payload.decode("utf-8")
        store_entry.topic = self.topic
        session.add(store_entry)
        session.commit()


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    thread = WriteMessage(msg.topic, msg.payload)
    thread.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
