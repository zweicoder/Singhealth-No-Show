import ast
from datetime import datetime
import numpy as np

cols = ["Institution Description",
        "Appointment Week Name", "Appointment Date", "Appointment Time", "eHIntS Appointment Id",
        "Appointment Created Date", "Rescheduled Date", "Rescheduled Time", "Appointment Rescheduled Reason Code",
        "Session Start Time", "Session End Time", "Appointment Type Duration", "Specialty Code", "Department Code",
        "Appointment Type Code", "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code",
        "Visit Status Code", "Date of Birth", "Gender", "Race", "Nationality", "Marital Status", "Postal Code",
        "Patient Class Code", "Pioneer Indicator", "Overbook Indicator", "No Show Count", "Actual Turn Up Count",
        "Appointment Movement Count", "Appointment Waiting Time (days)", "Attending Doctor Rank",
        "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
        "Attending Doctor Department Code"]

c_cols = {}
for i, v in enumerate(cols):
    c_cols[v] = i


# Mapping for real number classification
def read_mapping():
    with open('mapping.txt', 'r') as f:
        s = f.read()
        return ast.literal_eval(s)


def classify(code, tokens):
    return tokens[code.lower()]


# Return list of extracted values
def extract(raw, tokens, length):
    categories = ["Appointment Rescheduled Reason Code", "Specialty Code", "Department Code", "Appointment Type Code",
                   "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Gender", "Race",
                   "Nationality", "Marital Status", "Patient Class Code", "Attending Doctor Rank",
                   "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
                   "Attending Doctor Department Code"]
#    categories = ['Referral Source Code','Attending Doctor Rank','Appointment Type Code','Patient Class Code']

    features = [0] * length
    # Get all qualitative features from categories we are interested in
    for cat in categories:
        col_idx = c_cols[cat]
        # column index -> raw data for column -> feature index for that category
        col_val = raw[col_idx].lower()
        feature_index = tokens[col_val]
        features[feature_index] = 1

    # Solve for some quantitative features here
    apmt_delay = int(float(raw[c_cols["Appointment Waiting Time (days)"]]))
    features.append(apmt_delay)
    # parse dob for age using regex - 2016
    age = datetime.now().year - datetime.strptime(raw[c_cols["Date of Birth"]],'%d/%m/%y %H:%M').year
    age = age + 100 if age < 0 else age        
    features.append(age)
    # apmt duration from start time - end time
    
    duration = int(raw[c_cols["Appointment Type Duration"]])
    features.append(duration)
    # label
    label = 1 if raw[c_cols["Visit Status Code"]] == 'NS' else 0
    return label, features


def parse_data(filename, tokens, means, stds):
    parsed = []
    label_list = []
    length = len(tokens.keys())

    with open(filename, 'rb') as f:
        for line in f:
            raw = line.strip().split(',')
            # Get data from appointment time onwards
            label, features = extract(raw, tokens, length)
            features[-3] = (1.0* features[-3] - means[0]) / stds[0]
            features[-2] = (1.0* features[-2] - means[1]) / stds[1]
            features[-1] = (1.0* features[-1] - means[2]) / stds[2]
            formatted =','.join(['%s' % (feature) for feature in features])
            label_list.append(label)
            parsed.append(formatted)

    return parsed,label_list


mapping = read_mapping()
files = ['csv/cleaned/quarter%s.csv' % i for i in range(1,4,1)]
#files = ['csv/quarter4.csv']

everything= [[],[],[]]
for input_file in files:
    with open(input_file, 'rb') as f:
        for line in f:
            raw = line.strip().split(',')
            everything[0].append(int(float(raw[c_cols["Appointment Waiting Time (days)"]])))
            age = datetime.now().year - datetime.strptime(raw[c_cols["Date of Birth"]],'%d/%m/%y %H:%M').year
            age = age + 100 if age < 0 else age       
            everything[1].append(age)
            everything[2].append(int(raw[c_cols["Appointment Type Duration"]]))
all_means = map(lambda x: np.mean(x), everything)
all_std = map(lambda x: np.std(x), everything)

with open('xtrain.txt', 'w') as f:
    with open('ytrain.txt','w') as f2:
        for input_file in files:
            print 'Parsing %s...' % input_file
            data,label = parse_data(input_file, mapping, all_means, all_std)
            for d in data:
                f.write(d + '\n')
            for l in label:
                f2.write(str(l) + '\n')
    
