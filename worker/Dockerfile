FROM python:3.12-slim

WORKDIR /worker

COPY worker.py .

ENV ONE_C_EXPORT_PATH=/data/receipts.csv
ENV SYNC_INTERVAL_SECONDS=10

CMD ["python", "worker.py"]
