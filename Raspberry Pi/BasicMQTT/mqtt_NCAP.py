import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "m14.cloudmqtt.com"
MQTT_TOPIC_ROOT = "NCAP1"

TIMS = []

class NCAP:
	def __init__(self, NCAPID=0):
		self.NCAPID = NCAPID
		self.TIMS = []


class TIM:
	def __init__(self, TIM_ID = 0):
		self.Channel = Channel
		self.TIM_ID = TIM_ID

class Channel:
	def __init__(self, ChannelID=0, TransducerType=0, TransducerReading=0):
		self.ChannelID = ChannelID
		self.TransducerType = TransducerType
		self.TransducerReading = TransducerReading





def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	client.subscribe(MQTT_TOPIC_ROOT)

def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

def Initialize_NCAP(NCAP_ID, TIM_ID, ChannelID):
	Channel1 = Channel(1)
	TIM1 = TIM([Channel1], 1)
	NCAP1 = NCAP(1, [TIM1])
	return(NCAP1)
	
NCAP1 = Initialize_NCAP()

NCAP1.TIM1.Channel1.TransducerReading = 100

print(NCAP1.TIM1.Channel1.TransducerReading)




client = mqtt.Client()
client.username_pw_set("wmejyshn", "sKbB0eN90aOx")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 19969, 60)

client.loop_forever()
