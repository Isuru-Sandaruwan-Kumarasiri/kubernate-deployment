# 🌱 Soil Classification App — Kubernetes Deployment

> A machine learning web application that classifies soil types based on physical properties, containerized with Docker and orchestrated with Kubernetes.

---

## 🏗️ Architecture Overview

```
                        ┌─────────────────────────────────────────┐
                        │           Kubernetes Cluster             │
                        │           (namespace: soil-app)          │
                        │                                          │
  User's Browser        │  ┌─────────────┐    ┌────────────────┐  │
  ──────────────        │  │  Frontend   │    │    Backend     │  │
                        │  │  Pod (Nginx)│    │  Pod (Flask)   │  │
  http://localhost:8080 │  │  port: 80   │    │  port: 5000    │  │
  ──────────────────────┼──►             │    │                │  │
                        │  │  Serves:    │    │  /classify     │  │
  http://localhost:5000 │  │  index.html │    │  POST endpoint │  │
  ──────────────────────┼──────────────────────►               │  │
     (API calls)        │  │             │    │  ML Model      │  │
                        │  └──────┬──────┘    └───────┬────────┘  │
                        │         │                   │            │
                        │  ┌──────▼──────┐    ┌───────▼────────┐  │
                        │  │  frontend   │    │   backend      │  │
                        │  │  Service    │    │   Service      │  │
                        │  │LoadBalancer │    │ LoadBalancer   │  │
                        │  │  :8080      │    │   :5000        │  │
                        │  └─────────────┘    └────────────────┘  │
                        └─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
kubernate-deployment/
├── namespace.yaml                  # Kubernetes namespace: soil-app
├── backend/
│   ├── app.py                      # Flask REST API
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Backend container image
│   ├── Training_models/
│   │   └── psb_lr_model.pkl        # Trained ML model (Logistic Regression)
│   ├── backend-deployment.yaml     # Kubernetes Deployment spec
│   └── backend-service.yaml        # Kubernetes Service (LoadBalancer :5000)
└── frontend/
    ├── index.html                  # Soil classification form UI
    ├── style.css                   # Stylesheet
    ├── Dockerfile                  # Frontend container image (Nginx)
    ├── frontend-deployment.yaml    # Kubernetes Deployment spec
    └── frontend-service.yaml       # Kubernetes Service (LoadBalancer :8080)
```

---

## ⚙️ How It Works

1. **User** opens `http://localhost:8080` → served by the **Nginx frontend pod**
2. User fills in soil properties (pH, EC, Bulk Density, Porosity, Moisture Content)
3. On submit, the browser sends a `POST` request to `http://localhost:5000/classify`
4. The **Flask backend pod** receives the data, runs it through the **Logistic Regression model** (`psb_lr_model.pkl`)
5. The prediction result is returned as JSON and displayed on the page

---

## 🚀 Deployment Guide (Docker Desktop + Kubernetes)

### Prerequisites

| Tool | Purpose |
|------|---------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Build images & run containers |
| Kubernetes (enable in Docker Desktop → Settings → Kubernetes) | Orchestrate pods |
| `kubectl` | Interact with the cluster |

---

### Step 1 — Enable Kubernetes in Docker Desktop

Go to **Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply & Restart**

Verify:
```bash
kubectl cluster-info
```

---

### Step 2 — Build Docker Images

```bash
# Build backend image
docker build -t backend:latest ./backend/

# Build frontend image
docker build -t frontend:latest ./frontend/
```

---

### Step 3 — Deploy to Kubernetes

```bash
# Create the namespace
kubectl apply -f namespace.yaml

# Deploy backend
kubectl apply -f backend/backend-deployment.yaml
kubectl apply -f backend/backend-service.yaml

# Deploy frontend
kubectl apply -f frontend/frontend-deployment.yaml
kubectl apply -f frontend/frontend-service.yaml
```

Or apply everything at once:
```bash
kubectl apply -f namespace.yaml -f backend/ -f frontend/
```

---

### Step 4 — Verify Deployment

```bash
# Watch pods come up (both should show 1/1 Running)
kubectl get pods -n soil-app -w

# Check services
kubectl get svc -n soil-app
```

Expected output:
```
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
backend    LoadBalancer   10.x.x.x        localhost     5000/TCP
frontend   LoadBalancer   10.x.x.x        localhost     8080/TCP
```

---

### Step 5 — Access the App

| Service | URL |
|---------|-----|
| 🌐 Frontend (UI) | http://localhost:8080 |
| 🔌 Backend (API) | http://localhost:5000/classify |

---

## 🔧 Useful Commands

```bash
# View live logs
kubectl logs -n soil-app deployment/backend
kubectl logs -n soil-app deployment/frontend

# Describe a pod (for debugging errors)
kubectl describe pod -n soil-app -l app=backend

# Restart deployments after rebuilding images
kubectl rollout restart deployment/backend -n soil-app
kubectl rollout restart deployment/frontend -n soil-app

# Tear down everything
kubectl delete namespace soil-app

# Redeploy from scratch
kubectl apply -f namespace.yaml -f backend/ -f frontend/
```

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ImagePullBackOff` | Image not found in registry | Rebuild image: `docker build -t <name>:latest ./<dir>/` |
| `ErrImagePull` | Wrong `imagePullPolicy` | Set `imagePullPolicy: IfNotPresent` in deployment YAML |
| `Error: Check if backend is running` | Wrong API URL in frontend | Ensure fetch calls `http://localhost:5000/classify` |
| Pod stuck in `Pending` | Insufficient resources | Check `kubectl describe pod -n soil-app <pod-name>` |
| `CrashLoopBackOff` | App crash on startup | Check `kubectl logs -n soil-app deployment/backend` |

---

## 🧠 ML Model Info

- **Algorithm**: Logistic Regression
- **Model file**: `psb_lr_model.pkl`
- **Input features**: pH, EC (Electrical Conductivity), BD (Bulk Density), PR (Porosity), MC (Moisture Content)
- **Output**: Soil classification prediction (integer class label)

---

## 📝 API Reference

### `POST /classify`

**Request Body (JSON):**
```json
{
  "ph": 6.5,
  "ec": 1.2,
  "bd": 1.4,
  "pr": 40.0,
  "mc": 25.0
}
```

**Response:**
```json
{
  "prediction": 2
}
```