import json
import os
import logging
from flask import Flask, request
from watson_developer_cloud import VisualRecognitionV3
from watson_developer_cloud import watson_service

app = Flask(__name__, static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True
logging.basicConfig(level=logging.FATAL)
port = os.getenv('VCAP_APP_PORT', '5000')

# Global variables for credentials
apikey = ''
classifier_id = ''


# Set Classifier ID
def set_classifier():
    visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey=apikey)
    classifiers = visual_recognition.list_classifiers()
    for classifier in classifiers['classifiers']:
        if classifier['name'] == 'waste':
            if classifier['status'] == 'ready':
                return classifier['classifier_id']
            else:
                return ''
    create_classifier()
    return ''


# Create custom waste classifier
def create_classifier():
    visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey=apikey)
    with open('./resources/landfill.zip', 'rb') as landfill, open(
        './resources/recycle.zip', 'rb') as recycle, open(
            './resources/compost.zip', 'rb') as compost, open(
                './resources/negative.zip', 'rb') as negative:
        visual_recognition.create_classifier(
            'waste',
            Landfill_positive_examples=landfill,
            Recycle_positive_examples=recycle,
            Compost_positive_examples=compost,
            negative_examples=negative)
    return ''


# API destination
@app.route('/api/sort', methods=['POST'])
def sort():
    try:
        images_file = request.files.get('images_file', '')
        visual_recognition = VisualRecognitionV3('2018-03-19',
                                                 iam_apikey=apikey)
        global classifier_id
        if classifier_id == '':
            classifier_id = set_classifier()
            if classifier_id == '':
                return json.dumps(
                    {"status code": 500, "result": "Classifier not ready",
                        "confident score": 0})
        parameters = json.dumps({'classifier_ids': [classifier_id]})
        url_result = visual_recognition.classify(images_file=images_file,
                                                 parameters=parameters)
        if len(url_result["images"][0]["classifiers"]) < 1:
            return json.dumps(
                    {"status code": 500, "result": "Image is either not "
                        "a waste or it's too blurry, please try it again.",
                        "confident score": 0})
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
    apikey = visual_creds['apikey']
    classifier_id = set_classifier()
    app.run(host='0.0.0.0', port=int(port))
