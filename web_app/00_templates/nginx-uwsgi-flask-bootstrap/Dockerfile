FROM python:3.8

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

CMD ["uwsgi", "app.ini"]
