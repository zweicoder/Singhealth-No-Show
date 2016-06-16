# Oracle
This is a data source for the [Showtime](https://github.com/zweicoder/Showtime-Dashboard) dashboard as a mock database. Uses the trained prediction model to predict No Shows given a `input.csv` file with the proper format and creates an endpoint at `localhost:5000/predict`

## Usage (*layman / ops staff*)
#### **NOTE: Any folders/ files not highlighted here should not be touched**
![Only two files that matter](https://i.gyazo.com/b1f7a5aee66bb89d99c3d84d7264e681.png)
1. Replace `input.csv` with your exported view file. This file should contain the data you want to predict. A one week (*or less*) range is recommended. Make sure the columns are present and in the correct order as shown here:

> Institution Description, Appointment Week Name, Appointment Date, Appointment Time, eHIntS Appointment Id, Appointment Created Date, Rescheduled Date, Rescheduled Time, Appointment Rescheduled Reason Code, Session Start Time, Session End Time, Appointment Type Duration, Specialty Code, Department Code, Appointment Type Code, Referral Source Code, Referral Healthcare Facility Code, Visit Type Code, Visit Status Code, Date of Birth, Gender, Race, Nationality, Marital Status, Postal Code, Patient Class Code, Pioneer Indicator, Overbook Indicator, No Show Count, Actual Turn Up Count, Appointment Movement Count, Appointment Waiting Time (days), Attending Doctor Rank, Attending Doctor Department Summary (NDCS Only), Attending Doctor Unit (NDCS Only), Attending Doctor Department Code, PID, Past NS, Patient Name, Phone Number, Resource Name

### **DO NOT LEAVE THE COLUMN HEADERS INSIDE THE FILE, EVERY ROW MUST BE A ROW OF DATA!**

For those who for some reason think it is more intuitive, the contents will looks something like this:
```
National Dental Centre,04 Jan - 10 Jan,5/1/15,7:30,C~3382514,31/12/14,,,EXPUNKNOWN,7:30:00,16:30:00,15,DPDN,DRDPEDO,PEDOSURG,60,CDSHG,FP,A,6/6/12 0:00,MALE,Chinese,Singapore Citizen,,806327,SUB,N,N,,1,1,5,Registrar,RESTORATIVE DENTISTRY,RD - PEDODONTICS,DRDPEDO,110205,0
National Dental Centre,04 Jan - 10 Jan,5/1/15,8:00,C~3022385,13/1/14,,,EXPUNKNOWN,8:00:00,12:30:00,15,DOTD,DORTHO,ORTHOTXT,702,NDCSUB,FP,A,11/3/95 0:00,MALE,Chinese,Singapore Citizen,,520729,SUB,N,N,,1,0,357,Dental Officer (Resident),RESIDENT,RESIDENT - ORTHODONTICS,DORTHO,100158,1
...
```

2. ~~Run `server.exe`~~ (Currently unavailable due to difficulties packaging Python app. Get someone to host it on a running server or install it on your computers.)
3. Run `dashboard.exe`
4. Results are on the dashboard. Additionally a `results.csv` file is generated in the `results/` folder, containing predictions on all the data passed in for the last query.


## Usage (*devs / technical people*)
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
