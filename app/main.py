from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app import __version__
from app.model import load_model, predict

state: dict[str, object] = {"model": None, "requests": 0, "predictions": 0}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["model"] = load_model()
    yield


app = FastAPI(
    title="API de Sentimiento",
    description="Clasifica texto en español como positivo, negativo o neutral.",
    version=__version__,
    lifespan=lifespan,
)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, examples=["Me encantó el servicio, todo excelente"])


class PredictResponse(BaseModel):
    text: str
    label: str
    confidence: float
    scores: dict[str, float]


@app.get("/")
def root() -> dict[str, object]:
    return {
        "name": "API de Sentimiento",
        "version": __version__,
        "endpoints": ["/predict (POST)", "/health", "/metrics", "/docs"],
    }


@app.get("/health")
def health() -> dict[str, str]:
    status = "ok" if state["model"] is not None else "loading"
    return {"status": status}


@app.get("/metrics")
def metrics() -> dict[str, int]:
    return {
        "requests_total": int(state["requests"]),
        "predictions_total": int(state["predictions"]),
    }


@app.post("/predict", response_model=PredictResponse)
def predict_sentiment(req: PredictRequest) -> PredictResponse:
    state["requests"] = int(state["requests"]) + 1
    result = predict(state["model"], req.text)
    state["predictions"] = int(state["predictions"]) + 1
    return PredictResponse(
        text=req.text,
        label=str(result["label"]),
        confidence=float(result["confidence"]),
        scores=dict(result["scores"]),
    )
