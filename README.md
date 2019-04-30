# Telocam-server

# Guides

- Boilerplate Flask https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

# JWT Authentication

- Usamos JWT tokens para atenticar a los usuarios

## Set up with Docker

- Install docker in [local development computer](https://www.docker.com/products/docker-desktop) & [server](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- To build / re-build containers

```bash
docker-compose up --build
```

- To build / re-build a specific container

```bash
docker-compose up --build postgress
docker-compose up --build api
```

- To run a container in detach mode (background process)

```bash
docker-compose up -d
```

## Setup development enviroment

```bash

# Crear virtual enviroment
virtualenv -p python3 env

# Activar virtualenv
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Editar fichero app/main/config.py o exportar variable entorno
BD_PASSWORD              // default: proyecto_software
BD_NAME

```

## Build Setup

```bash

# crear base de dados en mysql server
CREATE DATABASE proyecto-software

# Create migration folder
python manage.py db init

# Create a migration script from the detected changes in the model
python manage.py db migrate --message 'initial database migration'

#Apply the migration script to the database
python manage.py db upgrade

```

## Build Setup

```bash
# Run
python manage.py run

#Test
python manage.py test

```
