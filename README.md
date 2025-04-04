Put the following env variables into .env file

```
POSTGRES_HOST = guardian_db
POSTGRES_USER = guardian
POSTGRES_PASSWORD = guardian
POSTGRES_DB = guardian
POSTGRES_PORT = 5432
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

build app 
```
docker compose build

```

Run the app

```
docker compose up
```

Go to `http://0.0.0.0:8000/docs` and test endpoints
