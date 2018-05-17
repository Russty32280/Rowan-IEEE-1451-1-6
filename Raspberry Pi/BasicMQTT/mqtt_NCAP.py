import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "m14.cloudmqtt.com"
MQTT_TOPIC_ROOT = "NCAP1/*"


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	client.subscribe(MQTT_TOPIC_ROOT)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.username_pw_set("wmejyshn", "sKbB0eN90aOx")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 19969, 60)

client.loop_forever()
