
"""
for each wanted column:
    if value not in seen:
        mapping[unseen_value] =  i++
        set.add(unseen_value)

return mapping, len(set)

in format-data.py,
initialize [0]*len(set)
for each value get from the mapping its index and set to 1
"""
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
    # categories = ["Appointment Rescheduled Reason Code", "Specialty Code", "Department Code", "Appointment Type Code",
    #                "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Gender", "Race",
    #                "Nationality", "Marital Status", "Patient Class Code", "Attending Doctor Rank",
    #                "Attending Doctor Department Summary (NDCS Only)", "Attending Doctor Unit (NDCS Only)",
    #                "Attending Doctor Department Code"]
    idx=1
    categories = ['Visit Type Code', 'Referral Source Code','Attending Doctor Rank',
    'Appointment Type Code','Patient Class Code', 'Attending Doctor Department Summary (NDCS Only)',
    'Gender','Specialty Code']
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

    with open('mapping.txt','w') as f:
        f.write(str(mapping))

files = ['csv/cleaned/quarter%s.csv' % i for i in range(1,5,1)]
getBinaryMap(files)