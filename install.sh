#!/bin/bash

###############################
###### Meet Requirements ######
###############################


#Check wheter Docker-compose is installed or not

which docker-compose

if [ $? -eq 0 ]
then
    docker-compose --version | grep "docker-compose version"
    if [ $? -eq 0 ]
    then
        echo "docker-compose existing"
    else
        echo "Installing docker-compose"
        apt install docker-compose -y
    fi
else
    echo "Installing docker-compose"
    apt install docker-compose -y
fi

###############################
###### Prepare System #########
###############################

#Set appropriate permissions so you can execute docker and docker-compose without sudo

if [ $(getent group docker) ]; 
then
    echo "Group docker exists, adding you to the group"
    usermod -aG docker $USER
    newgrp docker
else
    echo "Droup docker does not exist,creating group"
    groupadd docker
    usermod -aG docker $USER
    newgrp docker
fi


# #Create nginx config 
# cat << EOF > /etc/nginx/conf.d/observer.conf
#     server {
#         listen 443 ssl;
#         server_name observer.example.com;
#         ssl_certificate       /etc/pki/tls/certs/cert_name.cer;
#         ssl_certificate_key   /etc/pki/tls/private/observer.example.com.key;
#         access_log /var/log/nginx/observer.access.log;
#         error_log /var/log/nginx/observer.error.log warn;
    
#         location / {
#             proxy_pass http://server_ip:8081;
#             proxy_set_header   Host $http_host;
#             proxy_set_header   X-Real-IP $remote_addr;
#             proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
#             proxy_set_header   X-Forwarded-Proto $scheme;
        
#             client_max_body_size       10m;
#             client_body_buffer_size    128k;
        
#             proxy_connect_timeout      90;
#             proxy_send_timeout         90;
#             proxy_read_timeout         90;
        
#             proxy_buffer_size          4k;
#             proxy_buffers              4 32k;
#             proxy_busy_buffers_size    64k;
#             proxy_temp_file_write_size 64k;
#         }
#     }
# EOF

# #Reload nginx conf
# nginx -s reload

##################################################
###### Create and config sustemd service #########
##################################################

SERVICE=$(ls /etc/systemd/system |  grep "observer")

if [ -z "$SERVICE" ]
then
    #Create systemd service
    cat << EOF > /etc/systemd/system/observer.service
        [Unit]
        Description=Django based observer service
    
        [Service]
        WorkingDirectory=/opt/MedViews/MedVeiws
        ExecStart=/usr/bin/docker-compose up -d
        ExecStop=/usr/bin/docker-compose down --remove-orphans
        RemainAfterExit=yes
        TimeoutSec=300
        Restart=on-failure
        
        [Install]
        WantedBy=multi-user.target
EOF

    #Prepare service
    chown root:root /etc/systemd/system/observer.service
    chmod 644 /etc/systemd/system/observer.service
    systemctl daemon-reload
    systemctl enable observer.service
else 
    chown root:root /etc/systemd/system/observer.service
    chmod 644 /etc/systemd/system/observer.service
    echo "Service is already installed" 
fi

echo "You can start the app now"
