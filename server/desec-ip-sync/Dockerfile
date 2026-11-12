FROM node:latest

COPY . /desec

WORKDIR /desec

RUN apt update && apt install python3-all-venv -y

RUN ./run.bash

ENV PATH="/desec/.venv/bin:$PATH"

CMD ["python3", "main.py"]

