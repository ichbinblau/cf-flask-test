import os
import pprint
import logging
from flask import Flask

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    return 'Hello World at cf port' + port + '!'
	#pprint.pformat(str(os.environ))

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))