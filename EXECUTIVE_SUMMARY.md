# RenewTwin — Executive Summary / Abstract

**Project Name:** RenewTwin  
**Track:** Track 4 — Digital Asset Management (AI/ML, Digital Twins, Robotics, Corrosion)  
**Competition:** MC²Plus × Oil India Ltd. × IIT Kharagpur — Energy Innovation Challenge 2026  

---

### Abstract (Submission Ready)

RenewTwin is an AI-driven digital asset management platform designed for continuous health monitoring, failure prediction, and maintenance prioritization across renewable energy infrastructure, with an initial prototype focused on solar photovoltaic (PV) assets. Modern utility-scale renewable plants consist of thousands of distributed assets where traditional periodic manual inspections lead to delayed fault detection, increased maintenance costs, and avoidable energy loss. 

RenewTwin addresses this operational challenge by establishing an intelligent **Digital Twin** for every physical asset. The platform ingests multimodal operational signals—combining computer vision-based visual defect detection (utilizing deep transfer learning via ResNet-18) with operational anomaly analysis (powered by Isolation Forest models on telemetry data). These signals feed into a dynamic Digital Twin Engine that contextualizes real-time performance against historical baselines.

Using a transparent **Prototype Asset Health Index (AHI)**, RenewTwin dynamically evaluates asset health by integrating visual defect severity (40%), operational anomaly scores (30%), performance deviation (20%), and thermal elevation penalties (10%). Assets are automatically classified into four actionable operational risk categories: *Healthy*, *Monitor*, *At Risk*, and *Critical*. The platform features an automated **Maintenance Recommendation Engine** that ranks maintenance tasks based on failure severity and energy loss impact, ensuring operators dispatch field technicians to highest-priority faults before major catastrophic failure or energy loss occurs.

The RenewTwin prototype features a production-grade FastAPI backend, an SQLite digital twin registry, an ML inference engine, and a dark-themed industrial monitoring dashboard built with React and Vite. By shifting operations from reactive periodic inspection to proactive, AI-assisted digital twin management, RenewTwin enables renewable energy operators to lower Levelized Cost of Energy (LCOE), reduce unplanned downtime, and maximize asset lifespan.

*Note: The current prototype demonstrates full pipeline functionality, backend APIs, ML inference scripts, and dashboard interfaces using synthetic demo data labeled as SYNTHETIC_DEMO.*
