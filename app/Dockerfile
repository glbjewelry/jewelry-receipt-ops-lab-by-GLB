FROM python:3.12-slim

WORKDIR /app

COPY main.py .

ENV ONE_C_EXPORT_PATH=/data/receipts.csv

EXPOSE 8000

CMD ["python", "main.py"]
