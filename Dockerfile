FROM python:3.11-slim

WORKDIR /app

# Install netcat for wait-for-it.sh
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "main.py"]

ENV PYTHONPATH=/app
