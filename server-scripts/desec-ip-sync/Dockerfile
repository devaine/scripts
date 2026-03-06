FROM node:latest

COPY . /desec

WORKDIR /desec/server-scripts/desec-ip-sync/

SHELL ["bash", "-c"]

RUN apt update && apt install python3.11-venv -y

RUN bash run.bash

ENV PATH="$PWD/venv/bin:$PATH"

CMD ["python3", "main.py"]

