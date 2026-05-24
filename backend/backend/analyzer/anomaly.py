import numpy as np
from sklearn.ensemble import IsolationForest


def run_anomaly(ela_result, ocr_result, meta_result):
    try:
        # Build feature vector from all layer scores
        features = np.array([[
            ela_result.get('score', 0),
            ela_result.get('mean_diff', 0),
            ela_result.get('max_diff', 0),
            ocr_result.get('score', 0),
            ocr_result.get('low_confidence_regions', 0),
            meta_result.get('score', 0),
            len(ela_result.get('flags', [])),
            len(ocr_result.get('flags', [])),
            len(meta_result.get('flags', []))
        ]])

        # Isolation Forest — trained on synthetic normal documents
        normal_docs = np.random.normal(loc=10, scale=5, size=(100, 9))
        normal_docs = np.clip(normal_docs, 0, 100)

        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(normal_docs)

        prediction = model.predict(features)
        raw_score  = model.decision_function(features)[0]

        # Convert to 0-100 anomaly score
        anomaly_score = max(0, min(100, round((1 - raw_score) * 50)))

        flags = []
        if prediction[0] == -1:
            flags.append('Document pattern is statistically abnormal compared to genuine documents')
        if anomaly_score > 70:
            flags.append('High combined anomaly score — multiple suspicious signals detected')
        if anomaly_score > 40:
            flags.append('Moderate anomaly detected — manual review recommended')

        return {
            'score': anomaly_score,
            'is_anomaly': bool(prediction[0] == -1),
            'flags': flags if flags else ['Document pattern within normal range']
        }

    except Exception as e:
        return {
            'score': 0,
            'is_anomaly': False,
            'flags': [f'Anomaly detection error: {str(e)}']
        }
