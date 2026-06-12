"""Modelo de sentimiento: TF-IDF + regresión logística (scikit-learn)."""

from __future__ import annotations

import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "train.csv"
MODEL_PATH = ROOT / "artifacts" / "model.joblib"

# Si la probabilidad de la mejor clase no supera este margen, lo damos por neutral.
NEUTRAL_BAND = 0.60


def load_dataset(path: Path = DATA_PATH) -> tuple[list[str], list[str]]:
    texts: list[str] = []
    labels: list[str] = []
    with path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000, C=4.0)),
        ]
    )


def train(save: bool = True) -> Pipeline:
    texts, labels = load_dataset()
    pipeline = build_pipeline()
    pipeline.fit(texts, labels)
    if save:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)
    return pipeline


def load_model() -> Pipeline:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return train(save=True)


def predict(pipeline: Pipeline, text: str) -> dict[str, object]:
    proba = pipeline.predict_proba([text])[0]
    classes = list(pipeline.named_steps["clf"].classes_)
    best_idx = int(proba.argmax())
    confidence = float(proba[best_idx])
    label = classes[best_idx]
    if confidence < NEUTRAL_BAND:
        label = "neutral"
    return {
        "label": label,
        "confidence": round(confidence, 4),
        "scores": {cls: round(float(p), 4) for cls, p in zip(classes, proba, strict=True)},
    }
