FROM python:3.9

RUN python -m pip install --upgrade pip

WORKDIR /shop_api

COPY models.py /api
COPY shop_api.py /api
COPY db.db /api

RUN pip3 --no-cache-dir install flask flask-sqlalchemy flask-restful requests


CMD ["python3", "shop_api.py"]
