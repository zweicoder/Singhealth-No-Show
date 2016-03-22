import operator

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

def read_matching():
    hashmap = {}
    with open('csv/fix-ns.csv', 'rb') as f:
        for line in f:
            raw = line.strip().split(',')
            hashmap[raw[0]] = raw[1]
    return hashmap
   
def update_file():
    files = ['csv/quarter%s.csv' % i for i in range(1,5,1)]
    newfiles = ['csv/quarter%s_new.csv' % i for i in range(1,5,1)]
    hashmap = read_matching()
    data = []
    for input_file in files:
        with open(input_file,'rb') as f:
            for line in f:
                raw = line.strip().split(',')
                aid = raw[c_cols["eHIntS Appointment Id"]]
                if aid in hashmap:
                    data.append([aid, hashmap[aid] , raw[c_cols["Appointment Date"]] , raw[c_cols["Visit Status Code"]]])    
    data = sorted(data, key=operator.itemgetter(1, 2))
    patient = ""
    first = -1
    wrong_aid = set()
    for i in range(len(data)):
        if data[i][1]!=patient:
            patient=data[i][1]
            first = i
        if data[i][3] == "NS":
            for j in range(first,i):
                if data[j][2] == data[i][2] and data[j][3] == "A":
                    wrong_aid.add(data[i][0])
    
    for i in range(len(files)):
        with open(files[i],'rb') as f1:
            with open(newfiles[i],'w') as f2:
                for line in f1:
                    raw = line.strip()
                    row = raw.split(',')
                    aid = row[c_cols["eHIntS Appointment Id"]]
                    if aid not in wrong_aid:
                        f2.write(raw+"\n")
                    else:
                        row[c_cols["Visit Status Code"]] = "A"
                        f2.write(','.join(row)+"\n")
                    

update_file()