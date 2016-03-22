
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
    with open('pid.csv','w') as f:
        for input_file in files:
            with open(input_file,'rb') as f2:
                for line in f2:
                    raw = line.strip().split(',')
                    aid = raw[c_cols["eHIntS Appointment Id"]]
                    if aid in hashmap:
                        f.write(aid + ',' + hashmap[aid] + ',' + raw[c_cols["Appointment Date"]] + ',' + raw[c_cols["Visit Status Code"]] + "\n")



write_column()

