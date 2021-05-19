from flask import Flask, jsonify
import logging
from flask_cors import CORS
from mysql.connector import connect, Error as MysqlError
from dotenv import dotenv_values
import hashlib
from datetime import datetime

DEBUG = True
MARIADB_PORT = 3306
EVENTS = [
    'leaving_bed',
    'arriving_at_toilet',
    'leaving_toilet',
    'arriving_at_bed',
    'notification'
    'leaving_path'  # OPTIONAL if we have time
]
CONFIG = dotenv_values(".env")
OPTS = {
    "host": CONFIG['DB_HOST'],
    "port": MARIADB_PORT,
    "user": CONFIG['DB_USER'],
    "password": CONFIG['DB_PASS'],
    "database": CONFIG['DB_NAME']
}


class FrontApi:
    def __init__(self):
        # instantiate the app
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)

        # logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

        # enable CORS
        CORS(self.app)
        # CORS(self.app, resources={r'/*': {'origins': '*'}})

        # sanity check route
        @self.app.route('/echo/<txt>', methods=['GET'])
        def echo(txt: str):
            return jsonify({
                "echo": txt,
            })

        @self.app.route('/fetch-events/<usr>,<pwd>', methods=['GET'])
        def fetch_events(usr: str, pwd: str):

            user_hash = login_hash(usr, pwd)

            #### QUERIES ####
            try:
                with connect(**OPTS) as conn:
                    # conn.time_zone = '+00:00'
                    with conn.cursor(buffered=True) as cursor:

                        fetch_events_query = f"""
                        SELECT
                       	    e.timestamp,
                            et.event_type,
                            e.visit_id,
                            e.patient_id,
                            p.full_name
                        FROM events AS e
                        JOIN event_types AS et
                            ON e.event_type_id = et.id
                        JOIN patients AS p
                            ON e.patient_id = p.id
                        WHERE
                            p.id IN (
                                SELECT patient_id
                                FROM caregiver_patient_relation
                                WHERE caregiver_id IN (
                                    SELECT id
                                    FROM caregivers
                                    WHERE username = '{usr}' AND login_credential_hash = '{user_hash}'
                                )
                            )
                        ;
                        """

                        cursor.execute(fetch_events_query)
                        result = cursor.fetchall()

                        if len(result) == 0:
                            raise ValueError()

            except MysqlError as err:
                print(f"sql error: {err}")
                return jsonify({
                    "success": False,
                    "events": []
                })

            except ValueError as err:
                print(
                    f"invalid query arguments (maybe login credentials are incorrect?)")
                return jsonify({
                    "success": False,
                    "events": []
                })

            #### FORMATTING REPLY ####
            events = [
                {
                    # "timestamp": datetime.utcfromtimestamp(event[0]),
                    "timestamp": event[0].isoformat(sep='T',timespec='milliseconds') + '-00:00',
                    "event_type": event[1],
                    "patient_id": event[2],
                    "visit_id": event[3],
                    "patient_full_name": event[4]
                }
                for event in result
            ]

            return jsonify({
                "success": True,
                "events": events
            })

        @self.app.route('/fetch-heucod-events/<usr>,<pwd>', methods=['GET'])
        def fetch_heucod_events(usr: str, pwd: str):
            
            user_hash = login_hash(usr, pwd)

            #### QUERIES ####
            try:
                with connect(**OPTS) as conn:
                    conn.time_zone = '+00:00'
                    with conn.cursor(buffered=True) as cursor:

                        fetch_events_query = f"""
                        SELECT
                            e.timestamp,
                            et.event_type,
                            et.id,
                            p.HEUCOD_patient_id,
                            s.HEUCOD_sensor_id,
                            s.sensor_type,
                            s.device_model,
                            s.device_vendor,
                            g.HEUCOD_gateway_id
                        FROM events AS e
                        JOIN event_types AS et
                            ON e.event_type_id = et.id
                        JOIN patients AS p
                            ON e.patient_id = p.id
                        JOIN gateways AS g
                            ON e.gateway_id = g.id
                        JOIN sensors AS s
                            ON s.gateway_id = g.id
                        WHERE
                            p.id IN (
                                SELECT patient_id
                                FROM caregiver_patient_relation
                                WHERE caregiver_id IN (
                                    SELECT id
                                    FROM caregivers
                                    WHERE username = '{usr}' AND login_credential_hash = '{user_hash}'
                                )
                            )
                        ;
                        """

                        cursor.execute(fetch_events_query)
                        result = cursor.fetchall()

                        if len(result) == 0:
                            raise ValueError()

            except MysqlError as err:
                print(f"sql error: {err}")
                return jsonify({
                    "success": False,
                    "events": []
                })

            except ValueError as err:
                print(
                    f"invalid query arguments (maybe login credentials are incorrect?)")
                return jsonify({
                    "success": False,
                    "events": []
                })

            #### FORMATTING REPLY ####
            events = [
                {
                    # "timestamp": datetime.utcfromtimestamp(event[0]),
                    "timestamp": int(event[0].timestamp()), # UNIX timestamp
                    "event_type": event[1],
                    "event_type_enum": event[2],
                    "patient_id": event[3],
                    "sensor_id": event[4],
                    "sensor_type": event[5],
                    "device_model": event[6],
                    "device_vendor": event[7],
                    "gateway_id": event[8],
                }
                for event in result
            ]

            return jsonify({
                "success": True,
                "events": events
            })
        
        self.app.run(host='0.0.0.0', port=5000)




def login_hash(usr: str, pwd: str) -> str:
    usr_bytes = usr.encode(encoding='ASCII')
    pwd_bytes = pwd.encode(encoding='ASCII')
    return hashlib.sha256(usr_bytes + pwd_bytes).hexdigest()


if __name__ == "__main__":
    api = FrontApi()
