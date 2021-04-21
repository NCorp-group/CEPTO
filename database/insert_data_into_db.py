from mysql.connector import connect, Error
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import signal
import time
from threading import Event, Thread
from datetime import datetime
import json
# import logging
import sys
from loguru import logger
from typing import Dict, Any, List

config = dotenv_values(".env")

SUB_TOPIC = 'light_guide/events'
MARIADB_PORT = 3306
DB = 'testdb'

MQTT_BROKER_PORT = 1883

log_opts = {
	'format': "{time} {level} {message}",
	'filter': __name__,
	'level': 'INFO'
}

logger.add(sys.stderr, colorize=True, **log_opts)
logger.add('file_{time}.log', **log_opts)

# log_opts = {
# 	'level': logging.INFO,
# 	'filename': 'app.log',
# 	'filemode': 'w', # write, use 'a' for append
# 	'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# 	'datefmt': '%d-%b-%y %H:%M:%S'
# }

# logging.basicConfig(**log_opts)

# logger = logging.getLogger(__name__)
# logger.warning('this is a warning')

EVENTS = [
	'leaving_bed',
	'arriving_at_toilet',
	'leaving_toilet',
	'arriving_at_bed',
	'notification'
	'leaving_path' # OPTIONAL if we have time
]

# print(datetime.now())

@logger.catch
def insert_toilet_event_into_db(toilet_event: Dict[str, Any]) -> None:
	"""
	example object
	toilet_event = {
		"event": EVENTS,
		"user": {
			"full_name": "Elderly",
			"age": 70,
		},
		'timestamp': datetime.now()
	}

	an exception of type ValueError will be trown, if the toilet_event does not adhere to
	this.
	"""

	# TODO do type check

	user = {}
	try:
		user = toilet_event['user']
	except KeyError as e:
		logger.exception("could not find user object in toilet_event object")
		return

	try:
		opts = {
			"host": config['DB_HOST'],
			"port": MARIADB_PORT,
			"user": config['DB_USER'],
			"password": config['DB_PASS'],
			"database": DB
		}
		with connect(**opts) as conn:
			user_id = -1
			with conn.cursor() as cursor:
				insert_event_query = f"""
				INSERT INTO {event}(timestamp, user_id)
				VALUES({timestamp}, (SELECT user_id from users WHERE full_name = '{full_name}'))
				"""
				cursor.execute(insert_event_query)
				cursor.commit()
				# get_user_id_query = f'SELECT user_id FROM users WHERE full_name = "{user["full_name"]}"'
				# cursor.execute(get_user_id_query)
				# user_id = cursor.fetchall()[0]
				# logger.info(f'user_id is {user_id}')



				# cursor.execute("INSERT INTO users(full_name, age) VALUES('Henrik', 56)")
				# conn.commit()
				# conn.rollback()

			# insert_toilet_visit_query = """
			# INSERT INTO events(day, leaving_bed, arriving_at_toilet, leaving_toilet, arriving_at_bed)
			# VALUES( %s, %s, %s, %s, %s )
			# """

	except Error as e:
		print(e)
		raise e




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc) -> None:
    logger.info(f"Connected to the broker with result code: {str(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    result, msg_id = client.subscribe(SUB_TOPIC)
	if result is not mqtt.MQTT_ERR_SUCCESS:
		logger.critical(f'Subscription to topic: {SUB_TOPIC} failed, msg_id is: {msg_id}')



# The callback for when a PUBLISH message is received from the server.
@logger.catch
def on_message(client, userdata, msg) -> None:
	logger.info(f'Message received on topic: {msg.topic}')

	if not event in EVENTS:
		pass
    
	try:
		toilet_event = json.loads(msg.payload)    # json.JSONDecoderError
		insert_toilet_event_into_db(toilet_event) # ValueError
	except json.JSONDecodeError as e:
		logger.exception(e)
	except ValueError as e:
		logger.exception(e)



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



# if __name__ == '__main__':
# 	stop_daemon = Event()

# 	# def shutdown(signal, frame): 
# 	# 	stop_daemon.set()

# 	shutdown = lambda signal, frame: stop_daemon.set()

# 	# Subscribe to signals sent from the terminal, so that the application is shutdown properly.
#     # When one of the trapped signals is captured, the function shutdown() will be execute. This
#     # will set the stop_daemon event that will then stop the loop that keeps the application running.
#     signal.signal(signal.SIGHUP, shutdown)
#     signal.signal(signal.SIGINT, shutdown)
#     signal.signal(signal.SIGTERM, shutdown)

# 	while not stop_daemon.is_set():
#         # The event times out evey 60 seconds, or when the event is set. If it is set, then the loop
#         # will stop and the application will exit.
#         stop_daemon.wait(60)