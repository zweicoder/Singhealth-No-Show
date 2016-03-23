import ast

cols = ["Institution Description", "Appointment Year", "Appointment Quarter", "Appointment Month",
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
def extract(raw, tokens):
    categories = ["Appointment Rescheduled Reason Code", "Specialty Code", "Department Code", "Appointment Type Code",
                  "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Gender", "Race",
                  "Nationality", "Marital Status", "Patient Class Code", "Attending Doctor Rank",
                  "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
                  "Attending Doctor Department Code"]

    features = [0] * len(tokens.keys())
    # Get all qualitative features from categories we are interested in
    for cat in categories:
        col_idx = c_cols[cat]
        # column index -> raw data for column -> feature index for that category
        feature_index = tokens[raw[col_idx]]
        features[feature_index] = 1

    # Solve for some quantitative features here
    # apmt_delay = int(float(raw[c_cols["Appointment Waiting Time (days)"]]))
    # features.append(apmt_delay)
    # parse dob for age using regex - 2016
    # apmt duration from start time - end time

    # label
    label = 1 if raw[c_cols["Visit Status Code"]] == 'NS' else 0
    return label, features


def parse_data(filename, tokens):
    parsed = []
    label_list = []
    with open(filename, 'rb') as f:
        for line in f:
            raw = line.strip().split(',')  # Get data from appointment time onwards
            label, features = extract(raw, tokens)
            formatted =','.join(['%s' % (feature) for feature in features])
            label_list.append(label)
            parsed.append(formatted)
    return parsed,label_list


mapping = read_mapping()

files = ['csv/cleaned/quarter%s.csv' % i for i in range(1,5,1)]
#files = ['csv/quarter4.csv']
with open('xtrain.txt', 'w') as f:
    with open('ytrain.txt','w') as f2:
        for input_file in files:
            print 'Parsing %s...' % input_file
            data,label = parse_data(input_file, mapping)
            for d in data:
                f.write(d + '\n')
            for l in label:
                f2.write(str(l) + '\n')
    
