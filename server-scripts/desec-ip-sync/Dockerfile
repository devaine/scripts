FROM node:latest

COPY . /desec

WORKDIR /desec/server-scripts/desec-ip-sync/

RUN apt update && apt install python3.11-venv -y

RUN bash run.bash

CMD ["python3", "main.py"]

