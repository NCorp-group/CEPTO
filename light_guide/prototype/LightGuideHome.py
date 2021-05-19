import paho.mqtt.client as mqtt
from threading import Thread
from enum import Enum
import datetime
import time
import json

class UserState(Enum):
    IN_BED = 1
    TO_BATHROOM = 2
    IN_BATHROOM = 3
    TO_BED = 4


class LightGuard:
    def __init__(self):
        # Reading the information from config.json
        fileObject = open("light_guide/prototype/config.json", "r")
        jsonContent = fileObject.read()
        self.room_info = json.loads(jsonContent)["room_info"]
        self.zones = json.loads(jsonContent)["zones"]

        self.mqtt_server_ip = "192.168.0.124"
        self.mqtt_server_port = 1883
        self.max_allowed_time = 60 * 30 # A bathroom visit can take a max time of 30 minutes

        # The model
        self.state = UserState.IN_BED
        self.pir_occupancy = []
        self.led_state = []

        # For each zone in config.json, turn the light strip off and initialize the arrays for led's and pir sensors
        for i in range(0, len(self.zones)):
            self.pir_occupancy.append(False)
            self.led_state.append(True)
            self.turn_light_off(self.zones[i]['led'])

        # Subscribing to all PIR sensors
        sub = mqtt.Client()
        sub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        for i in range(0, len(self.zones)):
            sub.subscribe(f"zigbee2mqtt/{self.zones[i]['pir']}", 1)
        sub.on_message = self.on_message
        print("Waiting for events")
        sub.loop_start()

        self.logic()

    def on_message(self, client, userdata, msg):
        dictionary = json.loads(msg.payload)    # The message itself
        print(msg.topic.split("/")[1], "->", dictionary["occupancy"])
        if("pir" in msg.topic):
            for i in range(0, len(self.zones)):
                if(msg.topic == f"zigbee2mqtt/{self.zones[i]['pir']}"):
                    self.pir_occupancy[i] = dictionary["occupancy"]
        

    # Assumptions: 
    # 1. Person starts in bed
    # 2. Has to walk all the way to and from bathroom thorugh the zones
    # 3. There are at least 3 zones in the system
    def logic(self):
        while(True):
            if(self.state == UserState.IN_BED):

                # Check if the first PIR sensor reports occupancy TRUE
                if(self.pir_occupancy[0] == True):
                    self.turn_light_on(self.zones[0]['led'])
                    self.turn_light_on(self.zones[1]['led'])
                    self.state = UserState.TO_BATHROOM
                    self.event("left_bed")
                    self.start_timer = time.time()
                    self.timer_active = True

            if(self.state == UserState.TO_BATHROOM):
                # Make sure the timer is not exeeded.
                if(time.time() - self.start_timer > self.max_allowed_time and self.timer_active == True):
                    self.event("notification")
                    self.timer_active == False
                # If the last PIR sensor is occupied, change state to in bathroom
                if(self.pir_occupancy[len(self.zones)-1] == True):
                    self.state = UserState.IN_BATHROOM
                    self.event("arrived_at_bathroom")
                    print("Timeout for bathroom visit for 75 seconds")
                    time.sleep(75)
                    print("Ready to go back to bed")
                # If any of other zone is oocupied, checked from bathroom to the bed
                else:
                    for i in range(len(self.zones)-1, 0, -1):
                        if(self.pir_occupancy[i] == True):
                            self.turn_light_on(self.zones[i+1]['led'])
                            for j in range(0, i):
                                self.turn_light_off(self.zones[j]['led'])
                            break

            if(self.state == UserState.IN_BATHROOM):
                # Make sure the timer is not exeeded.
                if(time.time() - self.start_timer > self.max_allowed_time and self.timer_active == True):
                    self.event("notification")
                    self.timer_active == False

                if(self.pir_occupancy[len(self.zones)-2] == True):
                    self.turn_light_off(self.zones[len(self.zones)-1]["led"])
                    self.turn_light_on(self.zones[len(self.zones)-3]["led"])
                    self.state = UserState.TO_BED
                    self.event("left_bathroom")

            if(self.state == UserState.TO_BED):
                # Make sure the timer is not exeeded.
                if(time.time() - self.start_timer > self.max_allowed_time and self.timer_active == True):
                    self.event("alert")
                    self.timer_active == False
                
                # If bed pir sensor is occupant, change state to in bed
                if(self.pir_occupancy[0] == True):
                    self.state = UserState.IN_BED
                    self.event("arrived_at_bed")
                    self.turn_light_off(self.zones[1]['led'])
                    print("Turning off all lights in 10 seconds")
                    time.sleep(10)
                    for i in range(0, len(self.zones)):
                        self.turn_light_off(self.zones[i]['led'])
                    print("Program state resetting in 75 seconds")
                    self.timer_active = False
                    self.start_timer = 0
                    time.sleep(75)
                    print("Program state reset complete")
                else:
                    for i in range(0, len(self.zones)-2):
                        if(self.pir_occupancy[i] == True):
                            self.turn_light_on(self.zones[i-1]['led'])
                            for j in range(i+1, len(self.zones)):
                                self.turn_light_off(self.zones[j]['led'])
              
# Event functions:
    def event(self, event):
        print("Sending event:", event)
        pub = mqtt.Client()
        pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        message = {
            "event_type": event,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_id": self.room_info["patient_id"],
            "gateway_id": self.room_info["gateway_id"]
        }
        pub.publish("light_guide/events/add", json.dumps(message), 1)
        pub.disconnect()
    
    def turn_light_off(self, led_fname):
        for i in range(0, len(self.zones)):
            if(led_fname == self.zones[i]['led'] and self.led_state[i] == True):
                print("Turning", led_fname, "off")
                pub = mqtt.Client()
                pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
                message = '{"state":"OFF"}'
                pub.publish(f"zigbee2mqtt/{led_fname}/set", message, 1)
                self.led_state[i] = False
                pub.disconnect()

    def turn_light_on(self, led_fname):
        for i in range(0, len(self.zones)):
            if(led_fname == self.zones[i]['led'] and self.led_state[i] == False):
                print("Turning", led_fname, "on")
                pub = mqtt.Client()
                pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
                message = {
                    "state": "ON"
                }
                #message = '{"state":"ON"}'
                pub.publish(f"zigbee2mqtt/{led_fname}/set", json.dumps(message), 1)
                self.led_state[i] = True
                pub.disconnect()

guard = LightGuard()