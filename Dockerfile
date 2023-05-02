FROM python:3.10

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN python3 -m pip install -U pip

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY . .