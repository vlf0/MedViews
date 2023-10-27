# MedVeiws

_ATTENTION:
It is the test bench.
The files .env and db.sqlite3 are here because it allows because this allows you
to make the process of launching a test bench locally as easy as possible 
and no contains important / secret information or any CREDs._\
**db.sqlite3** contains already created superuser only; SECRET_KEY in the **.env** file was created for testing goals special.
**<center><p>NOTES: superuser for SQLite DB:</p></center>**
__<center>login: admin</center>__
__<center>password: root</center>__

This project - Django multiuser app which allow to users getting data from database
of **KIS.EMIAS** very fast and easy in real time.

**KIS.EMIAS** - it is government information system and all hospitals of Moscow connected to it. 
It has own database cluster, one instance belong to one hospital. The network of databases always protected, 
we have no opportunity connect to this network from out (can from hospital network only).
In this reason the app need to deploy in the hospital own server, that allow the app to work correct.

**<center><p>App logic</p></center>**
The app has SQLite database as a main DB needed only for saving connecting to Postgres database data.
So, how it works:
the app using depend on hospital Postgres database, that the first thing you need to do - create the SQlite DB superuser.
Then by using superuser acc - add connection data to Postgres. 
After need restart the app and it works now.
The app collects the data gotten from pages across POST requests and insert them into prepared SQL query in app code.
Then sends the SQL queries to Postgres DB and gets responses as data array.
Handling received arrays of data by using Pandas library and creating reports of 2 types: **.xlsx** files and **HTML** code,
that output on the reporting page. 
Users also can download excel files to their machine if it needs.\


Project wrote on Django framework, deployed on Ubuntu 22.04 OS using Gunicorn and Nginx.
The service controlling on OS by Supervisor utility.
Collaborators - [Anton Ryadovoy](https://github.com/AntonRyadovoy) 

I was motivated to create this app because i with my teammate really don't like how 
built-in tools from KIS.EMIAS works: slowly, ineffective and often exiting unsuccessful.
This app solving the human resource consumption and too long waiting response; 
also users can get needed data immediately  themselves now (earlier they used to depend on one database administrator).
In the process of creating I learn many useful things, such as Git and GitHub, Docker and Docker-compose, little JS,
HTML, CSS, API, linux OS, world of networks, project design also improved Python knowing lvl.


To run the application locally you need install Docker and Docker-Compose and follow these steps:

NOTES: if you are using Windows OS, you need insert this command in terminal before all other steps:\
`git config --global core.autocrlf input`\
This configures Git to handle line endings correctly for your operating system
by setting the core.autocrlf configuration option.\
Since we are using docker containers based on the *nix OS we need do it
for shell can read the commands correct  on starting app. 
After you testing the app you need switch back docker settings using this command:\
`git config --global core.autocrlf true`\
This is return settings to default for your OS.\
_If you are a developer/programmer you can just switch CRLF to LF in your IDE and then go to steps below._ 

1. Open your any favourite console and go to folder where you want to place the app;

2. Copy and past this command to download repo:

    `git clone https://github.com/vlf0/MedVeiws.git`

3. Go to _MedVeiws_ folder and type this command to change working branch:

   `git checkout docker_dev`

4. Insert next command to run the app:

   `docker-compose up`

5. After this steps the app will be run in docker container, just go to your localhost on 8080 port:

   [localhost](http://localhost:8080) 
