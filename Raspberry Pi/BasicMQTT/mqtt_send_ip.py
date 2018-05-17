import socket
import fcntl
import struct
import paho.mqtt.client as mqtt
import time

MQTT_SERVER = "m14.cloudmqtt.com"
MQTT_PATH = "NCAP1/IP"

def on_connect(client, userdata, flags, rc):
    print("Connected with Result Code "+str(rc))


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


client = mqtt.Client()
client.username_pw_set("wmejyshn", "sKbB0eN90aOx")
client.on_connect = on_connect

client.connect(MQTT_SERVER, 19969, 60)

while True:

    client.publish(MQTT_PATH, payload=get_ip_address('wlan0'), qos=0, retain=False)
    time.sleep(10)

