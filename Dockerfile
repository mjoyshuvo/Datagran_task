FROM python:3.6
ADD . /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt