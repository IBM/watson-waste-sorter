import json, requests, os
from flask import Flask, Response, abort, request
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
port = os.getenv('VCAP_APP_PORT', '5000')

# Global variables for credentials
url = ''
apikey = ''

# API destination
@app.route('/api/sort', methods=['POST'])
def sort():
    visual_recognition = VisualRecognitionV3('2016-05-20', api_key=apikey)
    sampleImageUrl = 'https://www.ibm.com/ibm/ginni/images/ginni_bio_780x981_v4_03162016.jpg'
    #sample parameter json
    #{ "classifier_ids": ["watson-waste-sorter-classifier-id"]}
    url_result = visual_recognition.classify(parameters=json.dumps({'url': sampleImageUrl}))
    # print(json.dumps(url_result, indent=2))
    return json.dumps({"status code": 200, "result" : "landfill", "accuracy rate": 90})

# Default frontend page.
@app.route('/')
def default():
    return ''
    

if __name__ == "__main__":
    visual_creds = watson_service.load_from_vcap_services('watson_vision_combined')
    url = visual_creds['url']
    apikey = visual_creds['api_key']
    app.run(host='0.0.0.0', port=int(port))