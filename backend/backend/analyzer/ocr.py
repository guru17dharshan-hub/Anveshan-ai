import easyocr
import re
from pdf2image import convert_from_path
from PIL import Image
import numpy as np


reader = easyocr.Reader(['en', 'ta', 'hi'], gpu=False)


def run_ocr(file_path):
    try:
        # Convert PDF to image if needed
        if file_path.endswith('.pdf'):
            pages = convert_from_path(file_path, first_page=1, last_page=1)
            img = np.array(pages[0])
        else:
            img = np.array(Image.open(file_path).convert('RGB'))

        results = reader.readtext(img)
        texts = [r[1] for r in results]
        confidences = [r[2] for r in results]
        full_text = ' '.join(texts)

        flags = []
        score = 0

        # Check for low confidence OCR regions
        low_conf = [c for c in confidences if c < 0.5]
        if len(low_conf) > len(confidences) * 0.3:
            flags.append('More than 30% of text regions have low OCR confidence')
            score += 30

        # Check for suspicious number patterns
        numbers = re.findall(r'\b\d{4,}\b', full_text)
        if len(numbers) > 20:
            flags.append('Unusually high number of numeric fields detected')
            score += 20

        # Check for date inconsistencies
        dates = re.findall(
            r'\b(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\b',
            full_text
        )
        if len(dates) > 5:
            flags.append('Multiple date fields found — cross-check recommended')
            score += 15

        # Check for copy-paste repeated phrases
        words = full_text.lower().split()
        unique_ratio = len(set(words)) / max(len(words), 1)
        if unique_ratio < 0.4:
            flags.append('Low text uniqueness ratio — possible copy-paste content')
            score += 25

        score = min(100, score)

        return {
            'score': score,
            'text_extracted': full_text[:500],
            'total_regions': len(results),
            'low_confidence_regions': len(low_conf),
            'flags': flags if flags else ['No text anomalies detected']
        }

    except Exception as e:
        return {
            'score': 0,
            'text_extracted': '',
            'total_regions': 0,
            'low_confidence_regions': 0,
            'flags': [f'OCR error: {str(e)}']
        }
