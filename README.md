This project - Django multiuser app which allow to users getting data from database
of **KIS.EMIAS** very fast and easy in real time.

**KIS.EMIAS** - it is government information system and all hospitals of Moscow connected to it. 
It has own database cluster, one instance belong to one hospital. The network of databases always protected, 
we have no opportunity connect to this network from out (can from hospital network only).
In this reason the app need to deploy in the hospital own server, that allow the app to work correct. 

Project wrote on Django framework, deployed on Ubuntu 22.04 OS using Gunicorn and Nginx.
The service controlling on OS by Supervisor utility.

I was motivated to create this app because i with my teammate really don't like how 
built-in tools from KIS.EMIAS works: slowly and often exiting unsuccessful.
This app solving the human resource consumption and too long waiting response; 
also users can get needed data immediately  themselves now (earlier they used to depend on one database administrator).
In the process of creating I learn many useful things, such as Git and GitHub, Docker and Docker-compose, little JS, 
linux OS, world of networks, also improved Python knowing lvl.

I also have test version on the docker's containers. 
All you need - to have the Docker and Docker-Compose
If you want to try it - go to **"docker_dev"** branch and check README file.