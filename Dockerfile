FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y gcc build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py setup.py
RUN pip install .

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]