import csv
import os
import time

RECEIPTS_FILE = os.getenv("ONE_C_EXPORT_PATH", "/data/receipts.csv")
SYNC_INTERVAL_SECONDS = int(os.getenv("SYNC_INTERVAL_SECONDS", "10"))


def load_receipts():
    if not os.path.exists(RECEIPTS_FILE):
        return []

    with open(RECEIPTS_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def sync_once():
    receipts = load_receipts()
    print(f"worker heartbeat: loaded {len(receipts)} receipts from 1C mock export", flush=True)


print("jewelry receipt sync worker started", flush=True)

while True:
    sync_once()
    time.sleep(SYNC_INTERVAL_SECONDS)
