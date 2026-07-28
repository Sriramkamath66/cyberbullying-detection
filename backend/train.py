"""
Train Logistic Regression and Random Forest classifiers for cyberbullying detection.
Run this script once before starting the API server.

Usage:
    python train.py
"""

import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    classification_report,
)
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_FULL  = os.path.join(BASE_DIR, "data", "cyberbullying_data_full.csv")
_SMALL = os.path.join(BASE_DIR, "data", "cyberbullying_data.csv")
DATA_PATH  = _FULL if os.path.exists(_FULL) else _SMALL
MODELS_DIR = os.path.join(BASE_DIR, "models")


def train():
    # ── Load dataset ──────────────────────────────────────────────────────────
    print(f"\nUsing dataset: {os.path.basename(DATA_PATH)}")
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {len(df)} samples")
    print(f"\nClass distribution:\n{df['label'].value_counts().to_string()}\n")

    X = df["text"].fillna("")
    y = df["label"]

    # ── Train / test split ────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples : {len(X_train)}")
    print(f"Testing  samples : {len(X_test)}\n")

    # ── TF-IDF vectorisation ──────────────────────────────────────────────────
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    results = {}

    # ── Logistic Regression ───────────────────────────────────────────────────
    print("=" * 55)
    print("Training Logistic Regression ...")
    lr = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    lr.fit(X_train_tfidf, y_train)
    lr_pred = lr.predict(X_test_tfidf)
    lr_acc = accuracy_score(y_test, lr_pred)
    lr_prec = precision_score(y_test, lr_pred, average="weighted", zero_division=0)

    print(f"\nLogistic Regression")
    print(f"  Accuracy  : {lr_acc:.4f} ({lr_acc*100:.2f}%)")
    print(f"  Precision : {lr_prec:.4f} ({lr_prec*100:.2f}%)")
    print(f"\nClassification Report:\n{classification_report(y_test, lr_pred)}")

    results["logistic_regression"] = {
        "name": "Logistic Regression",
        "accuracy": round(lr_acc, 4),
        "precision": round(lr_prec, 4),
    }

    # ── Random Forest ─────────────────────────────────────────────────────────
    print("=" * 55)
    print("Training Random Forest ...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train_tfidf, y_train)
    rf_pred = rf.predict(X_test_tfidf)
    rf_acc = accuracy_score(y_test, rf_pred)
    rf_prec = precision_score(y_test, rf_pred, average="weighted", zero_division=0)

    print(f"\nRandom Forest")
    print(f"  Accuracy  : {rf_acc:.4f} ({rf_acc*100:.2f}%)")
    print(f"  Precision : {rf_prec:.4f} ({rf_prec*100:.2f}%)")
    print(f"\nClassification Report:\n{classification_report(y_test, rf_pred)}")

    results["random_forest"] = {
        "name": "Random Forest",
        "accuracy": round(rf_acc, 4),
        "precision": round(rf_prec, 4),
    }

    # ── Comparison summary ────────────────────────────────────────────────────
    print("=" * 55)
    best = (
        "logistic_regression"
        if lr_acc >= rf_acc
        else "random_forest"
    )
    results["best_model"] = best
    print(f"Best model by accuracy: {results[best]['name']}")
    print(
        f"  LR  accuracy={lr_acc:.4f}  RF  accuracy={rf_acc:.4f}"
    )

    # ── Persist models ────────────────────────────────────────────────────────
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "vectorizer.pkl"))
    joblib.dump(lr, os.path.join(MODELS_DIR, "logistic_regression.pkl"))
    joblib.dump(rf, os.path.join(MODELS_DIR, "random_forest.pkl"))

    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll models saved to: {MODELS_DIR}/")
    print("Training complete!\n")
    return results


if __name__ == "__main__":
    train()
