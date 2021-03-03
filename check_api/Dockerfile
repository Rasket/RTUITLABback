FROM python:3-alpine

RUN python -m pip install --upgrade pip

WORKDIR /check_api

COPY check_api.py /check_api
COPY check_db.db /check_api

RUN pip3 --no-cache-dir install flask flask-sqlalchemy flask-restful requests flask_bootstrap


CMD ["python3", "check_api.py"]