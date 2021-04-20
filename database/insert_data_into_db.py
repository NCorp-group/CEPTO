from mysql.connector import connect, Error
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import signal
import time
from threading import Event, Thread
from datetime import datetime
import json
import logging
from typing import Dict, Any, List

config = dotenv_values(".env")

SUB_TOPIC = 'light_guide/events'
MARIADB_PORT = 3306
DB = 'testdb'

MQTT_BROKER_PORT = 1883


log_opts = {
	'level': logging.INFO,
	'filename': 'app.log',
	'filemode': 'w', # write, use 'a' for append
	'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	'datefmt': '%d-%b-%y %H:%M:%S'
}

logging.basicConfig(**log_opts)

logger = logging.getLogger(__name__)
logger.warning('this is a warning')


def insert_toilet_event_into_db(toilet_event: Dict[str, Dict[str, Any]]) -> None:
	"""
	example object
	"""
	pass



try:
	opts = {
		"host": config['DB_HOST'],
		"port": MARIADB_PORT,
		"user": config['DB_USER'],
		"password": config['DB_PASS'],
		"database": DB
	}
	with connect(**opts) as conn:
		with conn.cursor() as cursor:
			# cursor.execute(use_db_query)
			cursor.execute('SELECT * FROM users')
			for row in cursor:
				print(row)
			# cursor.execute("INSERT INTO users(full_name, age) VALUES('Henrik', 56)")
			# conn.commit()
			# conn.rollback()

		insert_toilet_visit_query = """
		INSERT INTO events(day, leaving_bed, arriving_at_toilet, leaving_toilet, arriving_at_bed)
		VALUES( %s, %s, %s, %s, %s )
		"""

		toilet_visit_records = [
			# (time.day)
		]

except Error as e:
	print(e)
	raise e

# with connect(host="localhost", )

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to the broker with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUB_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):


    print(msg.topic + " " + str(msg.payload))
	# insert_toilet_event_into_db()


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.enable_logger()


mqtt_client.connect(config['MOSQUITTO_HOST'], 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()



if __name__ == '__main__':
	stop_daemon = Event()

	# def shutdown(signal, frame): 
	# 	stop_daemon.set()

	shutdown = lambda signal, frame: stop_daemon.set()

	# Subscribe to signals sent from the terminal, so that the application is shutdown properly.
    # When one of the trapped signals is captured, the function shutdown() will be execute. This
    # will set the stop_daemon event that will then stop the loop that keeps the application running.
    signal.signal(signal.SIGHUP, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

	while not stop_daemon.is_set():
        # The event times out evey 60 seconds, or when the event is set. If it is set, then the loop
        # will stop and the application will exit.
        stop_daemon.wait(60)