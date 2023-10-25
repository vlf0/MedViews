FROM python:3.11-slim

# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1

# Creating working directory
WORKDIR /usr/src/MedViews

# Copy content
COPY . .

COPY ./entry.sh /

# Installing dependencies
RUN pip3 install -r ./requirements.txt

EXPOSE 8000

# Running the app
ENTRYPOINT ["sh", "/entry.sh"]

