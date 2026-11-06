# BharatDoc AI — Indian Document Understanding Tool

A lightweight Streamlit application for uploading Indian-language notices, forms and government documents, extracting text, identifying important fields, generating summaries and answering questions using document evidence.

## 1. Project Overview

BharatDoc AI aims to make Indian government documents easier to understand by allowing users to upload documents, extract information and ask questions in a simple interface.

### Key Features

- Upload PDF and image documents.
- Extract text from text-based and scanned PDFs.
- Perform OCR on image-based documents.
- Extract dates, phone numbers, email addresses and reference numbers.
- Generate short document summaries.
- Answer questions using extracted document text.
- Display supporting evidence for answers.
- Download extracted text.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | User interface |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | Scanned document and image text extraction |
| Pillow | Image processing |
| Regular Expressions | Basic information extraction |
| Rule-based QA | Evidence-based question answering |

## 3. Model Integration Status

The project is designed around the following models:

- **BharatGen Patram:** Planned integration for vision-language document understanding.
- **AI4Bharat IndicTrans2:** Planned integration for Indian-language translation.

**Important:** The current prototype uses Tesseract, PyMuPDF and rule-based processing. Patram and IndicTrans2 inference have not yet been integrated.

## 4. Installation and Setup

### Requirements

- Python 3.10 or 3.11
- Git
- Tesseract OCR for scanned documents and image OCR

### Clone the repository

```bash
git clone https://github.com/poornavm/BharatDoc-AI.git
cd BharatDoc-AI
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate it on Windows

```powershell
venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

## 5. Application Workflow

1. Upload an Indian-language document.
2. Extract text using PDF processing or OCR.
3. Identify important fields such as dates, phone numbers and reference numbers.
4. Generate a short summary.
5. Enter questions about the uploaded document.
6. Retrieve answers with supporting evidence.
7. Download the extracted text.

## 6. Project Structure

```text
indian_document_understanding_tool/
│
├── app.py
├── app/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── analysis.py
│   └── translation.py
│
├── tests/
│   └── test_cases.csv
│
├── sample_docs/
│   └── sample_notice.txt
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 7. Testing and Evaluation

The project includes test scenarios in `tests/test_cases.csv`.

Evaluation focuses on:

- Text extraction accuracy
- Field extraction accuracy
- Question-answering accuracy
- Evidence retrieval
- Handling of missing information

The current test cases are scenarios, not measured accuracy results. Actual performance must be evaluated using manually verified answers.

## 8. Current Limitations

- OCR accuracy depends on document quality and installed language data.
- Tables, handwriting and complex layouts may produce extraction errors.
- Regex-based extraction may miss or incorrectly identify fields.
- Rule-based question answering may retrieve an unrelated sentence.
- Translation functionality is not yet connected to IndicTrans2.
- Patram inference is not yet integrated.

Important extracted information should always be verified against the original document.

## 9. Future Enhancements

- Integrate BharatGen Patram for multimodal document understanding.
- Integrate AI4Bharat IndicTrans2 for multilingual translation.
- Improve extraction of tables and structured layouts.
- Add stronger semantic question answering.
- Expand evaluation across multiple Indian languages and document types.

## 10. References

- BharatGen: https://bharatgen.com/models/
- AI4Bharat IndicTrans2: https://github.com/AI4Bharat/IndicTrans2
- Streamlit: https://streamlit.io/
- PyMuPDF: https://pymupdf.readthedocs.io/
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract