import json
import sys
from typing import Dict, Any
import time
import datetime

from mysql.connector import connect, Error as MysqlError
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
from loguru import logger

# from heucod_event import HEUCODobject, LightGuideEvent

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
        "timestamp": "2021-05-10 23:20:56",        
        "event": "left_bed",
        "patient_id": "041cb23-31f4-4b27-a20b-d160564e2e687",
        "gateway_id": "1fb3b683-7fd5-4581-b201-30ac171e5414"
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
            increment_number_of_visits(toilet_event.get('event_type'), conn)

            with conn.cursor() as cursor:
                try:
                    insert_event_query = f"""
                    INSERT INTO events(timestamp, event_type_id, patient_id, gateway_id)
                    VALUES(
                        '{toilet_event['timestamp']}',
                        (SELECT id FROM event_types WHERE event_type = '{toilet_event['event_type']}'),
                        (SELECT id FROM patients WHERE patient_id = '{toilet_event['patient_id']}'),
                        (SELECT id FROM gateways WHERE gateway_id = '{toilet_event['gateway_id']}'),
                        (SELECT count FROM number_of_visits)
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


def increment_number_of_visits(event_occured: str, conn: MySQLConnection) -> None:
    """ Increments the visit_id in the database if the event_type equals 'left_bed' """
    if event_occured == 'left_bed':
        with conn.cursor() as cursor:
            try:
                update_visit_id_query = f"""
                UPDATE
                    number_of_visits
                SET count = count + 1;
                """
                cursor.execute(update_visit_id_query)
                conn.commit()
                logger.info(f"Updated 'visit_id' in the 'visits' table, as the 'left_bed' occurred.")

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
        if toilet_event.get('timestamp') is None:
            toilet_event['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
