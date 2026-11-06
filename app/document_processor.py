
from io import BytesIO


def extract_document_text(file_bytes: bytes, filename: str) -> dict:
    ext = filename.lower().rsplit(".", 1)[-1]

    # PDF processing
    if ext == "pdf":
        try:
            import fitz

            doc = fitz.open(stream=file_bytes, filetype="pdf")

            # First, extract embedded PDF text.
            pages = [page.get_text("text") for page in doc]
            text = "\n".join(pages).strip()

            # Check whether Kannada Unicode characters are present.
            kannada_chars = sum(
                1 for char in text
                if "\u0C80" <= char <= "\u0CFF"
            )

            # Use embedded text if Kannada is readable,
            # or if the document contains ordinary English text.
            if text:
                if kannada_chars > 0:
                    return {
                        "text": text,
                        "method": "PyMuPDF (embedded PDF text)",
                        "warning": ""
                    }

                # For PDFs without Kannada Unicode, use OCR
                # to handle potentially corrupted Kannada text.
                # English PDFs will also go through OCR here.

            # OCR fallback for scanned or corrupted PDFs.
            try:
                import pytesseract
                from PIL import Image

                pytesseract.pytesseract.tesseract_cmd = (
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                )

                ocr_pages = []

                for page in doc:
                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2)
                    )

                    image = Image.open(
                        BytesIO(pix.tobytes("png"))
                    )

                    ocr_text = pytesseract.image_to_string(
                        image,
                        lang="kan+eng"
                    )

                    ocr_pages.append(ocr_text)

                final_text = "\n".join(ocr_pages).strip()

                return {
                    "text": final_text,
                    "method": "Tesseract Kannada + English OCR",
                    "warning": (
                        "OCR was used because embedded text was "
                        "unavailable or did not contain Kannada Unicode. "
                        "Accuracy depends on document quality."
                    )
                }

            except Exception as exc:
                return {
                    "text": text,
                    "method": "PDF extraction (OCR unavailable)",
                    "warning": (
                        f"OCR could not run. Details: {exc}"
                    )
                }

        except Exception as exc:
            return {
                "text": "",
                "method": "PDF extraction failed",
                "warning": str(exc)
            }

    # Image processing
    else:
        try:
            import pytesseract
            from PIL import Image

            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )

            image = Image.open(BytesIO(file_bytes))

            text = pytesseract.image_to_string(
                image,
                lang="kan+eng"
            )

            return {
                "text": text.strip(),
                "method": "Tesseract Kannada + English OCR",
                "warning": ""
            }

        except Exception as exc:
            return {
                "text": "",
                "method": "Image OCR unavailable",
                "warning": f"OCR error: {exc}"
            }
