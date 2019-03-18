FROM mysql:latest
LABEL Alberto G "albert111.garcia@gmail.com"

RUN apt-get update && apt-get install vim -y

COPY . /db/files

# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

WORKDIR /db