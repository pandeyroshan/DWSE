# Distributed Weather Simulation Engine
The Distributed Weather Simulation Engine (DWSE) is a Python-based application that enables users to submit weather simulations for specific geographic regions over a given time period. DWSE will perform simulations by distributing tasks to multiple workers and returning the predicted weather data.

## How to run?

Spin up the containers:

```sh
$ docker-compose up -d --build
```

Go to [http://localhost:8004](http://localhost:8004) to run the tasks and click here to [http://localhost:5556](http://localhost:5556) to view the Flower dashboard.

## Technology used
* Celery
* Postgres
* FastAPI
* redis
* pytest
