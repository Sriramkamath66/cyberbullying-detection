from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PredictRequest
from .model import model_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_manager.load()
    yield


app = FastAPI(
    title="Cyberbullying Detection API",
    description="Multi-class text classification using Logistic Regression and Random Forest",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Cyberbullying Detection API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": model_manager.loaded}


@app.post("/predict")
def predict(request: PredictRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    if not model_manager.loaded:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded. Run train.py first.",
        )
    return model_manager.predict(request.text, request.model or "logistic_regression")


@app.get("/metrics")
def get_metrics():
    if not model_manager.metrics:
        raise HTTPException(
            status_code=503,
            detail="Metrics unavailable. Run train.py first.",
        )
    return model_manager.metrics


@app.get("/models")
def list_models():
    return {
        "available": list(model_manager.models.keys()),
        "loaded": model_manager.loaded,
    }
