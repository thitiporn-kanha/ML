#!/usr/bin/env python3
"""KMeans clustering template

Simple KMeans example; saves cluster labels and inertia.
"""
import json
from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.cluster import KMeans


def main(data_file='data/data.csv', out_dir='results', n_clusters=3):
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    df = pd.read_csv(data_file)
    X = df.select_dtypes(include='number')
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(X)
    df['cluster'] = labels
    metrics = {'inertia': float(km.inertia_)}
    (out / 'results.json').write_text(json.dumps(metrics, indent=2))
    df.to_csv(out / 'with_clusters.csv', index=False)
    dump(km, out / 'model.joblib')
    print('Saved results to', out)


if __name__ == '__main__':
    main()
