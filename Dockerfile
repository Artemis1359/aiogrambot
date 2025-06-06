FROM python:3.12-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/run.py"]
