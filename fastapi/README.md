# Fastapi celery progess bar

This project is an example for using fastapi, celery to create a progress bar
for long running tasks like machine learning model training, data processing
etc.

# How to install?

#### You need install redis first on your computer or server

first create a virtual env

```
python3 -m venv venv
```

then activate virtual env

```
source ./venv/bin/activate
```

then install requirements

```
pip install -r requirements.txt
```

now run the server

```
uvicorn main:app --port 8000 --reload
```

run celery

```
celery -A main.celery 
worker --loglevel=info
```
