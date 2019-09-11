#!/usr/bin/env python3
import datetime
import os
import logging
import uuid
import configparser
import connexion
from connexion.resolver import RestyResolver

from flask import session, request, g
from pony.flask import Pony
#from flask_cors import CORS
from flask_dotenv import DotEnv


from db.models import *


class Server:
    application = None
    app = None

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.connexion_app = connexion.FlaskApp(__name__, specification_dir="./openapi")
        # CORS(self.connexion_app.app, support_credentials=True)
        env = DotEnv()
        env_loc = os.path.join(os.path.dirname(os.path.expanduser(os.path.expandvars(__file__))), '.env')
        env.init_app(self.connexion_app.app, env_file=env_loc, verbose_mode=False)
        # print(self.connexion_app.app.config)

        self.connexion_app.add_api(self.connexion_app.app.config["SWAGGER_FILE"], options={'swagger_ui': False})

        self.port = int(self.connexion_app.app.config['CC_PORT']) or 8080
        self.debug = bool(self.connexion_app.app.config["DEBUG"]) or False

        db.bind(
            provider="postgres",
            user='c3s_admin',
            password='tester',
            host='0.0.0.0',
            database='cs',
            sslmode='disable',
        )
        db.generate_mapping(create_tables=True)

        self.connexion_app.app.secret_key = self.connexion_app.app.config["SECRET_KEY"] or uuid.uuid4()
        Pony(self.connexion_app.app)

        @self.connexion_app.app.after_request
        def apply_cors(response):
            response.headers["Content-Type"] = "application/json"
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "x-api-key, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"
            response.headers["Access-Control-Request-Headers"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, OPTIONS, DELETE"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response

        # @self.connexion_app.app.teardown_appcontext
        # def shutdown_session(exception=None):
        #     orm_handler.db_session.remove()

    def run(self):
        if self.connexion_app.app.config["CC_ENV"] in ["dev", "local", "test", "docker"]:
            print("Running in Debug Mode")
            self.connexion_app.run(port=self.port, debug=True, threaded=True)
        else:
            self.connexion_app.run(port=self.port, debug=self.debug, server="gevent")


s = None

if __name__ == "__main__":
    s = Server()
    s.run()
