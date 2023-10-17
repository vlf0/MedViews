FROM python:3.11-slim
# Making container logs unbuffered
ENV PYTHONUNBUFFERED 1



WORKDIR /usr/src/MedViews

# Copy content
COPY . .

# Installing dependencies
RUN pip3 install -r ./requirements.txt

RUN apt-get update
# Set up Ru locale in container
RUN apt-get install locales -y
RUN sed -i 's/# ru_RU.CP1251 CP1251/ru_RU.CP1251 CP1251/g' /etc/locale.gen

ENV LANGUAGE ru_RU.cp1251
ENV LANG ru_RU.cp1251
ENV LC_ALL ru_RU.cp1251
RUN locale-gen ru_RU.CP1251 && update-locale LANG=ru_RU.cp1251 LANGUAGE=ru_RU.cp1251 LC_ALL=ru_RU.cp1251

EXPOSE 8000

# Running the app
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
