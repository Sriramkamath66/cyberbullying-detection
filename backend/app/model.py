import joblib
import os
import json
from typing import Dict

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

LABEL_DISPLAY = {
    "not_cyberbullying": "Not Cyberbullying",
    "hate_speech": "Hate Speech",
    "harassment": "Harassment",
    "cyberbullying": "Cyberbullying",
}


class ModelManager:
    def __init__(self):
        self.vectorizer = None
        self.models: Dict = {}
        self.metrics: Dict = {}
        self.loaded = False

    def load(self):
        try:
            self.vectorizer = joblib.load(os.path.join(MODELS_DIR, "vectorizer.pkl"))
            self.models["logistic_regression"] = joblib.load(
                os.path.join(MODELS_DIR, "logistic_regression.pkl")
            )
            self.models["random_forest"] = joblib.load(
                os.path.join(MODELS_DIR, "random_forest.pkl")
            )
            metrics_path = os.path.join(MODELS_DIR, "metrics.json")
            if os.path.exists(metrics_path):
                with open(metrics_path) as f:
                    self.metrics = json.load(f)
            self.loaded = True
            print("Models loaded successfully.")
        except FileNotFoundError:
            print("Models not found — run train.py first.")
            self.loaded = False

    def predict(self, text: str, model_name: str = "logistic_regression") -> Dict:
        if not self.loaded:
            raise RuntimeError("Models not loaded. Run train.py first.")
        if model_name not in self.models:
            model_name = "logistic_regression"

        model = self.models[model_name]
        vec = self.vectorizer.transform([text])
        label = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        classes = model.classes_

        return {
            "text": text,
            "label": label,
            "label_display": LABEL_DISPLAY.get(label, label),
            "confidence": round(float(max(proba)), 4),
            "model_used": model_name,
            "is_cyberbullying": label != "not_cyberbullying",
            "probabilities": {
                cls: round(float(p), 4) for cls, p in zip(classes, proba)
            },
        }


model_manager = ModelManager()
