#!/usr/bin/env python3
"""Neural Network (MLP) template

Simple MLPClassifier example using scikit-learn.
"""
import json
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def main(data_file='data/data.csv', target='target', out_dir='results'):
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    df = pd.read_csv(data_file)
    if target not in df.columns:
        raise SystemExit(f"Target column '{target}' not found")
    X = df.drop(columns=[target])
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'report': classification_report(y_test, y_pred, output_dict=True)
    }
    (out / 'results.json').write_text(json.dumps(metrics, indent=2))
    dump(clf, out / 'model.joblib')
    print('Saved results to', out)


if __name__ == '__main__':
    main()
