FROM python:3.9

RUN python -m pip install --upgrade pip

WORKDIR /shop_api

COPY models.py /shop_api
COPY shop_api.py /shop_api
COPY db.db /shop_api

RUN pip3 --no-cache-dir install flask flask-sqlalchemy flask-restful requests


CMD ["python3", "shop_api.py"]
