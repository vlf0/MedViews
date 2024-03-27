# MedVeiws
Team work for hospital monitoring app.

This multiuser app will connect to one of the Moscow hospitals DB and displaying data for further analys. 
Projected for their own using and deploying on their own local server.

To deploy the application locally follow these steps:


1. Open **Git Bash** (or **PowerShell**) console and 
go to folder where you want to place the app;
2. Copy and past this code snippet to download repo:

    __git clone https://github.com/vlf0/MedVeiws.git__
3. Create ENV in root the same folder (in this example i use _virtualenv_ module):

    __virtualenv venv__
4. Go to scripts folder (root_folder/venv/scripts/) and activate virtual environment by
typing activating command. For example - for windows powershell it will be 

    __.\activate.ps1__

5. Go to _MedViews_ folder and type for change working branch:

   __git checkout localdev_vlf__

6. Go to project folder named _observer_ and type:

   __pip install -r requirements.txt__

7. After this step you can testing app:

   __python manage.py runserver__
