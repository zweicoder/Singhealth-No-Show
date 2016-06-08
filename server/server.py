from flask import Flask, jsonify, request
app = Flask(__name__)

from flask import request, Response
import xgboost as xgb
import numpy as np
import json
from oracle import Oracle

filename = 'input.csv'
predictor = Oracle(filename)

@app.route('/predict', methods=['GET'])
def getPredictions():
    with open(filename) as f:
        preds = predictor.predict()
        lines = f.read().split('\n')[:-1]
        lines = [line.split(',') for line in lines]
        # Specialty and id row
        specialty, id, date = zip(*((line[12], line[4], line[2]) for line in lines))
        preds = [{
        'specialty':specialty[i], 
        'score':'%s'%preds[i], 
        'date': date[i],
        'prediction':0 if preds[i]<0.65 else 1,
        'id':id[i] } for i in xrange(len(preds))]

        return jsonify(result=preds)

    return 'ERROR'
    
if __name__ == '__main__':
    app.run()
