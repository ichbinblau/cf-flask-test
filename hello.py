import os
import logging
from db import db_session, initial_db
from models import User
from flask import Flask
import requests
import socket
import ssl
import json
from requests.exceptions import ConnectionError, ReadTimeout, SSLError

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello():
    return 'Hello World listening at CloudFoundry port ' + port + '.'


@app.route('/users')
def get_user():
    initial_db()
    u = User('theresa', 'theresa.shan@xxx.com')
    db_session.add(u)
    db_session.commit()
    return 'The first user is ' + db_session.query(User).first().name


@app.route('/get_countries')
def get_countries():
    try :
        r = requests.get('http://services.groupkt.com/country/get/all', proxies={
            'http': 'http://proxy-shm.intel.com:911',
            'https': 'http://proxy-shm.intel.com:911'
        })
    except (ConnectionError, ReadTimeout, SSLError, ssl.SSLError, socket.error) as e:
            return str(e)
    if r.status_code == requests.codes.ok:
        try:
            return json.dumps(r.json())
        except ValueError:
            return "Wrong response format."
    else:
        return "Request failure with code: " + r.status_code


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))