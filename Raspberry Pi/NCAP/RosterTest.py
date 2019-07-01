# RosterTest.py
# This code is designed to quickly test the XML Capabilities of python while also providing the bases for Roster Management

import xml.etree.ElementTree as ET 
import paho.mqtt.client as mqtt


tree = ET.parse('TIMRoster.xml')
root = tree.getroot()

for child in root:
	print(child.tag,child.attrib)

for timID in root.iter('timID'):
	print timID.text

MQTT_SERVER = "localhost"
MQTT_PATH = "NewTim"

NewTIMID = 1

def CheckRoster(DeviceID):
	tree = ET.parse('TIMRoster.xml')
	root = tree.getroot()
	for child in root:
			print(child.attrib)
			print(DeviceID)
			print(child.find('mac_address').text)
			if child.find('mac_address').text == DeviceID:
				print("Device Previously Connected")
				return child.find('timID').text
	print("Device Not Previously Connected")
	return -1

def AddToRoster(DeviceID, newTIMID):
	newTIM = ET.Element("tim")
	newTIM.text = '\n'
	root.append(newTIM)
	macAddress = ET.Element("mac_address")
	newTIM.append(macAddress)
	macAddress.text='%s' %(DeviceID)
	timID = ET.Element("timID")
	newTIM.append(timID)
	timID.text = '%s' %(newTIMID)
	tree.write('TIMRoster.xml')





# The callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global NewTIMID
    if msg.topic == MQTT_PATH:
        print("New TIM Identified")
        if CheckRoster(msg.payload) == -1:
        	# create a new timID and send it to the TIM
        	print("Need new timID")
        	AddToRoster(msg.payload, NewTIMID)
        	AssignedTIMID = NewTIMID
   	        NewTIMID = NewTIMID + 1
   	        # The New TIM ID needs to not exist in the roster
    	else:
    		# get old timID and assign it
    		print("has old timID")
    		AssignedTIMID = CheckRoster(msg.payload)

        client.unsubscribe(MQTT_PATH)
        client.publish(MQTT_PATH, str(AssignedTIMID))
        client.subscribe(MQTT_PATH)
        print("Assigned New TIM ID: " + str(AssignedTIMID))
        client.subscribe(str(NewTIMID))

    print(msg.topic+" "+str(msg.payload))
    # more callbacks, etc

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
