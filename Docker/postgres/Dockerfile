FROM postgres:latest

ENV POSTGRES_DB=syskidatabase
ENV POSTGRES_USER=syskiuser
ENV POSTGRES_PASSWORD=syskipassword

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

VOLUME ["/workspaces/webTools/Docker/postgres/data"]
