import paho.mqtt.client as mqtt
import json

class SmartHome:

    def __init__(self):
        self.mqtt_server_ip = "192.168.0.127"
        self.mqtt_server_port = 1883
        self.pir1_occupancy = bool
        self.pir2_occupancy = bool
        self.light_state = bool

        # Turning light strip OFF
        pub = mqtt.Client()
        pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        message = '{"state":"OFF"}'
        pub.publish("zigbee2mqtt/light_strip/set", message, 1)
        pub.disconnect()
        self.light_state = False

        # Starting routine
        self.start()
    
    def turn_light_off(self):
        print("Turning light off")
        pub = mqtt.Client()
        pub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        message = '{"state":"OFF"}'
        pub.publish("zigbee2mqtt/light_strip/set", message, 1)
        pub.disconnect()

    def turn_light_on(self):
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
        pub.publish("zigbee2mqtt/light_strip/set", json.dumps(message), 1)
        #pub.publish("zigbee2mqtt/light_strip/set", message, 1)
        pub.disconnect()

    def on_message(self, client, userdata, msg): # Updating the correct variables
        dictionary = json.loads(msg.payload)
        print("Occupancy", dictionary["occupancy"] ,"recieved from", msg.topic.split("/")[1])
        if(msg.topic == "zigbee2mqtt/pir_sensor1"):
            self.pir1_occupancy = dictionary["occupancy"] 
        elif(msg.topic == "zigbee2mqtt/pir_sensor2"):
            self.pir2_occupancy = dictionary["occupancy"]
        self.update_mqtt()

    def start(self):
        sub = mqtt.Client()
        sub.connect(self.mqtt_server_ip, self.mqtt_server_port)
        sub.subscribe("zigbee2mqtt/pir_sensor1", 1)
        sub.subscribe("zigbee2mqtt/pir_sensor2", 1)
        sub.on_message = self.on_message
        print("Waiting for events")
        sub.loop_forever()
        
    def update_mqtt(self):
        if((self.pir1_occupancy == True or self.pir2_occupancy == True) and not(self.light_state)):
            self.turn_light_on()
            self.light_state = True
        elif(self.pir1_occupancy == False and self.pir2_occupancy == False and self.light_state):
        #elif(self.pir1_occupancy == False and self.light_state):
            self.turn_light_off()
            self.light_state = False

my_home = SmartHome() 