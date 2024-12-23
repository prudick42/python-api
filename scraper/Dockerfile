FROM python:3.12.3

WORKDIR /app

COPY scrapery.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scrapery.py"]