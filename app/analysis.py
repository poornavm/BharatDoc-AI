
import re


DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",
]


def extract_fields(text: str) -> dict:
    dates = []

    for pattern in DATE_PATTERNS:
        dates.extend(re.findall(pattern, text, flags=re.I))

    phones = re.findall(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        text
    )

    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    refs = re.findall(
        r"\b[A-Z]{2,}[-/][A-Z0-9/-]{4,}\b",
        text,
        flags=re.I
    )

    return {
        "dates_found": list(dict.fromkeys(dates)),
        "phone_numbers": list(dict.fromkeys(phones)),
        "email_addresses": list(dict.fromkeys(emails)),
        "reference_numbers": list(dict.fromkeys(refs)),
        "note": (
            "Prototype extraction uses patterns. Names, addresses and "
            "domain-specific fields need a trained model or validation."
        )
    }


def _sentences(text):
    return [
        s.strip()
        for s in re.split(r"(?<=[.!?।])\s+|\n+", text)
        if len(s.strip()) > 10
    ]


def summarize_text(text: str, max_sentences: int = 3) -> str:
    sentences = _sentences(text)

    if not sentences:
        return text[:500] if text else "No text available."

    keywords = (
        "date", "submit", "submission", "deadline",
        "required", "amount", "ಕರ್ನಾಟಕ", "ಅರ್ಜಿ",
        "last date", "ನೋಟಿಸ್", "ವಿಷಯ",
        "ಶೈಕ್ಷಣಿಕ", "ಪ್ರವಾಸ", "ದಿನಾಂಕ",
        "ಪೋಷಕರ", "ಒಪ್ಪಿಗೆ"
    )

    ranked = sorted(
        enumerate(sentences),
        key=lambda x: (
            sum(k in x[1].lower() for k in keywords),
            -x[0]
        ),
        reverse=True
    )

    chosen = sorted(
        [i for i, _ in ranked[:max_sentences]]
    )

    return " ".join(sentences[i] for i in chosen)


