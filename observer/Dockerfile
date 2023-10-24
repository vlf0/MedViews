FROM python:3.11-slim

# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1

# Creating working directory
WORKDIR /usr/src/MedViews

# Copy content
COPY . .
#COPY ["/kisdb_connecting/", "/observer/", "/WebApp/", "db.sqlite3",
#      "Dockerfile", "manage.py", "requirements.txt", "/usr/src/MedViews/"
#      ]

COPY ./observer_entrypoint.sh /

# Installing dependencies
RUN pip3 install -r ./requirements.txt

EXPOSE 8000

# Running the app
ENTRYPOINT ["sh", "/observer_entrypoint.sh"]
#ENTRYPOINT ["sh", "-c", "python3 manage.py collectstatic --no-input && gunicorn observer.wsgi -b 0.0.0.0:8000"]
#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
