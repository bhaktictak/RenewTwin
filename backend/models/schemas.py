from pydantic import BaseModel, ConfigDict
from typing import Dict, List

class AssetBase(BaseModel):
    asset_id: str
    asset_type: str
    location: str
    rated_capacity_kw: float
    installation_date: str
    current_power_kw: float
    expected_power_kw: float
    temperature_c: float
    defect_class: str
    defect_probability: float
    anomaly_score: float
    health_score: float
    risk_level: str
    maintenance_priority: int
    last_inspection: str
    recommended_action: str
    status: str
    created_at: str
    updated_at: str

class AssetResponse(AssetBase):
    data_source: str = 'SYNTHETIC_DEMO'
    model_config = ConfigDict(from_attributes=True)

class AssetDigitalTwin(AssetResponse):
    pass

class DashboardSummary(BaseModel):
    total_assets: int
    healthy_count: int
    monitor_count: int
    at_risk_count: int
    critical_count: int
    avg_health_score: float
    maintenance_pending: int
    data_source: str = 'SYNTHETIC_DEMO'

class PredictionResponse(BaseModel):
    defect_class: str
    probabilities: Dict[str, float]
    confidence: float
    data_source: str = 'DEMO_INFERENCE'

class MaintenancePriority(BaseModel):
    asset_id: str
    priority: int
    risk_level: str
    health_score: float
    recommended_action: str
    estimated_loss_pct: float
    data_source: str = 'SYNTHETIC_DEMO'
