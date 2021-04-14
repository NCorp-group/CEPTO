import paho.mqtt.client as mqtt
import json
import signal
from threading import Event, Thread
import time

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
        self.subscriber_thread = Thread(target=self.start, daemon=True)
        self.subscriber_thread.start()
        #self.start()
    
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
        message = '{"state":"ON"}'
        pub.publish("zigbee2mqtt/light_strip/set", message, 1)
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
        hour = int(time.strftime('%H'))
        if(((self.pir1_occupancy == True or self.pir2_occupancy == True) and not(self.light_state)) and not ((hour >= 0 and hour <= 7) or (hour >= 23 and hour <= 24))):
            self.turn_light_on()
            self.light_state = True
        elif((self.pir1_occupancy == False and self.pir2_occupancy == False and self.light_state) or (hour >= 0 and hour <= 7) or (hour >= 23 and hour <= 24)): # Time between 23 and 7
            self.turn_light_off()
            self.light_state = False


my_home = SmartHome() 

stop_daemon = Event()

def shutdown(signal, frame):
    stop_daemon.set();

signal.signal(signal.SIGHUP, shutdown)
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

while not stop_daemon.is_set():
    stop_daemon.wait(60)

my_home.turn_light_off()