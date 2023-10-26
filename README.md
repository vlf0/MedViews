# MedVeiws

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


We also have a test bench for running the app locally fast and easy.
To run the application locally - go to branch "docker_dev" and check detail instruction.
