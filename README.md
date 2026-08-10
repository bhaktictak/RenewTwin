# RenewTwin — AI-Powered Digital Twin for Predictive Management of Renewable Energy Assets

An AI-driven digital asset management platform for renewable energy infrastructure. Combines computer vision defect detection with operational anomaly analysis to build intelligent digital twins that assess asset health, predict risk, and prioritize maintenance.

## Problem Statement
Renewable energy plants contain thousands of distributed assets (solar panels, inverters, transformers). Performance degrades due to defects, thermal anomalies, soiling, corrosion, and environmental exposure. Traditional periodic inspection delays detection and increases avoidable energy loss and maintenance costs. Manual inspection of large solar farms is time-consuming, expensive, and unable to provide continuous monitoring.

## Solution
RenewTwin creates continuously updated digital representations of each physical asset. The platform combines:
- AI-based visual defect detection using computer vision
- Operational anomaly detection using statistical/ML methods
- A digital twin engine that consolidates these signals
- Transparent health scoring and risk classification
- Prioritized maintenance recommendations

## Why Digital Twins?
A digital twin consolidates multiple data streams (visual inspection, operational metrics, environmental data) into a single, continuously updated asset representation. Unlike traditional dashboards showing current values, a digital twin contextualizes observations against asset history, fleet baselines, and AI analysis.

## Key Features
- **Asset Registry**: Centralized inventory mapping of all physical assets and their technical specifications.
- **Digital Twin Engine**: Core system managing state synchronization between physical assets and digital representations.
- **CNN Defect Detection**: Computer vision pipeline identifying surface and thermal anomalies on solar panels.
- **Anomaly Detection**: Unsupervised machine learning models analyzing operational telemetry.
- **Health Index**: Composite metric indicating overall asset degradation and operating state.
- **Risk Classification**: Automated categorization of failure probability and operational impact.
- **Maintenance Prioritization**: Resource-optimized scheduling based on risk levels and impact severity.
- **Operator Dashboard**: Comprehensive visualization interface for real-time asset monitoring and management.

## System Architecture

```text
                PHYSICAL ASSETS
                       │
                       ↓
             DATA ACQUISITION
             ┌─────────┴─────────┐
             ↓                   ↓
       VISUAL DATA         OPERATIONAL DATA
             │                   │
             ↓                   ↓
      COMPUTER VISION      ANOMALY ANALYSIS
             │                   │
             └─────────┬─────────┘
                       ↓
                DIGITAL TWIN
                       │
                       ↓
              ASSET HEALTH INDEX
                       │
                       ↓
               RISK PREDICTION
                       │
                       ↓
            MAINTENANCE PRIORITY
                       │
                       ↓
                  DASHBOARD
```

## AI/ML Methodology
- **Visual Defect Detection**: Transfer learning with ResNet-18, fine-tuned for 4-class solar panel defect classification (none, crack, hotspot, inactive).
- **Anomaly Detection**: Isolation Forest on operational parameters (current, voltage, temperature).
- **Why ResNet-18**: Proven architecture, fast to fine-tune, good accuracy-speed tradeoff for prototype development.
- **Target dataset**: ELPV Electroluminescence dataset (2,624 images) for production-grade validation.
- **Current prototype**: Synthetic demo data for pipeline demonstration and architecture validation.

## Digital Twin Model

```json
{
  "asset_id": "PV-A-0174",
  "asset_type": "Solar PV Panel",
  "location": "Array A / Row 17",
  "rated_capacity_kw": 0.55,
  "current_power_kw": 0.41,
  "expected_power_kw": 0.51,
  "temperature_c": 67.2,
  "defect_class": "hotspot",
  "defect_probability": 0.87,
  "anomaly_score": 0.81,
  "health_score": 62,
  "risk_level": "AT_RISK",
  "maintenance_priority": 1,
  "recommended_action": "Inspect thermal condition",
  "data_source": "SYNTHETIC_DEMO"
}
```

## Prototype Asset Health Index
The Asset Health Index (AHI) is a synthetic metric calculated using weighted parameters:
`AHI = 100 - (W1 * Visual_Defect_Penalty + W2 * Anomaly_Score_Penalty + W3 * Performance_Deviation)`
- *Visual Defect Penalty*: Based on defect severity (hotspot > crack > inactive).
- *Anomaly Score Penalty*: Normalized isolation forest anomaly score.
- *Performance Deviation*: `|current_power - expected_power| / expected_power`.

