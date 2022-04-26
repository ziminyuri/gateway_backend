FROM python:3.10-slim-buster

WORKDIR /usr/src/app

EXPOSE 5000

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src

CMD ["gunicorn", "src.wsgi:app", "--bind", "0.0.0.0:5000"]
