FROM python:3.13-slim-bookworm

USER root

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY etc ./etc
COPY README.md .
COPY .env .

CMD ["bash", "etc/docker/init.sh"]

