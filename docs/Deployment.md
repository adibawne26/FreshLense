# Deployment Guide

## Overview

FreshLense 2.0 is deployed using Docker Compose.

The deployment consists of multiple containers working together:

- Frontend
- Backend
- MongoDB
- Prometheus
- Grafana
- Loki
- Promtail
- Alertmanager
- Node Exporter

---

# Prerequisites

Install:

- Docker
- Docker Compose
- Git

Verify installation:

```bash
docker --version
docker compose version
git --version
```

---

# Clone Repository

```bash
git clone https://github.com/adibawne26/FreshLense.git
cd FreshLense
```

---

# Configure Environment Variables

Create the environment file.

Example:

```env
MONGO_URI=mongodb://mongodb:27017/freshlense

REACT_APP_BACKEND_URL=http://backend:8000

OPENAI_API_KEY=

RESEND_API_KEY=
```

---

# Build Containers

```bash
docker compose build
```

---

# Start Application

```bash
docker compose up -d
```

---

# Verify Containers

```bash
docker ps
```

Expected containers:

- freshlense-frontend
- freshlense-backend
- freshlense-mongodb
- freshlense-prometheus
- freshlense-grafana
- freshlense-loki
- freshlense-promtail
- freshlense-alertmanager
- freshlense-node-exporter

---

# Application URLs

## Frontend

```
http://localhost
```

## Backend

```
http://localhost:8000
```

## API Documentation

```
http://localhost:8000/docs
```

## Prometheus

```
http://localhost:9090
```

## Grafana

```
http://localhost:3000
```

## Alertmanager

```
http://localhost:9093
```

---

# Health Checks

Verify backend:

```bash
curl http://localhost:8000/health
```

Verify metrics:

```bash
curl http://localhost:8000/metrics
```

---

# Logs

View backend logs:

```bash
docker logs freshlense-backend
```

View frontend logs:

```bash
docker logs freshlense-frontend
```

Follow logs:

```bash
docker compose logs -f
```

---

# Updating the Application

Pull latest changes:

```bash
git pull
```

Rebuild:

```bash
docker compose build
```

Restart:

```bash
docker compose up -d
```

---

# Stopping the Application

```bash
docker compose down
```

---

# Production Deployment

Production deployment follows the same workflow but uses:

```bash
docker compose -f docker-compose.prod.yaml up -d
```

The production environment is integrated with:

- GitHub Actions
- Docker Hub
- Jenkins
- Automated deployment
- Health checks

---

# Troubleshooting

## Backend not starting

Check:

```bash
docker logs freshlense-backend
```

---

## MongoDB connection issues

Verify:

```bash
docker ps
```

Ensure MongoDB is healthy.

---

## Frontend unavailable

Check:

```bash
docker logs freshlense-frontend
```

Verify Nginx health.

---

## Monitoring not working

Verify:

- Prometheus targets
- Grafana datasource
- Loki datasource
- Promtail logs

---

# Deployment Summary

FreshLense provides a production-ready deployment pipeline using containerized services, automated CI/CD, centralized monitoring, and observability tools, enabling reliable and repeatable deployments across environments.