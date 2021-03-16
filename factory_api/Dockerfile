FROM python:3.9

RUN python -m pip install --upgrade pip

WORKDIR /factory_api

COPY fact_api.py /factory_api
COPY factory_db.db /factory_api

RUN pip3 --no-cache-dir install flask flask-sqlalchemy requests

CMD ["python3", "fact_api.py"]
