FROM python:3.9

RUN python -m pip install --upgrade pip

WORKDIR /check_api

COPY check_api.py /check_api
COPY check_db.db /check_api
COPY templates/ /check_api/templates
COPY templates/base.html /check_api/templates

RUN pip3 --no-cache-dir install flask flask-sqlalchemy flask-restful requests flask_bootstrap

CMD ["python3", "check_api.py"]