from fastapi import APIRouter, UploadFile, File
from ..models.schemas import PredictionResponse
import hashlib
import random

router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("", response_model=PredictionResponse)
async def predict(image: UploadFile = File(...)):
    filename = image.filename or "unknown"
    seed = int(hashlib.md5(filename.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)
    
    classes = ['none', 'hotspot', 'crack', 'soiling', 'shading', 'cell_damage']
    defect_class = random.choice(classes)
    confidence = random.uniform(0.6, 0.99)
    
    probabilities = {c: (confidence if c == defect_class else random.uniform(0, 1 - confidence)/len(classes)) for c in classes}
    
    return PredictionResponse(
        defect_class=defect_class,
        probabilities=probabilities,
        confidence=confidence
    )
