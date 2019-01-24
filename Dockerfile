FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app/

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY flask_app /app/flask_app
COPY tests /app/tests
COPY main.py /app

RUN pytest
