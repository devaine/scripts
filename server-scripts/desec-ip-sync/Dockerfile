FROM node:latest

COPY . /desec

WORKDIR /desec/server-scripts/desec-ip-sync/

RUN apt update && apt install python3.11-venv -y

CMD ["bash", "run.bash"]

