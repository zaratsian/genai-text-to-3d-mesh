FROM nvidia/cuda:11.8.0-base-ubuntu22.04

RUN apt update && \
apt install -y software-properties-common git && \
add-apt-repository ppa:deadsnakes/ppa && \
DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata &&\
apt install -y python3.9 && \
apt install -y python3-pip

WORKDIR /app

COPY init.py main.py mlconfig.py requirements.txt /app/

RUN git clone https://github.com/openai/point-e.git && \
cd point-e && pip install -e . && \
python3 /app/init.py && \
pip3 install -r /app/requirements.txt

EXPOSE 8501

ENTRYPOINT ["python3", "/app/main.py"]
