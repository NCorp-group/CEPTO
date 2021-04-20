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

        self.PIR_occupancy = []
        self.LED_state = []
        self.VIB_state = 0

        for i in len(self.zones):
            self.PIR_occupancy.append(0)
            self.turn_light_off(self.zones[i]['LED'])
            self.LED_state.append(0)

        self.start()

    def start(self):
        sub = mqtt.Client()
        sub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        for i in len(self.zones):
            sub.subscribe(f"zigbee2mqtt/{self.zones[i]['PIR']}", 1)
        sub.subscribe(f"zigbee2mqtt/{self.zones[0]['VIB']}", 1)
        sub.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        

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