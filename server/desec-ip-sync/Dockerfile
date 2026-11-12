FROM node:latest

COPY . /desec

WORKDIR /desec

SHELL ["bash", "-c"]

RUN apt update && apt install python3-all-venv -y

RUN "ls -la"

RUN run.bash

ENV PATH="/desec/.venv/bin:$PATH"

CMD ["python3", "main.py"]

