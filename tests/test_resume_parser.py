import pytest
from app.resume_parser import extract_text_from_pdf

def test_extract_text():
    with open("data/sample_resume.pdf", "rb") as f:
        text = extract_text_from_pdf(f)
        assert len(text) > 0
