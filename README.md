<center>

# MedViews

</center>

This project - Django application which solves the problem of aggregating daily used data and removes this task from medical personnel, and also allows managers to receive current analytics at any time.
___
**Stack:**
- Django
- PostgresSQL
- Nginx

Hosted on Ubuntu 22.04
___
**KIS.EMIAS** - it is government information system and all hospitals of Moscow connected to it. 
It has own database cluster, one instance belong to one hospital. The network of databases always protected, 
we have no opportunity connect to this network from out (can from hospital network only).
In this reason the app need to deploy in the hospital own server, that allow the app to work correct.
___
**Main section:**

![Image alt](https://github.com/vlf0/Dashboard_media/blob/main/medviews/Screenshot_1.png)
___
**Department and dates choosing section:**

![Image alt](https://github.com/vlf0/Dashboard_media/blob/main/medviews/Screenshot_2.png)
___
**Result by specified parameters section:**

![Image alt](https://github.com/vlf0/Dashboard_media/blob/main/medviews/Screenshot_4.png)
___
**Global result by all depts section:**

![Image alt](https://github.com/vlf0/Dashboard_media/blob/main/medviews/Screenshot_5.png)
___

[See video on youtube (1:08)](https://youtu.be/8levWjwBjbw/)
___

<center><p>Motivating</p></center>

I was motivated to create this app because i with my teammate really don't like how 
built-in tools from KIS.EMIAS works: slowly, ineffective and often exiting unsuccessful.
This app solving the human resource consumption and too long waiting response; 
also users can get needed data immediately  themselves now (earlier they used to depend on one database administrator).
In the process of creating I learn many useful things, such as Git and GitHub, Docker and Docker-compose, little JS,
HTML, CSS, API, linux OS, world of networks, project design also improved Python knowing lvl.
___
We also have a test bench for running the app locally fast and easy.
To run the application locally - go to branch "docker_dev" and check detail instruction.

___
Collaborators - [Anton Ryadovoy](https://github.com/AntonRyadovoy) 