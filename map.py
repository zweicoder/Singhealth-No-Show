def getMap(files):
    mapping = {}
    cols = ["Institution Description", "Appointment Year", "Appointment Quarter", "Appointment Month", "Appointment Week Name", "Appointment Date", "Appointment Time", "eHIntS Appointment Id", "Appointment Created Date", "Rescheduled Date","Rescheduled Time", "Appointment Rescheduled Reason Code", "Session Start Time", "Session End Time", "Appointment Type Duration", "Specialty Code", "Department Code", "Appointment Type Code", "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Visit Status Code", "Date of Birth", "Gender","Race", "Nationality", "Marital Status", "Postal Code", "Patient Class Code", "Pioneer Indicator","Overbook Indicator", "No Show Count","Actual Turn Up Count","Appointment Movement Count","Appointment Waiting Time (days)","Attending Doctor Rank","Attending Doctor Department Summary (NDCS Only)","Attending Doctor Unit (NDCS Only)","Attending Doctor Department Code"]
    for token in ['expunknown', 'expected unknown', 'unknown','']:
        mapping[token] = 0

    # Map integer code to classes/categories specified in glossary
    for i in range(11):
        idx=1
        filename = 'csv/glossary-%s.csv'%i
        print('Parsing mapping from %s'%filename)
        with open(filename, 'rb') as f:
            for line in f:
                col = line.strip().split(',')[1].lower()
                if not col in mapping:
                    mapping[col] = idx
                    idx+=1
    # For each data file, find the columns we're gonna classify and make mappings for unseen values
    remove = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 22, 27, 34, 29, 30, 31, 32, 33])
    counts = [1] * len(cols)
    for filename in files:
        print('Parsing mapping from %s'%filename)
        with open(filename,'rb') as f:
            for line in f:
                data = line.strip().split(',') # Get data from appointment time onwards
                # Filter unused columns
                data = [data[i] if i not in remove else None for i in range(len(data))]

                for i in range(len(data)):
                    if data[i] == None:
                        continue

                    v = data[i].lower()
                    
                    # if any(c.isdigit() for c in v):
                    #     print 'Bad column %s with %s' % (i, v)
                    #     remove.add(i)
                    #     continue

                    # Make mappings for categories (qualitative columns)
                    if not v in mapping:
                        mapping[v] = counts[i]
                        counts[i] += 1

    with open('mapping.txt','w') as f:
        f.write(str(mapping))

files = ['csv/quarter%s.csv' % i for i in range(1,5,1)]
getMap(files)