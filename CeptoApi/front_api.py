from flask import Flask, jsonify
from flask_cors import CORS

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

class FrontApi:
    def __init__(self):
        # instantiate the app
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)

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
            try:
                opts = {
                    "host": config['DB_HOST'],
                    "port": MARIADB_PORT,
                    "user": config['DB_USER'],
                    "password": config['DB_PASS'],
                    "database": config['DB_NAME']
                }

                with connect(**opts) as conn, conn.cursor() as cursor:
                    try:

                    except KeyError as err:
                        print(f"could not find key: {err}")
            
            except MysqlError as err:
                print(f"unknown fatal error when interacting with mariadb database: {err}")


            return jsonify()

        self.app.run()