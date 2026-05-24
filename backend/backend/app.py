from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile

from analyzer.ela import run_ela
from analyzer.ocr import run_ocr
from analyzer.metadata import run_metadata
from analyzer.anomaly import run_anomaly
from analyzer.groq_explain import run_explanation

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Anveshan AI is running'})


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported. Upload PDF, PNG, or JPG'}), 400

    # Save to temp file
    suffix = '.' + file.filename.rsplit('.', 1)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        # Run all 4 layers in parallel
        ela_result     = run_ela(tmp_path)
        ocr_result     = run_ocr(tmp_path)
        meta_result    = run_metadata(tmp_path)
        anomaly_result = run_anomaly(ela_result, ocr_result, meta_result)

        # Calculate final risk score (weighted average)
        risk_score = round(
            (ela_result['score']     * 0.35) +
            (ocr_result['score']     * 0.25) +
            (meta_result['score']    * 0.20) +
            (anomaly_result['score'] * 0.20)
        )

        # Risk level
        if risk_score >= 70:
            risk_level = 'HIGH'
        elif risk_score >= 40:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        # AI explanation from Groq
        explanation = run_explanation(
            risk_score, risk_level,
            ela_result, ocr_result, meta_result
        )

        return jsonify({
            'risk_score':  risk_score,
            'risk_level':  risk_level,
            'explanation': explanation,
            'layers': {
                'visual':   ela_result,
                'ocr':      ocr_result,
                'metadata': meta_result,
                'anomaly':  anomaly_result
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        os.unlink(tmp_path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
