import paho.mqtt.client as mqtt
from threading import Thread
from enum import Enum
import time
import json

class LightGuard:
    def __init__(self):
        # Reading the devices from the 
        fileObject = open("devices.json", "r")
        jsonContent = fileObject.read()
        self.zones = json.loads(jsonContent)

        self.mqtt_server_ip = "127.0.0.1"
        self.mqtt_server_port = 1883


        # The model
        self.pir_occupancy = []
        self.led_state = []

        for i in len(self.zones):
            self.PIR_occupancy.append(False)
            self.turn_light_off(self.zones[i]['led'])
            self.LED_state.append(False)

        # Starting routine
        self.subscriber_thread = Thread(target=self.start, daemon=True)
        # Thread callback away from main process
        self.subscriber_thread.start()
        # This is the main logic
#        logic()

    def start(self):
        sub = mqtt.Client()
        sub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        for i in len(self.zones):
            sub.subscribe(f"zigbee2mqtt/{self.zones[i]['pir']}", 1)
        sub.subscribe(f"zigbee2mqtt/{self.zones[0]['vib']}", 1)
        sub.on_message = self.on_message
        print("Waiting for events")
        sub.loop_forever()

    def on_message(self, client, userdata, msg):
        dictionary = json.loads(msg.payload)    # The message itself

        if("pir" in msg.topic):
            for i in len(self.zones):
                if(msg.topic == f"zigbee2mqtt/{self.zones[i]['pir']}"):
                    self.PIR_occupancy[i] = dictionary["occupancy"]
        
#    def logic():

#    def event_leaving_bed():
#    def event_arriving_at_toilet():
#    def event_leaving_toilet():
#    def event_arriving_at_bed():
#    def event_notification():
    #OPTIONAL: def event_leaving_path():

    
    def turn_light_off(self, PIR_fname):
        print("Turning light off")
        pub = mqtt.Client()
        pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        message = '{"state":"OFF"}'
        pub.publish(f"zigbee2mqtt/{PIR_fname}/set", message, 1)
        pub.disconnect()

    def turn_light_on(self, PIR_fname):
        print("Turning light on")
        pub = mqtt.Client()
        pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        message = {
            "state": "ON",
            "color": {
            "x": 0.7025,
            "y": 0.3737
            }
        }
        #message = '{"state":"ON"}'
        pub.publish(f"zigbee2mqtt/{PIR_fname}/set", json.dumps(message), 1)
        #pub.publish("zigbee2mqtt/light_strip/set", message, 1)
        pub.disconnect()