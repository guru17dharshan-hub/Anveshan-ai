from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import tempfile
import os
from pdf2image import convert_from_path


def run_ela(file_path, quality=90):
    try:
        # Convert PDF to image if needed
        if file_path.endswith('.pdf'):
            pages = convert_from_path(file_path, first_page=1, last_page=1)
            img = pages[0]
        else:
            img = Image.open(file_path).convert('RGB')

        # Save at reduced quality and compare
        tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(tmp.name, 'JPEG', quality=quality)
        compressed = Image.open(tmp.name)

        # Get difference
        diff = ImageChops.difference(img, compressed)
        enhancer = ImageEnhance.Brightness(diff)
        diff_enhanced = enhancer.enhance(10)

        # Calculate anomaly score from pixel differences
        diff_array = np.array(diff).astype(float)
        mean_diff = diff_array.mean()
        max_diff = diff_array.max()

        # Score 0-100
        score = min(100, round((mean_diff / 10) * 100))

        flags = []
        if mean_diff > 5:
            flags.append('High pixel inconsistency detected across document')
        if max_diff > 50:
            flags.append('Extreme pixel anomaly found — possible spliced region')
        if mean_diff > 2:
            flags.append('Minor editing artifacts present')

        os.unlink(tmp.name)

        return {
            'score': score,
            'mean_diff': round(mean_diff, 4),
            'max_diff': round(float(max_diff), 4),
            'flags': flags if flags else ['No visual anomalies detected']
        }

    except Exception as e:
        return {'score': 0, 'mean_diff': 0, 'max_diff': 0, 'flags': [f'ELA error: {str(e)}']}
