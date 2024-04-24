FROM python:3.12-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt-get install -y python3-dev libevent-dev build-essential gcc g++

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv .env
RUN source .env/bin/activate
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

RUN weasel run setup

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]

