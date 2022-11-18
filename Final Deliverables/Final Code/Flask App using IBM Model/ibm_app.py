import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YIJAXb1Vp23FVn6FxaWNfEECIbjRwptpHaaL7jNGzuTE"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
#from joblib import load
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    #sc = load('scalar.save') 
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5']], "values": x_test }]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/f4aecc62-cd58-47a3-af62-6a940301a611/predictions?version=2022-11-15', json=payload_scoring,
headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    if(output<=9):
        ped="Worst performance with mileage " + str(output) +". Carry extra fuel"
    if(output>9 and output<=17.5):
        ped="Low performance with mileage " +str(output) +". Don't go to long distance"
    if(output>17.5 and output<=29):
        ped="Medium performance with mileage " +str(output) +". Go for a ride nearby."
    if(output>29 and output<=46):
        ped="High performance with mileage " +str(output) +". Go for a healthy ride"
    if(output>46):
        ped="Very high performance with mileage " +str(output)+". You can plan for a Tour"
        
    
    return render_template('index.html', prediction_text='{}'.format(ped))

if __name__ == "__main__":
    app.run(debug=True)