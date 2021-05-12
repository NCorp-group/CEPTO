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

            usr_bytes = usr.encode(encoding='ASCII')
            pwd_bytes = pwd.encode(encoding='ASCII')
            user_hash = hashlib.sha256(usr_bytes + pwd_bytes).hexdigest()

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

                    fetch_events_query = f"""
                    SELECT  
                        e.timestamp,
                        e.event_type_id, 
                        e.patient_id,
                        e.visit_id,
                        p.full_name
                    FROM
                        events AS e
                    INNER JOIN
                        patients AS p
                        ON
                            e.patient_id = p.patient_id
                    WHERE 
                        p.id IN (
                            SELECT patient_id
                            FROM caregiver_patient_relation
                            WHERE caregiver_id IN (
                                SELECT id
                                FROM caregivers
                                WHERE username = '{usr}' AND login_credential_hash = '{user_hash}'
                            )
                    );
                    """

                    cursor.execute(fetch_events_query)
                    result = cursor.fetchall()

                    if len(result) == 0:
                        raise ValueError()
            
            except MysqlError as err:
                print(f"sql error: {err}")
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
                    "visit_id": event[3],
                    "patient_full_name": event[4]
                }
                for event in result
            ]

            return jsonify({
                "success": True,
                "events": events
            })

        self.app.run()


if __name__ == "__main__":
    api = FrontApi()
