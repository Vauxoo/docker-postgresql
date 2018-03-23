FROM postgres:9.6-alpine
RUN mkdir -p /etc/postgresql/
COPY ./postgresql.conf /etc/postgresql/postgresql.conf
RUN chown postgres:postgres -R  /etc/postgresql
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

