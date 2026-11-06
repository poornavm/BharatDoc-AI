
import streamlit as st
from datetime import datetime

from app.document_processor import extract_document_text
from app.analysis import extract_fields, summarize_text, answer_question


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="BharatDoc AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# MINIMAL DESIGN
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #142B4A;
    --blue: #315F99;
    --light-blue: #EAF1FA;
    --background: #F7F8FA;
    --border: #E2E6EC;
    --text: #26364A;
    --muted: #718096;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--background);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--navy);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--navy) !important;
    font-weight: 700 !important;
}

p, label, span {
    color: var(--text);
}

.brand {
    color: var(--navy);
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
}

.subtitle {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.7;
}

.panel {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}

.answer-panel {
    background: #EDF4FC;
    border-left: 4px solid var(--blue);
    border-radius: 9px;
    padding: 18px;
    line-height: 1.8;
    color: var(--navy);
}

.evidence-panel {
    background: #F3F6FA;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 16px;
    line-height: 1.7;
}

[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #26364A !important;
    -webkit-text-fill-color: #26364A !important;
    opacity: 1 !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    color: var(--navy) !important;
    border: 1px solid #D5DCE5 !important;
    border-radius: 9px !important;
}

.stButton > button {
    background: var(--navy);
    color: #FFFFFF !important;
    border: 1px solid var(--navy);
    border-radius: 8px;
    padding: 9px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: var(--blue);
    border-color: var(--blue);
}

.stDownloadButton > button {
    background: #FFFFFF;
    color: var(--navy) !important;
    border: 1px solid #C9D3E0;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: var(--light-blue);
    border-color: var(--blue);
}

[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px dashed #AABBD0;
    border-radius: 12px;
    padding: 14px;
}

hr {
    border-color: var(--border);
}

.stTabs [data-baseweb="tab"] {
    color: var(--navy);
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: var(--blue) !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

if "current_evidence" not in st.session_state:
    st.session_state.current_evidence = None

if "current_question" not in st.session_state:
    st.session_state.current_question = ""


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">📄 BharatDoc AI</div>',
        unsafe_allow_html=True
    )

    st.caption("Multilingual Document Intelligence")

    st.divider()

    st.markdown("### Document Language")

    language = st.selectbox(
        "Select language",
        ["English", "Kannada"],
        index=1
    )

    st.divider()

    st.markdown("### Recent History")

    if st.session_state.history:

        for item in reversed(st.session_state.history[-5:]):
            st.caption(
                f"📄 {item['filename']} · {item['time']}"
            )

    else:
        st.caption("Uploaded documents will appear here.")

    st.divider()

    st.caption("BharatDoc AI · Prototype v1.0")


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="brand">Multilingual Document Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload official documents, extract key information, '
    'generate summaries and ask questions in English or Kannada.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ==================================================
# DOCUMENT UPLOAD
# ==================================================

st.markdown("### Upload Document")