def answer_question(text: str, question: str):

    if not text.strip():
        return "No readable text found in the document.", ""

    sentences = _sentences(text)
    q = question.lower().strip()

    # Normalise whitespace without changing the original evidence.
    normalized_text = re.sub(r"\s+", " ", text)

    def find_sentence(keywords):
        for sentence in sentences:
            if any(word in sentence.lower() for word in keywords):
                return sentence, sentence
        return None

    # --------------------------------------------------
    # 1. PARENTAL CONSENT QUESTIONS
    # --------------------------------------------------

    consent_words = [
        "parent", "parents", "consent",
        "ಪೋಷಕರ", "ಪೋಪಕರ", "ಒಪ್ಪಿಗೆ",
        "ಯಾರ ಒಪ್ಪಿಗೆ", "ಅಗತ್ಯ",
        "ಶೈಕ್ಷಣಿಕ ಪ್ರವಾಸಕ್ಕೆ ಹೋಗಲು",
        "ಪ್ರವಾಸಕ್ಕೆ ಹೋಗಲು"
    ]

    if any(word in q for word in consent_words):

        # Search for the actual rule in the document.
        # Allow OCR variations in the parent-related word.
        consent_pattern = (
            r"(?:ಪೋಷಕರ|ಪೋಪಕರ)"
            r"\s*ಒಪ್ಪಿಗೆ"
            r"\s*ಪಡೆದ"
            r"\s*ವಿದ್ಯಾರ್ಥಿಗಳನ್ನು"
            r"\s*ಮಾತ್ರ"
            r"\s*ಶೈಕ್ಷಣಿಕ\s*ಪ್ರವಾಸಕ್ಕೆ"
            r"\s*ಕರೆದೊಯ್ಯ(?:ುವುದು|ಬೇಕು)"
        )

        match = re.search(
            consent_pattern,
            normalized_text
        )

        if match:
            answer = match.group(0).strip()
            return answer, answer

        # More flexible fallback if OCR has damaged part
        # of the sentence.
        position = normalized_text.find("ಒಪ್ಪಿಗೆ")

        if position != -1:
            start = max(0, position - 50)
            end = min(len(normalized_text), position + 180)

            answer = normalized_text[start:end].strip()
            return answer, answer

        return (
            "Parental consent information could not be reliably extracted.",
            ""
        )

    # --------------------------------------------------
    # 2. REFERENCE NUMBER QUESTIONS
    # --------------------------------------------------

    reference_words = [
        "reference", "reference number", "ref no",
        "ಉಲ್ಲೇಖ ಸಂಖ್ಯೆ", "ನೋಂದಣಿ ಸಂಖ್ಯೆ",
        "ಸುತ್ತೋಲೆ ಸಂಖ್ಯೆ", "ಪತ್ರ ಸಂಖ್ಯೆ"
    ]

    if any(word in q for word in reference_words):

        match = re.search(
            r"\b[A-Z]{2,}[-/][A-Z0-9/-]{4,}\b",
            text,
            re.I
        )

        if match:
            answer = match.group(0)
            return answer, answer

        return "Reference number not found in the document.", ""

    # --------------------------------------------------
    # 3. DATE QUESTIONS
    # --------------------------------------------------

    date_question_words = [
        "date", "which date", "when issued",
        "ಯಾವ ದಿನಾಂಕ", "ಯಾವ ದಿನಾಂಕದಂದು",
        "ಹೊರಡಿಸಲಾಗಿದೆ", "ಹೊರಡಿಸಿದ ದಿನಾಂಕ"
    ]

    date_pattern = (
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
        r"|\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
    )

    if any(word in q for word in date_question_words):

        match = re.search(date_pattern, text, re.I)

        if match:
            answer = match.group(0)
            return answer, answer

        return "No date found in the document.", ""

    # --------------------------------------------------
    # 4. DEADLINE QUESTIONS
    # --------------------------------------------------

    deadline_words = [
        "last date", "deadline", "due date",
        "ಕೊನೆಯ ದಿನಾಂಕ", "ಸಲ್ಲಿಸಲು"
    ]

    if any(word in q for word in deadline_words):

        for sentence in sentences:
            low = sentence.lower()

            has_date = bool(
                re.search(date_pattern, sentence, re.I)
            )

            has_deadline_context = any(word in low for word in [
                "submit", "submission", "deadline",
                "ಕೊನೆಯ ದಿನಾಂಕ", "ಸಲ್ಲಿಸಲು", "ಅರ್ಜಿ"
            ])

            if has_date and has_deadline_context:
                return sentence, sentence

        return "No submission deadline found in the document.", ""

    # --------------------------------------------------
    # 5. CONTACT QUESTIONS
    # --------------------------------------------------

    contact_words = [
        "contact", "phone", "number",
        "ಸಂಪರ್ಕ", "ದೂರವಾಣಿ"
    ]

    if any(word in q for word in contact_words):

        match = re.search(
            r"(?<!\d)[6-9]\d{9}(?!\d)",
            text
        )

        if match:
            answer = match.group(0)
            return answer, answer

        return "Contact number not found in the document.", ""

    # --------------------------------------------------
    # 6. EDUCATIONAL TOUR TIMING
    # --------------------------------------------------

    tour_time_words = [
        "which month", "by which month",
        "ಯಾವ ತಿಂಗಳು", "ಯಾವ ತಿಂಗಳ",
        "ಯಾವಾಗ ಪೂರ್ಣಗೊಳಿಸಬೇಕು",
        "ಯಾವಾಗ ಪ್ರವಾಸ"
    ]

    if any(word in q for word in tour_time_words):

        result = find_sentence([
            "ಡಿಸೆಂಬರ್", "ಪ್ರವಾಸ"
        ])

        if result:
            return result

        return "Tour timing could not be reliably extracted.", ""

    # --------------------------------------------------
    # 7. TRANSPORT QUESTIONS
    # --------------------------------------------------

    transport_words = [
        "bus", "transport", "vehicle",
        "ಬಸ್", "ವಾಹನ", "ಸಾರಿಗೆ"
    ]

    if any(word in q for word in transport_words):

        result = find_sentence([
            "ಕರ್ನಾಟಕ ರಾಜ್ಯ ರಸ್ತೆ ಸಾರಿಗೆ",
            "ಪ್ರವಾಸೋದ್ಯಮ ಇಲಾಖಾ ವಾಹನ",
            "ಖಾಸಗಿ", "ಮಿನಿ ಬಸ್"
        ])

        if result:
            return result

        return "Transport information not found.", ""

    # --------------------------------------------------
    # 8. SAFETY QUESTIONS
    # --------------------------------------------------

    safety_words = [
        "safety", "health", "covid",
        "ಸುರಕ್ಷತೆ", "ಆರೋಗ್ಯ", "ಕೋವಿಡ್"
    ]

    if any(word in q for word in safety_words):

        result = find_sentence([
            "ಮಕ್ಕಳ ಆರೋಗ್ಯ",
            "ಸುರಕ್ಷತಾ ಕ್ರಮ",
            "ಅವಘಡಗಳಿಗೆ"
        ])

        if result:
            return result

        return "Safety information not found.", ""

    # --------------------------------------------------
    # 9. PERMISSION QUESTIONS
    # --------------------------------------------------

    permission_words = [
        "permission", "approval",
        "ಅನುಮತಿ", "ಅನುಮೋದನೆ"
    ]

    if any(word in q for word in permission_words):

        result = find_sentence([
            "ಅನುಮತಿ ನೀಡಲು",
            "ಅನುಮೋದನೆ ಪಡೆಯಬೇಕು",
            "ಕ್ಷೇತ್ರ ಶಿಕ್ಷಣಾಧಿಕಾರಿಗಳು"
        ])

        if result:
            return result

        return "Permission information not found.", ""

    # --------------------------------------------------
    # 10. MAIN TOPIC QUESTIONS
    # --------------------------------------------------

    topic_words = [
        "what is this circular about",
        "what is this notice about",
        "ಯಾವುದರ ಬಗ್ಗೆ ಇದೆ",
        "ಯಾವ ವಿಷಯಕ್ಕೆ ಸಂಬಂಧಿಸಿದೆ",
        "ಈ ಸುತ್ತೋಲೆ ಯಾವುದರ ಬಗ್ಗೆ",
        "ಈ ನೋಟಿಸ್ ಯಾವುದರ ಬಗ್ಗೆ"
    ]

    if any(word in q for word in topic_words):

        match = re.search(
            r"ವಿಷಯ\s*[:：]?\s*(.+?)(?=\n|ಉಲ್ಲೇಖ|$)",
            text
        )

        if match:
            answer = match.group(1).strip()
            return answer, answer

        return "Document topic could not be extracted.", ""

    # --------------------------------------------------
    # 11. DOCUMENT REQUIREMENT QUESTIONS
    # --------------------------------------------------

    document_words = [
        "document", "certificate", "proof",
        "ದಾಖಲೆ", "ಪ್ರಮಾಣಪತ್ರ"
    ]

    if any(word in q for word in document_words):

        result = find_sentence([
            "attach", "proof", "document",
            "ದಾಖಲೆ", "ಗುರುತಿನ ಚೀಟಿ", "ವಿಳಾಸ"
        ])

        if result:
            return result

        return "Document requirements not found.", ""

    # --------------------------------------------------
    # 12. GENERAL KEYWORD-BASED FALLBACK
    # --------------------------------------------------

    terms = [
        word.lower()
        for word in re.findall(r"\w+", q)
        if len(word) > 2
    ]

    scored = []

    for sentence in sentences:
        low = sentence.lower()

        score = sum(
            1 for term in terms if term in low
        )

        scored.append((score, sentence))

    score, best = max(
        scored,
        default=(0, "")
    )

    if score <= 0:
        return "I could not find a reliable answer in the document.", ""

    return best, best
