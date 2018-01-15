import json
import os
import logging
from flask import Flask, request
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service
import metrics_tracker_client

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
logging.basicConfig(level=logging.FATAL)
port = os.getenv('VCAP_APP_PORT', '5000')

# Global variables for credentials
apikey = ''
classifier_id = ''


# Set Classifier ID
def set_classifier():
    visual_recognition = VisualRecognitionV3('2016-05-20', api_key=apikey)
    classifiers = visual_recognition.list_classifiers()
    for classifier in classifiers['classifiers']:
        if classifier['name'] == 'waste' and classifier['status'] == 'ready':
            return classifier['classifier_id']


# API destination
@app.route('/api/sort', methods=['POST'])
def sort():
    try:
        images_file = request.files.get('images_file', '')
        visual_recognition = VisualRecognitionV3('2016-05-20', api_key=apikey)
        if classifier_id == '':
            global classifier_id
            classifier_id = set_classifier()
            if classifier_id == '':
                return json.dumps(
                    {"status code": 500, "result": "classifier not ready",
                        "confident score": 0})
        parameters = json.dumps({'classifier_ids': [classifier_id]})
        url_result = visual_recognition.classify(images_file=images_file,
                                                 parameters=parameters)
        list_of_result = url_result["images"][0]["classifiers"][0]["classes"]
        result_class = ''
        result_score = 0
        for result in list_of_result:
            if result["score"] >= result_score:
                result_score = result["score"]
                result_class = result["class"]
        return json.dumps(
            {"status code": 200, "result": result_class,
                "confident score": result_score})
    except Exception:
        return json.dumps(
            {"status code": 500, "result": "Not an image",
                "confident score": 0})


# Default frontend page.
@app.route('/')
def default():
    return ''


if __name__ == "__main__":
    visual_creds = watson_service.load_from_vcap_services(
        'watson_vision_combined')
    global apikey
    apikey = visual_creds['api_key']
    metrics_tracker_client.track()
    app.run(host='0.0.0.0', port=int(port))
