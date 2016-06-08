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
        preds =  predictor.predict()
        lines = f.read().split('\n')[:-1]
        lines = [line.split(',') for line in lines]
        # Specialty and id row
        specialty, id, date = zip(*((line[12], line[4], line[2]) for line in lines))
        day_to_num = dict(zip(list(day_name), range(7)))
        preds = [{
            'specialty':specialty[i], 
            'score':'%s'%preds[i], 
            'date': date[i],
            'id':id[i] 
        # Filter all that is less than the threshold
        } for i in xrange(len(preds)) if preds[i] > threshold]
        
        sorted(preds, key=lambda p:p['date'])
        preds = [{
        'date':key,
        'dayOfWeek': day_to_num[datetime.strptime(key, '%d/%m/%y').strftime('%A')],
        'predictions': [
            {
            'score': item['score'], 
            'id':item['id'],
            'specialty': item['specialty']
            } for item in group
            ]}
        for key, group in itertools.groupby(preds, lambda item: item['date'])
        ] 

        return jsonify(data=preds)

    return 'ERROR'
    
if __name__ == '__main__':
    app.run()
