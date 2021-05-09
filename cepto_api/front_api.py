from flask import Flask, jsonify
import logging
from flask_cors import CORS
from mysql.connector import connect, Error as MysqlError
from dotenv import dotenv_values
import hashlib

DEBUG = True
MARIADB_PORT = 3306
EVENTS = [
    'leaving_bed',
    'arriving_at_toilet',
    'leaving_toilet',
    'arriving_at_bed',
    'notification'
    'leaving_path' # OPTIONAL if we have time
]

CONFIG = dotenv_values(".env")

class FrontApi:
    def __init__(self):
        # instantiate the app
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)

        # logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

        # enable CORS
        CORS(self.app, resources={r'/*': {'origins': '*'}})

        # sanity check route
        @self.app.route('/echo/<txt>', methods=['GET'])
        def echo(txt: str):
            return jsonify({
                "echo":txt,
            })

        @self.app.route('/fetch-events/<usr>,<pwd>', methods=['GET'])
        def fetch_events(usr: str, pwd: str):

            usr = usr.encode(encoding='ASCII')
            pwd = pwd.encode(encoding='ASCII')
            user_hash = hashlib.sha256(usr + pwd).hexdigest()
            authorized = False
            active_caregiver_id = None

            #### QUERIES ####
            try:
                opts = {
                    "host": CONFIG['DB_HOST'],
                    "port": MARIADB_PORT,
                    "user": CONFIG['DB_USER'],
                    "password": CONFIG['DB_PASS'],
                    "database": CONFIG['DB_NAME']
                }

                with connect(**opts) as conn, conn.cursor(buffered=True) as cursor:
                    fetch_caregivers_query = """
                    SELECT *
                    FROM caregivers;
                    """

                    cursor.execute(fetch_caregivers_query)
                    result = cursor.fetchall()


                    for caregiver in result:
                        if caregiver[2] == usr and caregiver[3] == user_hash:
                            return jsonify(f"{user_hash} == {caregiver[3]}")
                            authorized = True
                            active_caregiver_id = caregiver[1]
                            break

                    if not authorized:
                        raise ValueError()

                    fetch_events_query = f"""
                    SELECT  events.timestamp, events.event_type_id, 
                            events.patient_id, patients.full_name
                    FROM events
                    INNER JOIN patients
                    ON events.patient_id=patients.patient_id;
                    WHERE events.patient_id IN (
                        SELECT patient_id
                        FROM caregiver_patient_relation
                        WHERE caregiver_id = '{active_caregiver_id}'
                    );
                    """

                    cursor.execute(fetch_events_query)
                    result = cursor.fetchall()

            
            except MysqlError as err:
                print(f"unknown fatal error when interacting with mariadb database: {err}")
                return jsonify({
                    "success":False,
                    "events":[]
                })
            
            except ValueError as err:
                print(f"invalid query arguments (maybe login credentials are incorrect?)")
                return jsonify({
                    "success":False,
                    "events":[]
                })
            
            #### FORMATTING REPLY ####
            events = [
                {
                    "timestamp": event[0],
                    "event_type_id": event[1],
                    "patient_id": event[2],
                    "patient_full_name": event[3]
                }
                for event in result
            ]

            return jsonify({
                "success":True,
                "events":events
            })

        self.app.run()


if __name__ == "__main__":
    api = FrontApi()