**Risk Thresholds:**
- **HEALTHY**: 85 - 100
- **MONITOR**: 70 - 84
- **AT_RISK**: 50 - 69
- **CRITICAL**: < 50

*Note: This formula and the associated weights are designed for prototype demonstration and require calibration against historical maintenance data.*

## Maintenance Prioritization
Assets are ranked based on a combination of their Risk Level (CRITICAL > AT_RISK > MONITOR) and their capacity impact (rated capacity * performance deviation). Assets requiring immediate attention due to severe visual defects or critical telemetry anomalies are prioritized highest.

## Technology Stack

| Component | Technology |
| :--- | :--- |
| **Machine Learning** | Python, PyTorch, scikit-learn, OpenCV |
| **Backend & API** | FastAPI, Uvicorn, Python |
| **Database** | SQLite |
| **Frontend UI** | React, Vite, JavaScript |
| **Version Control** | Git |

## Project Structure
```text
RenewTwin/
├── backend/
│   ├── database/
│   ├── models/
│   ├── routes/
│   └── services/
├── docs/
│   ├── architecture.md
│   └── methodology.md
├── frontend/
├── ml/
│   ├── data/
│   ├── models/
│   └── notebooks/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Dataset
- **Current Data**: Synthetic demo data generated programmatically to test the API and dashboard interfaces. *Clearly labeled as SYNTHETIC_DEMO in the system.*
- **Target Data**: ELPV Electroluminescence dataset (Buerhop-Obenauer et al.).
- **License**: ELPV is available for academic and research purposes. All synthetic data used here is open and unencumbered.

## Running Locally

### Backend & ML API
```bash
# Navigate to the project root
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/api/assets` | Retrieve list of all renewable energy assets and current status. |
| `GET` | `/api/assets/{asset_id}` | Retrieve detailed digital twin state for a specific asset. |
| `POST` | `/api/analyze/visual` | Submit asset image for ResNet-18 defect classification. |
| `POST` | `/api/analyze/telemetry` | Submit operational data for Isolation Forest anomaly detection. |
| `GET` | `/api/maintenance/schedule` | Retrieve prioritized list of recommended maintenance actions. |

## Model Results
*Results reported on synthetic demo data. Not representative of production performance. Included to demonstrate pipeline functionality.*

## Limitations
1. **Synthetic Data Dependency**: Current implementation relies on synthetic operational data and mockup predictions; it lacks validation against physical degradation patterns.
2. **Prototype Health Formula**: The Asset Health Index uses heuristic weights rather than empirically derived coefficients.
3. **Model Generalization**: The target CNN model may struggle with varying environmental conditions, lighting variations, or panel types not present in the training set.
4. **Scalability Constraints**: SQLite is utilized for prototype persistence and will not scale to high-frequency telemetry across large solar farms.
5. **Real-time Latency**: Image inference pipeline currently runs synchronously; a production environment would require asynchronous queuing and optimized edge deployment.

## Future Scope
1. **Edge Deployment**: Optimize ML models (e.g., MobileNet or TensorRT) for deployment on edge devices near the physical assets.
2. **Time-Series Forecasting**: Integrate LSTM or Prophet models to forecast degradation trends and predict time-to-failure.
3. **Multimodal Fusion**: Enhance the digital twin by fusing thermal imaging (IR) and RGB drone footage.
4. **Cloud Migration**: Transition the backend from SQLite to a scalable time-series database (e.g., InfluxDB) and managed PostgreSQL.
5. **Digital Twin 3D Visualization**: Develop WebGL-based 3D models for spatial representation of asset locations and defect overlays.
6. **Integration with EAM**: Build robust API connectors to standard Enterprise Asset Management systems (e.g., SAP, IBM Maximo).
7. **Automated Drone Routing**: Use maintenance priority outputs to automatically generate waypoints for drone inspection fleets.

## Industrial Impact
RenewTwin transforms the paradigm of renewable asset management from reactive maintenance to predictive, continuous monitoring. By aggregating visual defect data with operational telemetry into a unified digital twin, operators gain an unprecedented view of asset health at an individual panel level.

This transition enables substantial reductions in maintenance costs by eliminating unnecessary physical inspections and minimizing asset downtime. The targeted deployment of repair resources based on actual degradation rather than scheduled intervals directly improves the Levelized Cost of Energy (LCOE) and maximizes the operational lifespan of the renewable infrastructure.

## Competition
**MC²Plus × Oil India Ltd. × IIT Kharagpur — Energy Innovation Challenge 2026, Track 4: Digital Asset Management**

## Team
[Placeholder]
