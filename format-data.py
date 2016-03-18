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

    features = []
    # Get all qualitative features
    for cat in categories:
        col_idx = c_cols[cat]
        features.append(classify(raw[col_idx], tokens))

    # Solve for some quantitative features here
    apmt_delay = int(float(raw[c_cols["Appointment Waiting Time (days)"]]))
    features.append(apmt_delay)
    # parse dob for age using regex - 2016
    # apmt duration from start time - end time

    # label
    label = classify(raw[c_cols["Visit Status Code"]], tokens)
    return label, features, categories + ["Appointment Waiting Time (days)"]


def parse_data(filename, tokens):
    parsed = []
    with open(filename, 'rb') as f:
        for line in f:
            raw = line.strip().split(',')  # Get data from appointment time onwards
            label, features, categories = extract(raw, tokens)
            formatted = str(label) + ' ' + ' '.join(['%s:%s' % (idx, feature) for idx, feature in enumerate(features)])
            parsed.append(formatted)
    return parsed


mapping = read_mapping()

files = ['csv/quarter%s.csv' % i for i in range(1,4,1)]
# files = ['csv/quarter3.csv']
with open('out', 'w') as f:
    for input_file in files:
        print 'Parsing %s...' % input_file
        data = parse_data(input_file, mapping)
        for d in data:
            f.write(d + '\n')
