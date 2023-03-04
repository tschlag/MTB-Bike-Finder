# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /mtb-bike-compare-image

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--port=8000", "--host=0.0.0.0"]