FROM ubuntu:14.04
MAINTAINER Tulio Ruiz <tulio@vauxoo.com>

# Configure locale
RUN locale-gen en_US.UTF-8 && update-locale
RUN echo 'LANG="en_US.UTF-8"' > /etc/default/locale
RUN apt-get update && apt-get install wget -yq
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    sudo apt-key add -
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main' > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y supervisor python-software-properties \
        software-properties-common postgresql-common python-psycopg2

# Do not create main cluster
RUN sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf

# Install postgres and clean
RUN apt-get install -y postgresql-9.5 \
        postgresql-client-9.5 postgresql-contrib-9.5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /var/log/supervisor

COPY files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY files/entry_point.py /entry_point.py
COPY files/config_db.py /config_db.py
RUN chmod +x /entry_point.py && chmod +x /config_db.py

# Create the directory for the postgres logs and configure postgres
COPY files/common-vauxoo.conf /etc/postgresql-common/common-vauxoo.conf
RUN mkdir -p /var/log/pg_log
RUN chmod 0757 -R /var/log/pg_log

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/supervisor", "/var/lib/postgresql"]

ENTRYPOINT ["/entry_point.py"]
