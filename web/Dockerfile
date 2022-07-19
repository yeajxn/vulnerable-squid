# syntax=docker/dockerfile:1
FROM python:3.10-slim
WORKDIR /home/app/web
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY 'Asupersecret!'
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]