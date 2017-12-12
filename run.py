import json, requests, os
from flask import Flask, Response, abort, request
import atexit
from os import environ as env
import sys
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
port = os.getenv('VCAP_APP_PORT', '5000')

@staticmethod
def get_vcap_credentials(vcap_env, service):
    if service in vcap_env:
        vcap_conversation = vcap_env[service]
        if isinstance(vcap_conversation, list):
            first = vcap_conversation[0]
            if 'credentials' in first:
                return first['credentials']

@atexit.register
def shutdown():
    if client:
		client.disconnect()

@app.route('/sort', methods=['POST'])
def sort():
	print('received image')

@app.route('/')
def default():
	try:
		print(request.headers)
	except:
		pass
	return ''
	

if __name__ == "__main__":
    vcap_services = os.environ.get("VCAP_SERVICES")
    if vcap_services:
        vcap_env = json.loads(vcap_services)
    if vcap_env:
    	visual_creds = WatsonEnv.get_vcap_credentials(vcap_env, 'watson_vision_combined')
	app.run(host='0.0.0.0', port=int(port))