uploaded = st.file_uploader(
    "Choose a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)


# ==================================================
# DOCUMENT PROCESSING
# ==================================================

if uploaded:

    with st.spinner("Analyzing your document..."):

        result = extract_document_text(
            uploaded.getvalue(),
            uploaded.name
        )

    text = result["text"]

    if not text.strip():
        st.error(
            "Unable to extract readable text. "
            "Try uploading a clearer document."
        )
        st.stop()

    # Add document to session history
    if (
        not st.session_state.history
        or st.session_state.history[-1]["filename"] != uploaded.name
    ):

        st.session_state.history.append({
            "filename": uploaded.name,
            "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
        })

    # Extract document information
    fields = extract_fields(text)
    summary = summarize_text(text)

    st.caption(
        f"File: {uploaded.name} | "
        f"Extraction method: {result['method']}"
    )

    st.write("")

    # ==================================================
    # MAIN LAYOUT
    # ==================================================

    document_col, analysis_col = st.columns(
        [0.9, 1.1],
        gap="large"
    )

    # --------------------------------------------------
    # LEFT: DOCUMENT PREVIEW
    # --------------------------------------------------

    with document_col:

        st.markdown("### Document Preview")

        st.text_area(
            "Extracted document content",
            value=text,
            height=530,
            disabled=True,
            label_visibility="collapsed"
        )

        st.download_button(
            "↓ Download Extracted Text",
            data=text,
            file_name="extracted_document.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --------------------------------------------------
    # RIGHT: ANALYSIS TABS
    # --------------------------------------------------

    with analysis_col:

        summary_tab, fields_tab, qa_tab = st.tabs([
            "Summary",
            "Extracted Fields",
            "Q&A"
        ])

        # ==============================================
        # SUMMARY
        # ==============================================

        with summary_tab:

            st.markdown("### Document Summary")

            st.markdown(
                '<div class="panel">',
                unsafe_allow_html=True
            )

            st.write(summary)

            st.markdown("</div>", unsafe_allow_html=True)

        # ==============================================
        # EXTRACTED FIELDS
        # ==============================================

        with fields_tab:

            st.markdown("### Extracted Information")

            st.markdown("**Dates**")

            if fields["dates_found"]:
                for date in fields["dates_found"]:
                    st.write(f"• {date}")
            else:
                st.caption("No dates detected.")

            st.divider()

            st.markdown("**Phone Numbers**")

            if fields["phone_numbers"]:
                for phone in fields["phone_numbers"]:
                    st.write(f"• {phone}")
            else:
                st.caption("No phone numbers detected.")

            st.divider()

            st.markdown("**Email Addresses**")

            if fields["email_addresses"]:
                for email in fields["email_addresses"]:
                    st.write(f"• {email}")
            else:
                st.caption("No email addresses detected.")

            st.divider()

            st.markdown("**Reference Numbers**")

            if fields["reference_numbers"]:
                for ref in fields["reference_numbers"]:
                    st.write(f"• {ref}")
            else:
                st.caption("No reference numbers detected.")

            st.caption(fields["note"])

        # ==============================================
        # QUESTION ANSWERING
        # ==============================================

        with qa_tab:

            st.markdown("### Ask Your Document")

            st.caption(
                "Ask questions about the uploaded document "
                "in English or Kannada."
            )

            question = st.text_input(
                "Your question",
                placeholder="What is the document about?",
                key="document_question"
            )

            if st.button(
                "Get Answer",
                disabled=not question.strip(),
                key="get_answer"
            ):

                with st.spinner("Finding supporting evidence..."):

                    answer, evidence = answer_question(
                        text,
                        question
                    )

                st.session_state.current_answer = answer
                st.session_state.current_evidence = evidence
                st.session_state.current_question = question

            if st.session_state.current_answer is not None:

                st.markdown("### Answer")

                st.markdown(
                    '<div class="answer-panel">',
                    unsafe_allow_html=True
                )

                st.write(st.session_state.current_answer)

                st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.current_evidence:

                    st.markdown("### Evidence from Document")

                    st.markdown(
                        '<div class="evidence-panel">',
                        unsafe_allow_html=True
                    )

                    st.write(st.session_state.current_evidence)

                    st.markdown("</div>", unsafe_allow_html=True)

                else:

                    st.warning(
                        "The document does not contain enough "
                        "evidence for a reliable answer."
                    )

    # ==================================================
    # DOWNLOAD ANALYSIS REPORT
    # ==================================================

    st.divider()

    st.markdown("### Download Analysis Report")

    report = f"""
BHARATDOC AI
DOCUMENT ANALYSIS REPORT

File: {uploaded.name}
Extraction method: {result['method']}

----------------------------------------
DOCUMENT SUMMARY
----------------------------------------

{summary}

----------------------------------------
EXTRACTED INFORMATION
----------------------------------------

Dates: {', '.join(fields['dates_found']) or 'None found'}

Phone numbers: {', '.join(fields['phone_numbers']) or 'None found'}

Email addresses: {', '.join(fields['email_addresses']) or 'None found'}

Reference numbers: {', '.join(fields['reference_numbers']) or 'None found'}

----------------------------------------
QUESTION AND ANSWER
----------------------------------------

Question: {st.session_state.current_question or 'No question asked'}

Answer: {st.session_state.current_answer or 'No answer generated'}

Evidence: {st.session_state.current_evidence or 'No evidence available'}

----------------------------------------
NOTE
----------------------------------------

Prototype extraction and analysis results.
Verify extracted information against the original document.
"""

    st.download_button(
        "↓ Download Analysis Report",
        data=report,
        file_name="BharatDoc_Analysis_Report.txt",
        mime="text/plain"
    )


# ==================================================
# EMPTY STATE
# ==================================================

else:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown("### Welcome to BharatDoc AI")

    st.write(
        "Upload a government notice, circular, application "
        "or other document to begin."
    )

    st.markdown("#### Features")

    st.write("• PDF text extraction and scanned document OCR")
    st.write("• Key information and field extraction")
    st.write("• Automatic document summarization")
    st.write("• English and Kannada document support")
    st.write("• Evidence-based document question answering")
    st.write("• Downloadable analysis reports")

    st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "BharatGen Patram and IndicTrans2 are integration targets; "
        "their model inference is not currently active."
    )
