FROM python:3.11.5

WORKDIR /KinopoiskApiDev

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt