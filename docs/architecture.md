# System Architecture

## Component Overview
RenewTwin operates on a modular, decoupled architecture consisting of a React-based frontend, a FastAPI Python backend, and an integrated Machine Learning inference pipeline. Data persistence for the prototype is managed by SQLite.

## Core Modules

### 1. Data Acquisition Layer (Prototype)
- **Visual Data Ingestion**: Endpoints for uploading ELPV imagery for defect classification.
- **Telemetry Simulator**: Injects synthetic voltage, current, and temperature data to simulate physical asset output.

### 2. Machine Learning Inference Pipeline
- **Computer Vision Service**: PyTorch-based service hosting a fine-tuned ResNet-18 model. It processes incoming panel imagery, resizes and normalizes the input, and returns classification probabilities for four conditions (none, crack, hotspot, inactive).
- **Anomaly Detection Service**: A scikit-learn Isolation Forest model trained on normative telemetry baselines. It scores the likelihood that incoming operational metrics represent a deviation from expected performance.

### 3. Digital Twin Engine
- Acts as the central synchronization hub.
- Consolidates real-time predictions from the ML pipeline and updates the asset registry.
- Computes the dynamic **Asset Health Index (AHI)** and updates the **Risk Classification**.

### 4. RESTful API Gateway
- Developed using FastAPI to ensure high throughput and asynchronous handling of requests.
- Serves endpoints for data ingestion, digital twin querying, and maintenance scheduling.

### 5. Frontend Dashboard
- A React (Vite) Single Page Application.
- Consumes the API to provide a comprehensive, real-time interface mapping the status of all assets.

## Data Flow
1. Telemetry and visual data are pushed to the FastAPI backend.
2. The backend routes data to the respective ML models for inference.
3. Model outputs (defect probabilities, anomaly scores) are passed to the Digital Twin Engine.
4. The Engine updates the asset state in the SQLite database and recalculates health metrics.
5. The React frontend periodically polls the API and updates the dashboard view to reflect real-time asset conditions.
