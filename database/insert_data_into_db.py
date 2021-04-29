import json
import sys
from typing import Dict, Any

from mysql.connector import connect, Error as MysqlError
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
from loguru import logger

from heucod_event import HEUCODobject, LightGuideEvent

# import pprint
# pp = pprint.PrettyPrinter(indent=4)

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

EVENTS = [
    'leaving_bed',
    'arriving_at_toilet',
    'leaving_toilet',
    'arriving_at_bed',
    'notification'
    'leaving_path' # OPTIONAL if we have time
]



@logger.catch
def insert_toilet_event_into_db(toilet_event: Dict[str, Any]) -> None:
    """
    example object
    toilet_event = {
        "event": EVENTS,
        "user": {
            "full_name": "Elderly",
            "date_of_birth": '1940-01-01',
        },
    'time_of_occurence': '2021-04-24 23:22:56'
    }
    """
        
    try:
        opts = {
            "host": config['DB_HOST'],
            "port": MARIADB_PORT,
            "user": config['DB_USER'],
            "password": config['DB_PASS'],
            "database": config['DB_NAME']
        }
        with connect(**opts) as conn:
            logger.info(f"established connection with mariadb database: {config['DB_NAME']}")
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
                    logger.error(f'could not find key: {e} in object toilet_event')
                    return

                cursor.execute(insert_event_query)
                conn.commit()
                logger.info(f"inserted event: '{toilet_event['event_type']}' into database")

    except MysqlError as err:
        logger.critical(f"Failure occured when interacting with mariadb database. error message: {err.msg}")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc) -> None:
    logger.info(f"Connected to the broker with result code: {str(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    result, msg_id = client.subscribe(SUB_TOPIC)
    if result is not mqtt.MQTT_ERR_SUCCESS:
        logger.critical(f'Subscription to topic: {SUB_TOPIC} failed, msg_id is: {msg_id}')



def on_message(client, userdata, msg) -> None:
    """The callback for when a PUBLISH message is received from the server."""

    logger.info(f'Message received on topic: {msg.topic}')

    try:
        toilet_event = json.loads(msg.payload)    # json.JSONDecoderError
        insert_toilet_event_into_db(toilet_event)
    except json.JSONDecodeError as err:
        logger.error(f"Could not parse json msg.payload. {err.msg}")


if __name__ == '__main__':
    logger.info('Starting logging:')
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(config['MOSQUITTO_HOST'], 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    mqtt_client.loop_forever()
