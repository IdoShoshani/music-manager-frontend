# frontend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]







