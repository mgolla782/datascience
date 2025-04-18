FROM python:3.10-slim

RUN apt-get update && apt-get install -y poppler-utils poppler-data tesseract-ocr libgl1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
