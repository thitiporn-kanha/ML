# ...existing code...
#!/usr/bin/env python3
"""Simple, readable Logistic Regression script.

Reads CSV from data/, trains a logistic model with basic preprocessing,
saves metrics, plots and the model into results/.
"""
import argparse
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, auc, confusion_matrix,
                             f1_score, precision_score, recall_score,
                             roc_curve, classification_report)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # handle odd column name from example dataset
    if "2urvived" in df.columns and "Survived" not in df.columns:
        df = df.rename(columns={"2urvived": "Survived"})
    return df


def clean(df: pd.DataFrame, target: str):
    # drop constant cols and id-like columns
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found in data columns")
    drop = [c for c in df.columns if df[c].nunique(dropna=False) <= 1 and c != target]
    possible_id = [c for c in df.columns if c.lower().endswith("id")]
    drop += possible_id
    df = df.drop(columns=set(drop), errors="ignore")

    # convert numeric-like strings
    for c in df.columns:
        if df[c].dtype == object:
            try:
                df[c] = pd.to_numeric(df[c])
            except Exception:
                pass

    # fill missing: numeric->median, categorical->mode
    num = df.select_dtypes(include=["number"]).columns.tolist()
    if target in num:
        num.remove(target)
    cat = [c for c in df.columns if c not in num and c != target]
    if num:
        df[num] = df[num].fillna(df[num].median())
    for c in cat:
        df[c] = df[c].fillna(df[c].mode().iloc[0] if not df[c].mode().empty else "_na_")
    return df, num, cat


def build_pipeline(num_cols, cat_cols):
    # OneHotEncoder compatibility across sklearn versions
    try:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)

    pre = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", ohe, cat_cols),
    ], remainder="drop")

    pipe = Pipeline([
        ("pre", pre),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    return pipe


def evaluate_and_save(model, X_test, y_test, out_dir: Path):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model.named_steps["clf"], "predict_proba") else None

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
    }

    out_dir.mkdir(exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(metrics, indent=2))

    # confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.savefig(out_dir / "confusion_matrix.png", bbox_inches="tight")
    plt.close()

    # ROC
    if y_proba is not None:
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        roc_auc = auc(fpr, tpr)
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
        plt.plot([0, 1], [0, 1], linestyle="--")
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.savefig(out_dir / "roc_curve.png", bbox_inches="tight")
        plt.close()
        metrics["roc_auc"] = roc_auc
        (out_dir / "results.json").write_text(json.dumps(metrics, indent=2))


def main():
    p = argparse.ArgumentParser(description="Simple Logistic Regression runner")
    p.add_argument("--data", default="data/train_and_test2.csv")
    p.add_argument("--target", default="Survived")
    p.add_argument("--out", default="results")
    args = p.parse_args()

    df = load_data(args.data)
    df, num_cols, cat_cols = clean(df, args.target)

    X = df.drop(columns=[args.target])
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,
                                                        stratify=y if y.nunique() == 2 else None)

    pipe = build_pipeline(num_cols, cat_cols)
    grid = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1.0, 10.0]}, cv=5, scoring="f1", n_jobs=-1)
    grid.fit(X_train, y_train)
    best = grid.best_estimator_
    # save model
    out_dir = Path(args.out)
    dump(best, out_dir / "model.joblib")
    # save best params and dataset info
    meta = {"best_params": grid.best_params_, "n_train": len(X_train), "n_test": len(X_test)}
    (out_dir / "metadata.json").write_text(json.dumps(meta, indent=2))

    evaluate_and_save(best, X_test, y_test, out_dir)
    print(json.dumps({**meta}, indent=2))


if __name__ == "__main__":
    main()
# ...existing code...