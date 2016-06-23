import xgboost as xgb
import numpy as np
import json
from oracle import Oracle
from datetime import datetime
from calendar import day_name
import itertools
import os
from hashlib import sha256

from flask import Flask, jsonify, request, Response, url_for, send_from_directory, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
preprocessed = all(os.path.isfile(path) for path in ['preprocess/mapping.txt','preprocess/means.txt','preprocess/stds.txt'])
if not preprocessed:
    print 'Data not preprocessed, preprocessing data for feature scaling...'
    import preprocess

predictor = Oracle()
threshold = 0.75 #  or 0.75

def getPredictions(filename):
    infile = UPLOAD_FOLDER+'/'+filename
    with open(infile) as f:
        lines = f.read().split('\n')
        preds = []
        for pred, line in itertools.izip(predictor.predict(infile), lines):
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
        outfile = dumpResults(preds, filename)
        return preds, outfile
        # return jsonify(data=preds, url=url_for('results', filename=outfile))

    return 'ERROR'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'nofile'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'nofilename'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = sha256(str(datetime.now())).hexdigest() + '-'+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Parse and predict uploaded file
            preds, outfile= getPredictions(filename)
            return jsonify(data=preds, url=url_for('results', filename=filename))
            # return redirect(url_for('results', filename=outfile))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/results/<filename>')
def results(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'],
                               filename)

def dumpResults(results, filename):
    outfile = '/%s.csv'%filename.rsplit('.',1)[0]
    with open(RESULTS_FOLDER + outfile,'w') as f:
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
    return outfile
    
if __name__ == '__main__':
    app.run()
