# Jewelry Receipt Ops Lab

![CI](https://github.com/glbjewelry/jewelry-receipt-ops-lab-by-GLB/actions/workflows/ci.yml/badge.svg)

A DevOps/backend lab that simulates a jewelry workshop workflow where physical numbered receipts are registered in 1C and synchronized into an operational tracking platform.

## Business Context

In the real workshop process, scrap metal intake and custom jewelry manufacturing orders are registered using physical numbered receipts. These receipts are then recorded in 1C.

This project does not connect to a real 1C instance. Instead, it simulates 1C integration using CSV/JSON mock exports so that no production data, credentials, or private business records are stored in GitHub.

## Architecture

Current implemented flow:

```text
1C mock export CSV
        |
        v
API service
        |
        +--> /receipts
        |
        +--> /metrics
                  |
                  v
            Prometheus
                  |
                  v
              Grafana
                  |
                  v
          Telegram alerts

## Planned target architecture:
physical numbered receipt
        |
        v
1C registration
        |
        v
1C mock export: CSV/JSON
        |
        v
sync worker
        |
        v
PostgreSQL
        |
        +--> API service
        |
        +--> metrics endpoint
                  |
                  v
            Prometheus
                  |
                  v
              Grafana
                  |
                  v
               Alerts

```

## Monitoring and Alerting

The project exposes Prometheus-compatible metrics from the API service:

```text
jewelry_receipts_total
jewelry_receipts_registered
jewelry_receipts_in_work
jewelry_receipts_ready
jewelry_receipts_issued
jewelry_receipts_cancelled
```
A business alert is configured for ready orders:

```text
jewelry_receipts_ready > 0
```

## Planned services:

api          HTTP API for receipts and statuses
worker       background sync worker for 1C mock exports
postgres     receipt/order storage
redis        queue/cache layer
nginx        reverse proxy
prometheus   metrics collection
grafana      dashboards and alerts

## Receipt model

receipt_number        physical numbered receipt ID
one_c_document_id     simulated 1C document ID
customer_name         customer name
operation_type        scrap_purchase / custom_order / repair / resizing
jewelry_type          ring / chain / pendant / earrings
metal                 gold / silver / platinum
metal_weight_grams    metal weight
stone                 optional stone information
status                registered / in_work / ready / issued / cancelled
created_at            creation timestamp
updated_at            update timestamp

## Planned endpointz:

GET  /health
GET  /metrics
POST /sync/1c
GET  /receipts
GET  /receipts/{receipt_number}
PATCH /receipts/{receipt_number}/status

## DevOps goals:

- Docker Compose stack
- PostgreSQL persistence
- Redis queue/cache layer
- background worker
- Nginx reverse proxy
- Prometheus metrics
- Grafana dashboards
- alerting for stuck receipts and failed sync
- GitHub Actions CI
- smoke tests
- safe mock 1C integration


## Security Note
Real 1C credentials, production exports, personal customer data, and private workshop records must never be committed to GitHub.
