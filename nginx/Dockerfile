FROM nginx:1.25-alpine

# Creating working directory
WORKDIR /app_static/

# Copy content
COPY . /app_static/static

COPY ./config/. /etc/nginx/conf.d/

EXPOSE 8080
