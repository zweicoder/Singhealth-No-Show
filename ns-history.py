cols = ["Institution Description",
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

# Map pid to ns history
def get_nsmap():
    mapping = {}
    with open('csv/no-show-history.csv') as f:
        next(f)
        for line in f:
            raw = line.strip().split(',')
            pid, totalNs = raw[0], raw[-1]
            if totalNs != 0:
                mapping[pid] = totalNs
    return mapping

# Map aid to pid so we can then map to NS history
def get_aid_pid_map():
    hashmap = {}
    with open('csv/fix-ns.csv', 'rb') as f:
        for line in f:
            raw = line.strip().split(',')
            aid, pid = raw[-2], raw[-1]
            hashmap[aid] = pid
    return hashmap


files = ['csv/cleaned/quarter%s.csv' % i for i in range(1,5,1)]
newfiles = ['csv/nshistory/quarter%s.csv' % i for i in range(1,5,1)]
aidPidMap = get_aid_pid_map()
nsHistory = get_nsmap()
data = []
for i in range(len(files)):
    with open(files[i],'rb') as infile:
        with open(newfiles[i],'w') as outfile:
            for line in infile:
                raw = line.strip().split(',')
                aid = raw[c_cols["eHIntS Appointment Id"]]
                pid = aidPidMap[aid] if aid in aidPidMap else 0
                pastNs  = nsHistory[pid] if pid in nsHistory else -1
                # if pastNs != -1:
                #     print pastNs
                data = line.strip() +',%s,%s\n' % (pid, pastNs)
                outfile.write(data)
