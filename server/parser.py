import ast
from datetime import datetime
import numpy as np
import calendar
day_to_num = dict(zip(list(calendar.day_name), range(7)))

cols = ["Institution Description",
        "Appointment Week Name", "Appointment Date", "Appointment Time", "eHIntS Appointment Id",
        "Appointment Created Date", "Rescheduled Date", "Rescheduled Time", "Appointment Rescheduled Reason Code",
        "Session Start Time", "Session End Time", "Appointment Type Duration", "Specialty Code", "Department Code",
        "Appointment Type Code", "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code",
        "Visit Status Code", "Date of Birth", "Gender", "Race", "Nationality", "Marital Status", "Postal Code",
        "Patient Class Code", "Pioneer Indicator", "Overbook Indicator", "No Show Count", "Actual Turn Up Count",
        "Appointment Movement Count", "Appointment Waiting Time (days)", "Attending Doctor Rank",
        "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
        "Attending Doctor Department Code", "PID", "Past NS"]

c_cols = {}
for i, v in enumerate(cols):
    c_cols[v] = i

def read_dict_from_file(filename):
    # Mapping for real number classification
    with open(filename, 'r') as f:
        s = f.read()
        return ast.literal_eval(s)

all_means, all_std = read_dict_from_file('preprocess/means.txt'), read_dict_from_file('preprocess/stds.txt')
tokens = read_dict_from_file('preprocess/mapping.txt')

class Parser:
    def __init__(self, input_file):
        self.input_file = input_file
    # Return list of extracted values
    def extract(self, raw, tokens, length):
        categories = ["Appointment Rescheduled Reason Code", "Specialty Code", "Department Code", "Appointment Type Code",
                      "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Gender", "Race",
                      "Nationality", "Marital Status", "Patient Class Code", "Attending Doctor Rank",
                      "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
                      "Attending Doctor Department Code"]

        features = [0] * length
        # Get all qualitative features from categories we are interested in
        for cat in categories:
            col_idx = c_cols[cat]
            # column index -> raw data for column -> feature index for that
            # category
            col_val = raw[col_idx].lower()
            feature_index = tokens[col_val]
            features[feature_index] = 1

        # Solve for some quantitative features here
        # day of the week
        day = day_to_num[datetime.strptime(
            raw[c_cols["Appointment Date"]], '%d/%m/%y').strftime('%A')]
        day_bin = [0 for i in range(7)]
        day_bin[day] = 1
        for d in day_bin:
            features.append(d)

        # Appointment Time of day
        time = datetime.strptime(raw[c_cols["Appointment Time"]], '%H:%M')
        time_cat = (time.hour - 7) * 2 + (time.minute / 30)
        features.append(time_cat)

        # Appointment delay
        apmt_delay = int(float(raw[c_cols["Appointment Waiting Time (days)"]]))
        apmt_delay = (1.0 * apmt_delay - all_means[
                      'Appointment Waiting Time (days)']) / all_std['Appointment Waiting Time (days)']
        features.append(apmt_delay)

        # Age
        age = datetime.now().year - \
            datetime.strptime(raw[c_cols["Date of Birth"]], '%d/%m/%y %H:%M').year
        age = age + 100 if age < 0 else age
        age = (1.0 * age - all_means['Age']) / all_std['Age']
        features.append(age)

        # Past NS
        pastNs = int(raw[c_cols["Past NS"]])
        # Remember the negatives if planning to scale this feature
        features.append(pastNs)

        # Postal code -> distance

        # label
        return features

    def parse(self):
        # TODO get all means and s.d.s     
        
        parsed = []
        length = len(tokens.keys())
        with open(self.input_file, 'rb') as f:
            for line in f:
                raw = line.strip().split(',')
                # Get data from appointment time onwards
                features = self.extract(raw, tokens, length)
                # formatted = ','.join(('%s' % (feature) for feature in features))
                parsed.append(features)

        return parsed
