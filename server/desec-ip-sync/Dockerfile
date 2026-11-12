FROM node:latest

COPY . /desec

WORKDIR /desec/server/desec-ip-sync/

SHELL ["bash", "-c"]

RUN apt update && apt install python3-all-venv -y

RUN bash run.bash

ENV PATH="/desec/server/desec-ip-sync/venv/bin:$PATH"

CMD ["python3", "main.py"]

