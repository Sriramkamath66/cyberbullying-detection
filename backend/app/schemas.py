from pydantic import BaseModel
from typing import Optional

class PredictRequest(BaseModel):
    text: str
    model: Optional[str] = "logistic_regression"

class PredictResponse(BaseModel):
    text: str
    label: str
    label_display: str
    confidence: float
    model_used: str
    is_cyberbullying: bool
    probabilities: dict

class ModelMetrics(BaseModel):
    name: str
    accuracy: float
    precision: float

class MetricsResponse(BaseModel):
    logistic_regression: dict
    random_forest: dict
    best_model: str
