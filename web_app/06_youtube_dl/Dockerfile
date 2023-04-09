FROM python:3.10.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt update -y ; \
    apt install -y sqlite3 libgl1-mesa-dev

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

