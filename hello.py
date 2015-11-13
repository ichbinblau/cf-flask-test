import os
import logging
from db import db_session, initial_db
from models import User
from flask import Flask

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

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))