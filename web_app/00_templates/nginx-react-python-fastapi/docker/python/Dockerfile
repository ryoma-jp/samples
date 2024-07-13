FROM python:3.12.4

WORKDIR /app

COPY ./docker/python/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./backend/ .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "4000"]
