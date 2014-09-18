FROM ubuntu:14.04
MAINTAINER Tulio Ruiz <tulio@vauxoo.com>


# Configure locale
RUN locale-gen en_US.UTF-8 && update-locale
RUN echo 'LANG="en_US.UTF-8"' > /etc/default/locale

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y supervisor python-software-properties \
        software-properties-common postgresql-common python-psycopg2

# Do not create main cluster
RUN sed -ri 's/#(create_main_cluster) .*$/\1 = false/' /etc/postgresql-common/createcluster.conf

# Install postgres and clean
RUN apt-get install -y postgresql-9.3 \
        postgresql-client-9.3 postgresql-contrib-9.3 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor

ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD files/entry_point.py /entry_point.py
ADD files/config_db.py /config_db.py
RUN chmod +x /entry_point.py && chmod +x /config_db.py

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/entry_point.py"]
