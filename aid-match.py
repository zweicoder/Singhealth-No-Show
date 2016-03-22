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

def write_column():
    files = ['csv/quarter%s.csv' % i for i in range(1,5,1)]
    hashmap = read_matching()
    with open('csv/pid.csv','w') as f:
        for input_file in files:
            with open(input_file,'rb') as f2:
                for line in f2:
                    raw = line.strip().split(',')
                    aid = raw[c_cols["eHIntS Appointment Id"]]
                    if aid in hashmap:
                        f.write(aid + ',' + hashmap[aid] + ',' + raw[c_cols["Appointment Date"]] + ',' + raw[c_cols["Visit Status Code"]] + "\n")
    
def get_wrongid():
    write_column()
    data = []
    data_new = []
    with open('csv/pid.csv','rb') as f:
        for line in f:
            raw = line.strip().split(',')
            data.append(raw)
    data = sorted(data, key=operator.itemgetter(1, 2))
    print len(data)
    patient = ""
    first = -1
    for i in range(len(data)):
        if data[i][1]!=patient:
            patient=data[i][1]
            first = i
        if data[i][3] == "NS":
            for j in range(first,i):
                if data[j][2] == data[i][2] and data[j][3] == "A":
                    data_new.append(data[j][0])
    with open('csv/pid_new.csv','w') as f:
        for d in data_new:
            f.write(d+"\n")

get_wrongid()
