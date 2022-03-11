FROM python:3.9-alpine

WORKDIR /src

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r ./requirements.txt
RUN pip install -r ./requirements-dev.txt

COPY ./app ./app
COPY ./tests ./tests

ENV PYTHONPATH=/src

ENTRYPOINT ["pytest"]
