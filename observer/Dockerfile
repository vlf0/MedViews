FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1


WORKDIR /MedViews
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["gunicorn", "observer.wsgi", "-b", "10.123.8.17:8000"]
