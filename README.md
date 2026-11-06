# BharatDoc AI — Indian Document Understanding Tool

A lightweight Streamlit prototype for uploading Indian-language notices, forms and government documents, extracting text, identifying common fields, generating a short summary and answering simple questions from the document.

## Important project status

This is a **working prototype**, not a completed integration of BharatGen Patram and IndicTrans2.

- **Implemented:** Streamlit upload UI, text-based PDF extraction, image/scanned-PDF OCR path, basic field extraction, extractive summary, evidence-sentence question answering, text download.
- **Integration pending:** BharatGen Patram model inference and AI4Bharat IndicTrans2 translation.
- **Limitations:** Regex-based field extraction and keyword-based Q&A are baseline methods. Indic OCR depends on installed Tesseract language packs. Always verify extracted values against the original document.

BharatGen's model guidance indicates Patram requires substantial GPU memory (around 24 GB). Do not spend the two-hour build window attempting a local Patram setup unless suitable GPU access and model access are already available.

## 1. Run locally

Use Python 3.10 or 3.11 if available.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install packages:
```bash
pip install -r requirements.txt
```

Run:
```bash
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## 2. OCR requirement

For image files and scanned PDFs, install the **Tesseract OCR executable** separately. The Python package `pytesseract` is only a wrapper.

For Indic-language OCR, install the corresponding Tesseract trained language data and configure Tesseract if it is not on PATH. If Tesseract is unavailable, text-based PDFs can still be processed.

## 3. Model responsibilities

| Component | Responsibility | Status |
|---|---|---|
| BharatGen Patram | Vision-language document understanding and structured interpretation | Planned integration |
| Tesseract / PyMuPDF | Baseline OCR and PDF text extraction | Implemented |
| AI4Bharat IndicTrans2 | Translate between supported Indian languages and English | Planned integration |
| Rule-based extraction | Detect dates, phone numbers, emails and reference numbers | Implemented baseline |
| Extractive QA | Select a relevant evidence sentence from the document | Implemented baseline |

IndicTrans2 supports 22 scheduled Indic languages. Official setup and inference instructions:
https://github.com/AI4Bharat/IndicTrans2

BharatGen model information:
https://bharatgen.com/models/

## 4. Suggested two-hour build sequence

1. 0–15 min: create venv, install dependencies, run Streamlit.
2. 15–35 min: test with a text-based PDF.
3. 35–55 min: test image OCR; install Tesseract only if already feasible.
4. 55–75 min: test fields, summary and question answering; fix obvious issues.
5. 75–95 min: prepare 30–50 test cases and record correct/incorrect outputs.
6. 95–120 min: capture screenshots, update README, prepare demo explanation.

## 5. Test plan

See `tests/test_cases.csv`. Use real or publicly available sample documents for final evaluation, and manually record the ground-truth values. The included test rows are test scenarios, not measured model results.

## 6. Demo flow

1. Upload a sample government notice or form.
2. Show extracted text.
3. Show detected dates, phone numbers, email and reference number.
4. Show the summary.
5. Ask: "What is the last date for submission?"
6. Show the answer and its supporting sentence.
7. Download extracted text.

## 7. Failure analysis to report

- Blurry or skewed scans can cause OCR errors.
- Tables, stamps, handwriting and multi-column layouts may be read incorrectly.
- Date formats can be ambiguous.
- Regex extraction may miss names and addresses or extract irrelevant numbers.
- Keyword-based QA can select a related but incorrect sentence.
- Translation may change legal or administrative meaning; verify critical content.
- The current build does not claim Patram or IndicTrans2 inference until those models are connected.

## 8. Repository structure

```text
indian_document_understanding_tool/
├── app.py
├── app/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── analysis.py
│   └── translation.py
├── tests/
│   └── test_cases.csv
├── sample_docs/
├── requirements.txt
└── README.md
```
