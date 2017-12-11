import json, requests, os
from flask import Flask, Response, abort, request
import atexit
from os import environ as env
import sys

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
logging.basicConfig(level=logging.FATAL)
port = os.getenv('VCAP_APP_PORT', '5000')

f = open("/app/metadata.yml", "r")
raw = f.read()
original = yaml.load(raw)
jsonData = json.loads(json.dumps(original))

@atexit.register
def shutdown():
    if client:
		client.disconnect()

@app.route('/sort', methods=['POST'])
def sort():
		print('received image')
	pass

@app.route('/')
def default():
	try:
		print(request.headers)
	except:
		pass
	return ''
	

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))