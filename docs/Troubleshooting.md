# Troubleshooting Guide

## Overview

This document lists common issues encountered during the development and deployment of FreshLense 2.0, together with their causes and resolutions.

---

# Backend Fails to Start

## Symptoms

- Backend container exits immediately
- API unavailable
- Health endpoint returns an error

## Resolution

Check backend logs:

```bash
docker logs freshlense-backend
```

Verify:

- Environment variables
- MongoDB availability
- Python dependency installation

---

# MongoDB Connection Failure

## Symptoms

```
Connection refused
```

or

```
MongoServerSelectionTimeoutError
```

## Resolution

Verify MongoDB container:

```bash
docker ps
```

Check connectivity:

```bash
docker logs freshlense-mongodb
```

Verify:

```
MONGO_URI
```

inside the environment configuration.

---

# Frontend Health Check Failing

## Symptoms

Container remains:

```
unhealthy
```

## Cause

Health check attempted to connect using:

```
http://localhost
```

inside the container, which resolved to IPv6 (::1), while Nginx was listening on IPv4.

## Resolution

Update Dockerfile health check:

```dockerfile
HEALTHCHECK CMD wget --spider -q http://127.0.0.1 || exit 1
```

Rebuild the frontend container.

---

# CORS Errors

## Symptoms

Browser displays:

```
CORS Policy Error
```

## Resolution

Ensure frontend origin is included in:

```
ALLOWED_ORIGINS
```

Verify FastAPI CORS configuration.

---

# GitHub Actions Build Failure

## Resolution

Verify:

- Dockerfile paths
- Workflow syntax
- Docker Hub credentials
- Repository secrets

---

# Jenkins Deployment Failure

## Resolution

Check:

```bash
docker logs jenkins
```

Verify:

- SSH keys
- Docker permissions
- Jenkins credentials
- GitHub webhook delivery

---

# Docker Networking Issues

## Symptoms

Containers cannot communicate.

## Resolution

Inspect Docker network:

```bash
docker network inspect freshlense_default
```

Verify containers belong to the same bridge network.

---

# Prometheus Target Down

## Symptoms

Target status:

```
DOWN
```

## Resolution

Verify:

```bash
curl http://localhost:8000/metrics
```

Check:

- Prometheus configuration
- Backend container
- Network connectivity

---

# Grafana Dashboard Empty

## Resolution

Verify:

- Prometheus datasource
- Dashboard queries
- Metrics endpoint
- Scrape status

---

# Loki Not Receiving Logs

## Resolution

Check:

```bash
docker logs freshlense-promtail
```

Verify:

- Promtail configuration
- Loki endpoint
- Docker log mounts

---

# Alertmanager Not Triggering Alerts

## Resolution

Verify:

- Alert rules
- Prometheus configuration
- Alertmanager targets

---

# Metrics Not Increasing

## Symptoms

```
freshlense_crawl_requests_total
```

remains zero.

## Resolution

Ensure crawler requests pass through:

```
fetch_url()
```

Verify:

- Counter increment
- Metrics endpoint
- Prometheus scraping

---

# Email OTP Not Received

## Resolution

Verify:

```
RESEND_API_KEY
```

If the key is absent, email delivery is disabled and OTPs are only logged locally.

---

# AI Features Disabled

## Symptoms

```
OPENAI_API_KEY not set
```

## Resolution

Configure:

```
OPENAI_API_KEY
```

Restart the backend.

---

# General Diagnostics

Useful commands:

```bash
docker ps
```

```bash
docker compose logs -f
```

```bash
docker logs freshlense-backend
```

```bash
curl http://localhost:8000/health
```

```bash
curl http://localhost:8000/metrics
```

```bash
docker network inspect freshlense_default
```

---

# Summary

Most deployment issues can be diagnosed by checking container health, Docker networking, application logs, and Prometheus metrics. FreshLense exposes dedicated health and metrics endpoints to simplify troubleshooting and operational monitoring.