FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app/

COPY requirements.txt /app/
RUN pip install -r ./requirements.txt

COPY flask_app /app/flask_app
COPY tests /app/tests
COPY main.py /app

ARG MODEL_FILE=./model/model.tar.gz
ADD ${MODEL_FILE} /model/
ENV ML_MODEL_PATH=/model/model.pkl

ARG MODEL_TEST_FILE=./model/test_data.json
COPY ${MODEL_TEST_FILE} /model/test_data.json

RUN pytest
RUN python /app/tests/run_accuracy_tests.py ${ML_MODEL_PATH} /model/test_data.json
