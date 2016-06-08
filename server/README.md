# Oracle
This is a data source for the [Showtime]() repo as a mock database. Uses the trained prediction model to predict No Shows given a `input.csv` file with the proper format and creates an endpoint at `localhost:5000/predict`

## Usage
Put csv files under `csv/` folder, then preprocess data
```{bash}
python preprocess.py
```

Start the server
```{bash}
python server.py
```

Make sure `input.csv` exists and has these columns:
```{python}
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
```

Experience magic
```{bash}
curl localhost:5000/predict
```
