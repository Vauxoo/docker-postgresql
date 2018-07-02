FROM postgres:9.6
ENV LC_COLLATE "C"
RUN apt-get update \
    && apt-get install -yq postgis postgresql-9.6-postgis-scripts \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /etc/postgresql/
COPY ./postgresql.conf /etc/postgresql/postgresql.conf
COPY ./00-create_users.sql /docker-entrypoint-initdb.d/00-create_users.sql
RUN chown postgres:postgres -R  /etc/postgresql

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

