def getMap():
    mapping = {}
    cols = ["Institution Description", "Appointment Year", "Appointment Quarter", "Appointment Month", "Appointment Week Name", "Appointment Date", "Appointment Time", "eHIntS Appointment Id", "Appointment Created Date", "Rescheduled Date","Rescheduled Time", "Appointment Rescheduled Reason Code", "Session Start Time", "Session End Time", "Appointment Type Duration", "Specialty Code", "Department Code", "Appointment Type Code", "Referral Source Code", "Referral Healthcare Facility Code", "Visit Type Code", "Visit Status Code", "Date of Birth", "Gender","Race", "Nationality", "Marital Status", "Postal Code", "Patient Class Code", "Pioneer Indicator","Overbook Indicator", "No Show Count","Actual Turn Up Count","Appointment Movement Count","Appointment Waiting Time (days)","Attending Doctor Rank","Attending Doctor Department Summary (NDCS Only)","Attending Doctor Unit (NDCS Only)","Attending Doctor Department Code"]
    counts = [1] * len(cols)
    for token in ['expunknown', 'expected unknown', 'unknown','']:
        mapping[token] = 0

    for i in range(11):
        idx=1
        with open('csv/glossary-%s.csv'%i, 'rb') as f:
            for line in f:
                col = line.strip().split(',')[1].lower()
                if not col in mapping:
                    mapping[col] = idx
                    idx+=1

    with open('csv/quarter1.csv','rb') as f:
        remove = [1, 2, 3, 4, 5, 7, 29, 30, 31, 32, 33]
        for line in f:
            data = line.strip().split(',') # Get data from appointment time onwards
            # Filter unused columns
            data = filter(lambda x: x not in remove, data)

            for i in range(len(data)):
                v = data[i].lower()
                # Make mappings for categories (columns with no numbers)
                if not any(c.isdigit() for c in v) and not v in mapping:
                    mapping[v] = counts[i]
                    counts[i] += 1
                    # print v
                    # print counts

    with open('mapping.txt','w') as f:
        f.write(str(mapping))

getMap()