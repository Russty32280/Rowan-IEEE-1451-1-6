# RosterTest.py
# This code is designed to quickly test the XML Capabilities of python while also providing the bases for Roster Management

import xml.etree.ElementTree as ET
import paho.mqtt.client as mqtt
import time

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

def AddNewTimToRoster(DeviceID, newTIMID):
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


def AddTedsToRoster(timID, numTEDS):
    TEDS = ET.Element("teds")
    timID.append(TEDS)
    TEDS.text = '%s' %(numTEDS)
    tree.write('TIMRoster.xml')




# The callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global NewTIMID
    global root
    if msg.topic == MQTT_PATH:
        print("New TIM Identified")
        if CheckRoster(msg.payload) == -1:
        	# create a new timID and send it to the TIM
        	print("Need new timID")
        	AddNewTimToRoster(msg.payload, NewTIMID)
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
        print(str(AssignedTIMID)+"/TEDS")
	time.sleep(1)
	print("Sending go")
        client.publish((str(AssignedTIMID)+"/TEDS"), "go", qos=2)
        client.subscribe((str(NewTIMID)+"/TEDS"), 2)
    elif msg.topic == "1/TEDS":
	    if msg.payload != "go":
		    for child in root:
			print(child.find("timID").text+"/TEDS")
			print(msg.topic)
        		if msg.topic == (child.find("timID").text+"/TEDS"):
	            		# update the roster with the number of TEDS sent by the tim
	            		print("Adding number of TEDS to roster")
		    		print("child.find" + child.find("timID").text)
	            		AddTedsToRoster(child, msg.payload)
    print("End of on_Message")
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
