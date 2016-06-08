from datetime import datetime
import numpy as np
import calendar
import os
directory = 'preprocess'
if not os.path.exists(directory):
    os.makedirs(directory)

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

def getScales(files):
    quantitiesToScale = ['Appointment Waiting Time (days)', 'Age']
    scale = {key: [] for key in quantitiesToScale}
    for input_file in files:
        with open(input_file, 'rb') as f:
            for line in f:
                raw = line.strip().split(',')
                scale["Appointment Waiting Time (days)"].append(
                    int(float(raw[c_cols["Appointment Waiting Time (days)"]])))
                age = datetime.now().year - \
                    datetime.strptime(
                        raw[c_cols["Date of Birth"]], '%d/%m/%y %H:%M').year
                age = age + 100 if age < 0 else age
                scale['Age'].append(age)

    all_means = {key: np.mean(scale[key]) for key in quantitiesToScale}
    all_std = {key: np.std(scale[key]) for key in quantitiesToScale}
    with open(directory+'/means.txt','w') as f:
        f.write(str(all_means))
    with open(directory+'/stds.txt','w') as f:
        f.write(str(all_std))

def getBinaryMap(files):
    mapping = {}
    cols = ["Institution Description", "Appointment Week Name", "Appointment Date", "Appointment Time", "eHIntS Appointment Id", "Appointment Created Date", "Rescheduled Date","Rescheduled Time", "Appointment Rescheduled Reason Code", "Session Start Time", "Session End Time", "Appointment Type Duration", "Specialty Code", "Department Code", "Appointment Type Code", "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Visit Status Code", "Date of Birth", "Gender","Race", "Nationality", "Marital Status", "Postal Code", "Patient Class Code", "Pioneer Indicator","Overbook Indicator", "No Show Count","Actual Turn Up Count","Appointment Movement Count","Appointment Waiting Time (days)","Attending Doctor Rank","Attending Doctor Department Summary (NDCS Only)","Attending Doctor Unit (NDCS Only)","Attending Doctor Department Code"]

    c_cols = {}
    for i, v in enumerate(cols):
        c_cols[v] = i

    for token in ['expunknown', 'expected unknown', 'unknown','']:
        mapping[token] = 0

    # Map integer code to classes/categories specified in glossary
    # For each data file, find the columns we're gonna classify and make mappings for unseen values
    categories = ["Appointment Rescheduled Reason Code", "Specialty Code", "Department Code", "Appointment Type Code",
                   "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Gender", "Race",
                   "Nationality", "Marital Status", "Patient Class Code", "Attending Doctor Rank",
                   "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
                   "Attending Doctor Department Code"]
    idx=1
   #  categories = ['Visit Type Code', 'Referral Source Code','Attending Doctor Rank',
   # 'Appointment Type Code','Patient Class Code', 'Attending Doctor Department Summary (NDCS Only)',
   # 'Gender','Specialty Code']
    for filename in files:
        print('Parsing mapping from %s'%filename)
        with open(filename,'rb') as f:
            for line in f:
                data = line.strip().split(',')
                # Filter unused columns
                data = [data[c_cols[cat]] for cat in categories]

                for i in range(len(data)):
                    val = data[i].lower()

                    # Make mappings for categories (qualitative columns)
                    if not val in mapping:
                        mapping[val] = idx
                        idx += 1

    with open(directory+'/mapping.txt','w') as f:
        f.write(str(mapping))

files = ['csv/quarter%s.csv' % i for i in range(1, 5, 1)]
getBinaryMap(files)
getScales(files)