FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1


WORKDIR /MedViews
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
