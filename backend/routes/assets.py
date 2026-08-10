from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.schemas import AssetResponse, AssetDigitalTwin
from ..services.digital_twin import DigitalTwinEngine

router = APIRouter(prefix="/assets", tags=["Assets"])
engine = DigitalTwinEngine()

@router.get("", response_model=List[AssetResponse])
async def list_assets(risk_level: Optional[str] = None, limit: int = 100):
    return await engine.get_assets(risk_level, limit)

@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str):
    asset = await engine.get_twin(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.get("/{asset_id}/digital-twin", response_model=AssetDigitalTwin)
async def get_digital_twin(asset_id: str):
    asset = await engine.get_twin(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset
