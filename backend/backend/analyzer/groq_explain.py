import os
from groq import Groq


client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def run_explanation(risk_score, risk_level, ela, ocr, meta):
    try:
        all_flags = (
            ela.get('flags', []) +
            ocr.get('flags', []) +
            meta.get('flags', [])
        )
        flags_text = '\n'.join(f'- {f}' for f in all_flags)

        prompt = f"""
You are Anveshan AI, a document fraud detection assistant for Indian banking.

A document was analyzed and produced the following results:
- Overall Risk Score: {risk_score}/100
- Risk Level: {risk_level}

Detected signals:
{flags_text}

Write a short, professional, banker-friendly explanation (4-5 sentences) of:
1. Whether this document is likely genuine or forged
2. The specific reasons why it is suspicious
3. What action the underwriter should take

Be direct and specific. Do not use bullet points. Write in plain English.
        """

        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return (
            f'Risk Score: {risk_score}/100 — {risk_level} RISK. '
            f'Detected flags: {", ".join(all_flags[:3])}. '
            f'Manual review by compliance team is recommended.'
        )
