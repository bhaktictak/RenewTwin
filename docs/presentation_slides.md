# RenewTwin Presentation Slides Overview (12 Slides)

## Slide 1: Title
**Title:** RENEWTWIN — AI-Powered Digital Twin for Predictive Management of Renewable Energy Assets  
**Subtitle:** Energy Innovation Challenge 2026 | Track 4: Digital Asset Management  
**Organizers:** MC²Plus × Oil India Ltd. × IIT Kharagpur  

---

## Slide 2: Problem Statement
- **Massive Scale:** Renewable plants span thousands of acres with 50,000+ PV modules where manual physical inspections are slow, expensive, and logistically unfeasible.
- **Silent Degradation:** Surface defects, micro-cracks, and hot-spots develop unnoticed between annual maintenance cycles.
- **Cost of Delay:** Delayed defect discovery leads to continuous avoidable power loss and elevated risk of permanent hardware failure.

---

## Slide 3: Why Existing Approaches Fall Short
- **Traditional SCADA:** Monitors aggregate plant-level output, unable to isolate individual panel-level defects.
- **Periodic Drone Surveys:** Carried out 1-2 times per year, generating static images without live telemetry linkage.
- **Isolated ML Classifiers:** Perform single-image classification without persistent digital state or economic maintenance prioritization.

---

## Slide 4: RenewTwin Solution
- **Conceptual Shift:** Moving from *Periodic Inspection -> Fault -> Energy Loss* to *Continuous Telemetry -> Digital Twin State Persistence -> Asset Health Index -> Automated Priority Dispatch*.
- **Core Platform:** Asset Registry, ResNet-18 Defect Detector, Isolation Forest Anomaly Engine, Digital Twin State Manager, and Maintenance Priority Dispatcher.

---

## Slide 5: System Architecture
- **Data Acquisition:** Ingestion of visual imagery and operational telemetry (Power, Temp, Irradiance).
- **AI Analysis:** Parallel processing via ResNet-18 (Visual Defect Classifier) and Isolation Forest (Telemetry Anomaly Detector).
- **Digital Twin Engine:** Central persistent state model mapping physical asset state to digital identity.
- **Health Engine & Dashboard:** Prototype Asset Health Index computation powering real-time React Industrial Operator UI.

---

## Slide 6: AI/ML Methodology
- **Visual Defect Classifier:** Transfer learning using ResNet-18 architecture targeting 4 classes: Clean (None), Micro-crack, Hotspot, Inactive/Cell Damage.
- **Telemetry Anomaly Detector:** Unsupervised Isolation Forest evaluating power ratio deviation, temperature elevation, and recency.
- **Model Efficiency:** Balanced computational speed and accuracy suitable for edge/cloud hybrid execution.

---

## Slide 7: Digital Twin Schema
- **Object Model:** Every physical panel has a synchronized JSON Digital Twin state.
- **Parameters:** `asset_id`, `location`, `rated_capacity_kw`, `current_power_kw`, `expected_power_kw`, `temperature_c`, `defect_class`, `defect_probability`, `anomaly_score`, `health_score`, `risk_level`, `maintenance_priority`, `recommended_action`.

---

## Slide 8: Asset Health Index (AHI) & Risk Classification
- **AHI Formula:** $100 - (Defect\_Penalty \times 0.4) - (Anomaly\_Penalty \times 0.3) - (Performance\_Deviation \times 0.2) - (Temperature\_Penalty \times 0.1)$
- **Risk Tiers:**
  - **HEALTHY (90–100):** Normal operations.
  - **MONITOR (75–89):** Minor efficiency drift; routine check.
  - **AT RISK (50–74):** Thermal / structural anomaly detected; prioritize inspection.
  - **CRITICAL (<50):** Severe failure imminent; dispatch field technician immediately.

---

## Slide 9: Maintenance Prioritization Engine
- **Impact-Driven Ranking:** Ranks maintenance tasks based on failure severity and energy loss percentage.
- **Technician Dispatch:** Replaces static inspection schedules with an automated work queue (#1 PV-A-014: Hotspot, 46.9% loss estimated).

---

## Slide 10: Product Demonstration & MVP Implementation
- **Full Stack Architecture:** FastAPI REST API backend + SQLite persistent DB + React/Vite industrial dashboard.
- **Live Fleet Tracking:** Monitors 24 active solar PV assets with interactive digital twin drill-downs and real-time inference upload.

---

## Slide 11: Future Roadmap & Technical Scalability
- **Multi-Asset Support:** Extending digital twin models to Wind Turbines and Battery Energy Storage Systems (BESS).
- **Enterprise Integration:** Migrating to InfluxDB time-series database and connecting to SAP / IBM Maximo EAM systems.
- **Edge AI:** Deploying TensorRT/ONNX models directly on inspection drone hardware.

---

## Slide 12: Industrial Impact & Conclusion
- **Shift to Predictive O&M:** Substantial reduction in unplanned downtime and Levelized Cost of Energy (LCOE).
- **Deliverable Prototype:** Complete working backend, frontend, ML pipeline, and documentation repository.
- **GitHub Repository:** https://github.com/bhaktictak/RenewTwin
