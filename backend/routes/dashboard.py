from fastapi import APIRouter
from ..models.schemas import DashboardSummary, MaintenancePriority
from ..services.digital_twin import DigitalTwinEngine
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
engine = DigitalTwinEngine()

@router.get("/summary", response_model=DashboardSummary)
async def get_summary():
    return await engine.get_fleet_summary()

@router.get("/maintenance/priorities", response_model=List[MaintenancePriority])
async def get_priorities():
    return await engine.get_maintenance_priorities()
