import xgboost as xgb
import numpy as np
import json
from oracle import Oracle
from datetime import datetime
from calendar import day_name
import itertools

from flask import Flask, jsonify, request
from flask import request, Response
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

filename = 'input.csv'
predictor = Oracle(filename)
threshold = 0.75 #  or 0.75
@app.route('/predict', methods=['GET'])
def getPredictions():
    with open(filename) as f:
        lines = f.read().split('\n')
        preds = []
        for pred, line in itertools.izip(predictor.predict(), lines):
            # Case of empty string from empty \n
            if line and pred > threshold:
                line = line.split(',')
                specialty, id, date, patientName, phoneNum, resourceName  = line[12], line[4], line[2], line[-3], line[-2], line[-1]
                preds.append({
                    'specialty':specialty, 
                    'patientName': patientName,
                    'phoneNum': phoneNum,
                    'resourceName': resourceName,
                    'score':'%s'% pred, 
                    'date': date,
                    'id':id 
                    })
        
        # Specialty and id row
        day_to_num = dict(zip(list(day_name), range(7)))
        
        sorted(preds, key=lambda p:p['date'])
        preds = [{
            'date':key,
            'dayOfWeek': day_to_num[datetime.strptime(key, '%d/%m/%y').strftime('%A')],
            'predictions': [item for item in group]
            } for key, group in itertools.groupby(preds, lambda item: item['date'])
        ] 
        dumpResults(preds)
        return jsonify(data=preds)

    return 'ERROR'

def dumpResults(results):
    import os
    directory = 'results'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory+'/results.csv','w') as f:
        write = lambda s: f.write(s + '\n')
        write(','.join([
            'Date','Specialty','Case ID','Patient Name',
            'Phone Number', 'Resource Name', 'Probability'
            ]))
        for result in results:
            for pred in result['predictions']:
                write(','.join([
                    pred['date'], pred['specialty'], pred['id'], pred['patientName'], 
                    pred['phoneNum'], pred['resourceName'], pred['score']
                    ]))
                
    
if __name__ == '__main__':
    app.run()
