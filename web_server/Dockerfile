FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --requirement /app/requirements.txt
COPY . /app/

WORKDIR /app/

EXPOSE 5000:5000

ENTRYPOINT ["python3"]
CMD ["front_api.py"]
