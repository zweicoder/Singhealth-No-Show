# Oracle
This is a data source for the [Showtime](https://github.com/zweicoder/Showtime-Dashboard) dashboard as a mock database. Uses the trained prediction model to predict No Shows given a `input.csv` file with the proper format and creates an endpoint at `localhost:5000/predict`

## Usage (*layman*)
#### **NOTE: Any folders/ files not listed here should not be touched**
1. Replace `input.csv` with your exported view file. This file should contain the data you want to predict. A one week (*or less*) range is recommended. Make sure the columns are present and in the correct order as shown here:
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
        "Attending Doctor Department Code", "PID", "Past NS", "Patient Name", "Phone Number", "Resource Name"]
```
### **DO NOT LEAVE THE COLUMN HEADERS INSIDE THE FILE, EVERY ROW MUST BE A ROW OF DATA!**
2. ~~Run `server.exe`~~ (Currently unavailable due to difficulties packaging Python app. Get someone to host it on a running server or install it on your computers.)
3. Run `dashboard.exe`
4. Results are on the dashboard. Additionally a `results/results.csv` file is generated, containing predictions on all the data passed in for the last query.

## Usage (*devs*)
Put csv files under `csv/` folder, then preprocess data
```{bash}
python preprocess.py
```
This outputs the constants required to scale the features inside the `preprocess/` folder

Start the server
```{bash}
python server.py
```

Make sure `input.csv` exists and has the columns listed above.

Experience *magic*
```{bash}
curl localhost:5000/predict
```

## How it Works
- The structure of the app is made up of the web dashboard and this prediction model. The backend server returns the prediction results via the HTTP endpoint once queried by the web dashboard.

-  Ideally the server would be linked to the database, but since this was intended to be a demo and proof of concept, it receives input via an `input.csv` file manually put in. Results are outputted and overwrites the `results/results.csv` file.

- The server listens to `localhost:5000`, whereas the dashboard uses `localhost:3000` and queries the server through the above address. As such the application is currently tuned to listen to `localhost`. Deploying the server code on a production server will *at least* require file upload and download features, but ideally be linked to the database. However the implementation would be infeasible given the time constraints and restrictions with integration, hence it is out of scope for this project.
