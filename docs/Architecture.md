# FreshLense 2.0 Architecture

## Overview

FreshLense 2.0 is a cloud-native web content monitoring platform that continuously tracks web pages, detects meaningful content changes, performs AI-assisted fact verification, and provides analytics through a modern dashboard.

The platform follows a modular architecture consisting of independent frontend, backend, database, monitoring, logging, and CI/CD components. Every component is containerized using Docker and orchestrated with Docker Compose, making the system portable, scalable, and easy to deploy.

---

# High-Level Architecture

![System Architecture](images/system-architecture.png)

---

# Core Components

## React Frontend

The frontend provides the primary user interface.

### Responsibilities

- User authentication
- Dashboard
- Analytics
- Page management
- Fact verification
- Monitoring results
- API communication

Technology Stack

- React
- TypeScript
- Axios
- Material UI

---

## FastAPI Backend

The backend acts as the central orchestration layer.

### Responsibilities

- REST API
- JWT Authentication
- Multi-Factor Authentication (MFA)
- Page monitoring
- Scheduler
- Change detection
- Fact verification
- Analytics
- Metrics exposure

Technology Stack

- FastAPI
- Python
- Pydantic
- Uvicorn

---

## MongoDB

MongoDB stores all application data.

Collections include:

- Users
- Tracked Pages
- Page Versions
- Change Logs
- Fact Check Results

---

## Chrome Extension

The browser extension allows users to send web pages directly to FreshLense for monitoring without manually copying URLs.

---

# Monitoring Workflow

The monitoring scheduler periodically checks tracked websites.

Workflow:

1. Scheduler starts crawl.
2. Content Fetcher downloads page.
3. HTML is cleaned.
4. Text is extracted.
5. New version is stored.
6. Difference engine compares versions.
7. Freshness score is calculated.
8. Fact verification is performed.
9. Dashboard is updated.
10. Alerts are generated if required.

---

# Authentication Flow

FreshLense implements secure authentication using:

- JWT tokens
- Password hashing
- Multi-Factor Authentication (Email OTP)

Every protected endpoint validates the access token before serving requests.

---

# Observability Stack

FreshLense includes a complete observability stack.

## Metrics

- Prometheus
- Custom application metrics
- Health endpoints

## Dashboards

- Grafana

Displays:

- Crawl requests
- Crawl success rate
- Crawl duration
- System metrics

## Logging

- Loki
- Promtail

Centralized application logs are collected from Docker containers and visualized through Grafana.

## Alerting

Alertmanager routes alerts based on Prometheus rules.

---

# CI/CD Pipeline

Deployment is fully automated.

Developer
↓

GitHub Repository
↓

GitHub Actions (CI)

↓

Docker Hub

↓

Jenkins (CD)

↓

Production Deployment

GitHub Actions builds container images.

Jenkins automatically pulls updated images and redeploys the application after successful builds.

---

# Deployment

The application is deployed using Docker Compose.

Services include:

- Frontend
- Backend
- MongoDB
- Prometheus
- Grafana
- Loki
- Promtail
- Alertmanager
- Node Exporter

Each service runs inside its own isolated container.

---

# Design Principles

FreshLense follows several software engineering principles.

- Modular architecture
- Separation of concerns
- Containerized deployment
- Infrastructure observability
- Automated CI/CD
- Secure authentication
- Scalable service design

---

# Future Improvements

Planned enhancements include:

- Kubernetes deployment
- Helm Charts
- Terraform infrastructure
- Multi-node deployments
- Horizontal scaling
- Distributed crawling
- Cloud-native deployment on AWS/GCP