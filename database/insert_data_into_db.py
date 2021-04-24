from mysql.connector import connect, Error as MysqlError
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
import pprint

pp = pprint.PrettyPrinter(indent=4)

config = dotenv_values(".env")

MARIADB_PORT = 3306
MQTT_BROKER_PORT = 1883

SUB_TOPIC = config['MOSQUITTO_SUB_TOPIC']

log_opts = {
    'format': "{time} {level} {message}",
    'filter': __name__,
    'level': 'INFO'
}

logger.add(sys.stdout, colorize=True, **log_opts)
# logger.add('file_{time}.log', **log_opts)

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

# @logger.catch
def insert_toilet_event_into_db(toilet_event: Dict[str, Any]) -> None:
    """
    example object
    toilet_event = {
        "event": EVENTS,
        "user": {
            "full_name": "Elderly",
            "date_of_birth": '1940-01-01',
        },
        'time_of_occurence': datetime.now()
    }

    an exception of type ValueError will be trown, if the toilet_event does not adhere to
    this.
    """
        
    # user = {}
    # try:
    #     user = toilet_event['user']
    # except KeyError as e:
    #     logger.exception("could not find user object in toilet_event object")
    #     # return

    # event_type = ''
    # try:
    #     event_type = toilet_event['event_type']
    # except KeyError as e:
    #     logger.exception("could not find 'event' key in toilet_event object")
    #     return

    # keys = ['event', 'user', 'time_of_occurence']
    # if not all([key in toilet_event for key in keys]):
    # #if not all(map(lambda key: key in toilet_event, keys)):
    #     return

    try:
        opts = {
            "host": config['DB_HOST'],
            "port": MARIADB_PORT,
            "user": config['DB_USER'],
            "password": config['DB_PASS'],
            "database": config['DB_NAME']
        }
        with connect(**opts) as conn:
            logger.info(f"established with connection with mariadb database:{config['DB_NAME']}")
            with conn.cursor() as cursor:
                try:
                    insert_event_query = f"""
                    INSERT INTO events(time_of_occurence, user_id, event_type_id)
                    VALUES(
                        '{toilet_event['time_of_occurence']}',
                        (SELECT user_id FROM users WHERE full_name = '{toilet_event['user']['full_name']}'),
                        (SELECT event_type_id FROM event_types WHERE event_type = '{toilet_event['event_type']}')
                    );
                    """
                except KeyError as e:
                    logger.exception(f'could not find key: {e} in object toilet_event')
                    return

                cursor.execute(insert_event_query)
                conn.commit()
                logger.info(f"inserted event: '{toilet_event['event_type']}' into database")

    except MysqlError as e:
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

    try:
        toilet_event = json.loads(msg.payload)    # json.JSONDecoderError
        insert_toilet_event_into_db(toilet_event) # ValueError
    except json.JSONDecodeError as e:
        logger.exception(e)
    except ValueError as e:
        logger.exception(e)



if __name__ == '__main__':
    logger.info('Starting logging:')
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # mqtt_client.enable_logger()

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
