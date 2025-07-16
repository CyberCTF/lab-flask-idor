FROM python:3.11-slim
WORKDIR /app
COPY build/requirements.txt ./
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY deploy/ ../deploy/
COPY build/ ./
EXPOSE 5000
CMD ["python", "app.py"] 