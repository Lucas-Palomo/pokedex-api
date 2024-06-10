# Pokedex API

A Pokedex API made with FastAPI

## Requirements
This application needs:
- Postgres database to store data
- .env to get environment variables

## Running Steps

### Install requirements
```shell
pip3 install -r requirements.txt
```

### Collect data from pokeapi
In this step, we'll learn how to run a web crawler

```shell
python3 src/main.py collect
```
Running the collect command gives you all pokemons and download their images

#### Options
Waiting for the web crawler to run can be boring and tedious, so we can speed up its collection

##### Limiting the web scrap

In this example, we'll capture the first 15 pokémon

```shell
python3 src/main collect --limit --limit-size 15
```

##### Overwrite all web crawler data

```shell
python3 src/main collect --overwrite
```

##### Combined flags
You can combine the limit flag and the override flag

```shell
python3 src/main collect --overwrite --limit --limit-size 15
```

### Migrate all web crawler data to a database
In this step, we'll learn how to send all the data from the web crawler to a database

That is a simple command

```shell
python3 src/main.py migrate
```

### Starting the API
In this step, we'll learn how to run the api

```shell
python3 src/main start
```

#### Custom Host and Port
By default, the host is localhost and the port is 3000

```shell
python3 src/main start --host myserver.com --port 8080
```

## OpenAPI docs

By default, the documentation of all API endpoints can be accessed in /docs

```text
http://localhost:3000/docs
```

## Dotenv Variables

I recommend you copy the `.env-example` to your `.env`

```text
COLLECT_FOLDER="./localdb"
STATIC_FOLDER="./static"

MIGRATIONS_FOLDER="./migrations"

POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_USER="root"
POSTGRES_PASSWORD="toor"
POSTGRES_DB="pokedex"
```

### Explaining variables

- COLLECT_FOLDER
  - Is the web crawler directory
- STATIC_FOLDER
  - Web crawler download images in this folder
- MIGRATIONS_FOLDER
  - In this folder, we have SQL files for creating a database
- POSTGRES_HOST
  - Host used to access the database
- POSTGRES_PORT
  - Port used to access the database
- POSTGRES_USER
  - User used to access the database
- POSTGRES_PASSWORD
  - Password used to access the database
- POSTGRES_DB
  - Default database name used to access the database

## Run containerized
You can run it as a containerized application

Modify the `app.sh` to use custom command flags

```shell
docker-compose up -d --force-recreate
```

