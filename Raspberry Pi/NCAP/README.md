# MQTT Based NCAP with Roster

This folder contains the work associated with creating a IEEE 1451 NCAP based on MQTT. 

## Registering New TIMs
Whenever a TIM initially turns on in an IEEE 1451 network, it will need to broadcast to any available NCAPs that it is looking to be connected. From there, if an NCAP is available, it will then begin to register the device to the network.

When dealing with MQTT, this is accomplished in the following steps.

### Initial Broadcast
In our example, any TIM that wishes to connect to our broker first needs to PUBLISH to the "NewTim" topic. We are assuming that there is only one TIM attempting to connect at the same time. Simultaneous initial broadcast may cause an issue, so it is vital to minimize the amount of time spent on this NewTim topic.

#### 7/1/2019 Update
Currently the TIM is expected to send its WiFi Mac Address as a means of identifying itself. This will aid in the NCAP being able to manage the different TIM IDs which are allocated. This may have ot be shifted in accordance to the IEEE 1451 standard.

### Roster Check
The NCAP maintains an XML based roster of each device which has connected to it. It can use this to manage the distributed TIM IDs and aid in the reconnection of devices. Currently, the only information which is kept is the MAC Address and the associated TIM ID allocated previously by the NCAP. An example of the XML structure used can be seen below.

```xml
<roster>
	<tim>
		<mac_address>AA:BB:CC:DD:EE:FF</mac_address>
		<timID>ESP8266-NNN</timID>
	</tim>
</roster>
```

If a device has been connected previously, once it attempts to initialize with the NCAP, it will check this roster and then use the previously allocated TIM ID. If the device is new or the Mac Address is not found, it will add the new device to the list and apply a new TIM ID which is not shared with any other devices. 