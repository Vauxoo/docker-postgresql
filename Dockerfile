FROM ubuntu:14.04
MAINTAINER Tulio Ruiz <tulio@vauxoo.com>


# Configure locale
RUN locale-gen en_US.UTF-8 && update-locale
RUN echo 'LANG="en_US.UTF-8"' > /etc/default/locale

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y supervisor python-software-properties \
        software-properties-common postgresql-9.3 \
        postgresql-client-9.3 postgresql-contrib-9.3

RUN mkdir -p /var/log/supervisor
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

USER postgres

RUN /etc/init.d/postgresql start \
    && psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" \
    && psql --command "CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';" \
    && createdb -O docker docker

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

USER root

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/usr/bin/supervisord"]
