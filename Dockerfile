FROM python:3.9.5

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /requirements.txt .
RUN pip install -r requirements.txt

COPY src .

CMD gunicorn --worker-class gevent \
  --workers $WORKERS \
  --bind 0.0.0.0:$PORT \
  wsgi_app:app