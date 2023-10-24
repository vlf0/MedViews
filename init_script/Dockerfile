FROM postgres:15.4

# Set up Ru locale in container
RUN apt-get install locales -y

# Uncommenting strings of locales in locale.gen file
RUN sed -i 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/g' /etc/locale.gen

# Setting environment variables of needed locale
ENV LANGUAGE ru_RU.utf8
ENV LANG ru_RU.utf8
ENV LC_ALL ru_RU.utf8

# Write needed locale string in locale-gen file and then updating locale
RUN locale-gen ru_RU.utf8 && update-locale LANG=ru_RU.utf8 LANGUAGE=ru_RU.utf8 LC_ALL=ru_RU.utf8

# Creating working directory
WORKDIR /var/vib/postgres
