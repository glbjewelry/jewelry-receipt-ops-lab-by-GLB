from http.server import BaseHTTPRequestHandler, HTTPServer
import csv
import json
import os
from urllib.parse import urlparse

RECEIPTS_FILE = os.getenv("ONE_C_EXPORT_PATH", "one-c-mock/receipts.csv")
APP_NAME = "jewelry-receipt-ops-lab-by-GLB"

def load_receipts():
    if not os.path.exists(RECEIPTS_FILE):
        return []

    with open(RECEIPTS_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def find_receipt(receipt_number):
    for receipt in load_receipts():
        if receipt["receipt_number"] == receipt_number:
            return receipt

def build_metrics():
    receipts = load_receipts()

    total = len(receipts)
    registered = sum(receipt["status"] == "registered" for receipt in receipts)
    in_work = sum(receipt["status"] == "in_work" for receipt in receipts)
    ready = sum(receipt["status"] == "ready" for receipt in receipts)
    issued = sum(receipt["status"] == "issued" for receipt in receipts)
    cancelled = sum(receipt["status"] == "cancelled" for receipt in receipts)

    return (
        f"jewelry_receipts_total {total}\n"
        f"jewelry_receipts_registered {registered}\n"
        f"jewelry_receipts_in_work {in_work}\n"
        f"jewelry_receipts_ready {ready}\n"
        f"jewelry_receipts_issued {issued}\n"
        f"jewelry_receipts_cancelled {cancelled}\n"
    )

    return None

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = (json.dumps(data) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, status=200):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._send_json({
                "service": APP_NAME,
                "message": "1C jewelry receipt operations lab"
            })

        elif path == "/health":
            self._send_json({"status": "ok"})

        elif path == "/metrics":
            self._send_text(build_metrics())

        elif path == "/receipts":
            self._send_json({"receipts": load_receipts()})

        elif path.startswith("/receipts/"):
            receipt_number = path.split("/")[-1]
            receipt = find_receipt(receipt_number)

            if receipt is None:
                self._send_json({"error": "receipt not found"}, 404)
            else:
                self._send_json(receipt)
        else:
            self._send_json({"error": "not found"}, 404)

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Jewelry Receipt Ops API running on port 8000")
server.serve_forever()

