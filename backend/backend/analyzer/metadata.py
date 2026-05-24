import fitz  # PyMuPDF
from datetime import datetime


SUSPICIOUS_SOFTWARE = [
    'photoshop', 'gimp', 'inkscape', 'paint',
    'wps', 'canva', 'pixlr', 'fotor'
]


def run_metadata(file_path):
    try:
        if not file_path.endswith('.pdf'):
            return {
                'score': 0,
                'flags': ['Metadata analysis only available for PDF files'],
                'details': {}
            }

        doc = fitz.open(file_path)
        meta = doc.metadata

        flags = []
        score = 0
        details = {}

        # Extract metadata fields
        creator  = (meta.get('creator')  or '').lower()
        producer = (meta.get('producer') or '').lower()
        author   = (meta.get('author')   or 'Unknown')
        created  = meta.get('creationDate', '')
        modified = meta.get('modDate', '')

        details['author']   = author
        details['creator']  = creator
        details['producer'] = producer
        details['created']  = created
        details['modified'] = modified

        # Check for suspicious software
        for software in SUSPICIOUS_SOFTWARE:
            if software in creator or software in producer:
                flags.append(
                    f'Document created or edited using {software.title()} — '
                    f'not standard banking software'
                )
                score += 40
                break

        # Check if modified after creation
        if created and modified and created != modified:
            flags.append('Document was modified after original creation date')
            score += 30

        # Check for missing metadata
        if not author or author == 'Unknown':
            flags.append('Document author metadata is missing or stripped')
            score += 15

        if not created:
            flags.append('Document creation date is missing')
            score += 15

        score = min(100, score)
        doc.close()

        return {
            'score': score,
            'flags': flags if flags else ['No metadata anomalies detected'],
            'details': details
        }

    except Exception as e:
        return {
            'score': 0,
            'flags': [f'Metadata error: {str(e)}'],
            'details': {}
        }
