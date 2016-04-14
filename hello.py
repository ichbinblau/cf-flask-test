import os
import logging
from db import db_session, initial_db
from models import User
from flask import Flask, make_response, session, redirect, url_for
import requests
import socket
import ssl
import json
from requests.exceptions import ConnectionError, ReadTimeout, SSLError

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
KEY_SIZE = 32
SECRET_KEY = os.urandom(KEY_SIZE)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/tmp')
def create_tmp():
    import tempfile
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(delete=False) as f:
        path = f.name
        f.write("hello world!")
        f.flush()    # ensure all data written
        return path, tempfile.tempdir


@app.route('/scale_info')
def scale_info():
    inst_index = os.getenv('CF_INSTANCE_INDEX')
    inst_addr = os.getenv('CF_INSTANCE_ADDR')
    env_vars = ['INSTANCE_INDEX', 'INSTANCE_ID', 'HOST', 'PORT']

    res = "<html><body style=\"margin:0px auto; width:80%; font-family:monospace\">"
    res += "<h1>Instance:  <font color =Crimson>{}</font><br>".format(inst_index)
    res += " Address:  <font color=DarkBlue>{}</font></h1>".format(inst_addr)

    res += "<head><title>Application Instance Info</title><meta name=\"viewport\" content=\"width=device-width\"></head>"
    res += "<h2>Application Instance Info</h2>"
    res += "<div><table>"

    env_str = os.getenv("VCAP_APPLICATION", "")
    print "Current env: " + env_str
    env_dict = json.loads(env_str)
    print "Current env keys: " + str(env_dict.keys())

    for key in sorted(env_dict.keys()):
        if str(key).upper() in env_vars:
            value = env_dict[key]
            res += "<tr><td><strong>{}</strong></td><td>{}</tr>".format(key, value)
    res += "</table></div></body></html>"
    return res


@app.route('/')
def sticky_session():
    ret = "VCAP_APPLICATION env var: <br/>" + os.getenv("VCAP_APPLICATION", "") + "<br/>"
    ret += "<br/>"
    ret += "Port: " + os.getenv('PORT', '5000') + "<br/>"
    ret += "Index: " + os.getenv('CF_INSTANCE_INDEX', '') + "<br/>"
    resp = make_response(ret)
    resp.set_cookie('JSESSIONID', 'your secret here.')
    session['test'] = 'test'
    return resp


@app.route('/services')
def get_services():
    vcap_config = os.getenv('VCAP_SERVICES', "")
    decoded_config = json.loads(vcap_config)

    for key, value in decoded_config.iteritems():
        if key.startswith('mysql56'):
            mysql_creds = decoded_config[key][0]['credentials']
        elif key.startswith('rabbitmq33'):
            rabbitmq_creds = decoded_config[key][0]['credentials']

    if mysql_creds:
        mysql_url = str(mysql_creds['uri'])

    if rabbitmq_creds:
        rabbitmq_url = str(rabbitmq_creds['uri'])

    ret = "Mysql connection str is {} <br/> Rabbitmq connection str is {}".format(mysql_url, rabbitmq_url)
    return make_response(ret)


@app.route('/logout')
def logout():
    session.pop('test')
    return redirect(url_for('sticky_session'))


@app.route('/users')
def get_user():
    initial_db()
    u = User('theresa', 'theresa.shan@xxx.com')
    db_session.add(u)
    db_session.commit()
    return 'The first user is ' + db_session.query(User).first().name


@app.route('/get_countries')
def get_countries():
    try:
        r = requests.get('http://services.groupkt.com/country/get/all', proxies={})
    except (ConnectionError, ReadTimeout, SSLError, ssl.SSLError, socket.error) as e:
            return str(e)
    if r.status_code == requests.codes.ok:
        try:
            return json.dumps(r.json())
        except ValueError:
            return "Wrong response format."
    else:
        return "Request failure with code: " + r.status_code


@app.route('/get_time')
def get_server_time():
    # get server time
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return "Today is: " + today

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
