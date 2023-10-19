FROM python:3.11-slim

# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1

# Creating working directory
WORKDIR /usr/src/MedViews

# Copy content
COPY . .

# Installing dependencies
RUN pip3 install -r ./requirements.txt

# Updating system indexes
RUN apt-get update

EXPOSE 8000

# Running the app
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
