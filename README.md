# Anveshan-ai
Anveshan AI — Real-time document forgery and anomaly detection for Indian banking underwriting | SuRaksha Cyber Hackathon 2.0 | Canara Bank
# Anveshan AI (अन्वेषण)
### Real-Time Document Forgery & Anomaly Detection for Banking Underwriting

> "Because every forged document leaves a trace. We find it."

Built for SuRaksha Cyber Hackathon 2.0 by Canara Bank.

---

## The Problem

Indian banks lose thousands of crores every year to document fraud during loan underwriting. Fraudsters use photo editing tools, PDF manipulators, and AI generators to alter land area figures, inflate income, forge government stamps, and create entirely fake documents. Manual verification by bank officers is slow, error-prone, and increasingly ineffective against sophisticated digital forgeries.

---

## Our Solution — 4 Detection Layers

| Layer | Technology | What It Detects |
|-------|-----------|-----------------|
| Visual Forensics | PIL + OpenCV (ELA) | Pixel-level tampering, edited regions |
| OCR Intelligence | EasyOCR + NLP | Font mismatches, logical inconsistencies |
| Metadata Forensics | PyMuPDF | Edit history, software fingerprints |
| Anomaly Scoring | Isolation Forest (sklearn) | Statistical anomalies across all signals |

All four layers run in parallel. Full risk report delivered in under 2 seconds.

---

## AI Explanation Engine

All detected signals are passed to Groq API (LLaMA 3.3 70B — free tier) which generates a plain-English, banker-friendly explanation — not just THAT a document is suspicious, but exactly WHY, with field-level evidence.

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend | React.js, TailwindCSS, Chart.js |
| Backend | Python 3.11, Flask |
| OCR | EasyOCR (English, Tamil, Hindi) |
| Vision | PIL + OpenCV |
| PDF | PyMuPDF (fitz) |
| ML | scikit-learn Isolation Forest |
| AI | Groq API — LLaMA 3.3 70B (free) |
| Fallback | Ollama — LLaMA 3.2 (offline) |

---

## Folder Structure
