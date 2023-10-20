FROM python:3.11-slim

# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1

# Creating working directory
WORKDIR /usr/src/MedViews

# Copy content
COPY . .

# Updating system indexes
RUN apt-get update -y && apt-get upgrade

# Installing nginx
RUN apt-get install nginx -y

# Installing dependencies
RUN pip3 install -r ./requirements.txt

EXPOSE 8000

# Running the app
ENTRYPOINT ["gunicorn", "observer.wsgi", "-b", "0.0.0.0:8000"]
