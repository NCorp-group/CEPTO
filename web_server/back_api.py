import json
import sys
from typing import Dict, Any
import time
import datetime
import hashlib

from mysql.connector import connect, Error as MysqlError
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import CursorBase
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
from loguru import logger

# from heucod_event import HEUCODobject, LightGuideEvent

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

@logger.catch
def insert_bathroom_event_into_db(bathroom_event: Dict[str, Any]) -> None:
    """
    example object
    bathroom_event = {
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
            increment_number_of_visits(bathroom_event.get('event_type'), conn)

            with conn.cursor() as cursor:
                try:
                    insert_event_query = f"""
                    INSERT INTO events(timestamp, event_type_id, patient_id, gateway_id, visit_id)
                    VALUES(
                        '{bathroom_event['timestamp']}',
                        (SELECT id FROM event_types WHERE event_type = '{bathroom_event['event_type']}'),
                        (SELECT id FROM patients WHERE HEUCOD_patient_id = '{bathroom_event['patient_id']}'),
                        (SELECT id FROM gateways WHERE HEUCOD_gateway_id = '{bathroom_event['gateway_id']}'),
                        (SELECT count FROM number_of_visits)
                    );
                    """
                except KeyError as e:
                    logger.error(f'could not find key: {e} in object bathroom_event')
                    return

                cursor.execute(insert_event_query)
                conn.commit()
                logger.info(f"inserted event: '{bathroom_event['event_type']}' into database")

    except MysqlError as err:
        logger.critical(f"Failure occured when interacting with mariadb database. error message: {err.msg}")


def increment_number_of_visits(event_occured: str, conn: MySQLConnection) -> None:
    """ Increments the visit_id in the database if the event_type equals 'left_bed' """
    if event_occured == 'left_bed':
        with conn.cursor() as cursor:
            try:
                cursor.execute(f'CALL {config["DB_NAME"]}.increment_visit_id();')
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
        bathroom_event = json.loads(msg.payload)    # json.JSONDecoderError
        if bathroom_event.get('timestamp') is None:
            bathroom_event['timestamp'] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        insert_bathroom_event_into_db(bathroom_event)
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
