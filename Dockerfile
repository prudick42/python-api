FROM python:3.12.3

WORKDIR /app

COPY apps/ ./apps
COPY data/ ./data
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "apps/app.py"]