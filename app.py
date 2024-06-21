from flask import Flask, request, render_template, redirect, url_for
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from array import array
from dotenv import load_dotenv
import os
from PIL import Image
import sys
import time
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

subscription_key = os.getenv("VISION_KEY")

endpoint = os.getenv("VISION_ENDPOINT")

app = Flask(__name__)

def ocr(query):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    read_image_url = query
    read_response = computervision_client.read(read_image_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    ans = []
    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                ans.append(line.text)
                # print(line.text)
                # print(line.bounding_box)
    
    return ans


def image_analysis(query):
    client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(subscription_key)
    )

    result = client.analyze_from_url(
    image_url=query,
    visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
    gender_neutral_caption=True,  # Optional (default is False)
    )
    print(" Caption:")
    ans = result.caption.text
    if result.caption is not None:
        print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")
    return ans






@app.route('/')
def home():
    # ocr()
    # image_analysis()
    return render_template('index.html')



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        query = request.form['query']
        query1 = request.form['query1']
        ans = ""
        if(query != ""):
            ans = ocr(query)
        else:
            ans = image_analysis(query1)
        return render_template('index.html' , ans = ans)
    
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)