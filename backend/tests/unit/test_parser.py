from pathlib import Path

from services.processing.parser import PDFParser


def test_pdf_parser():

    pdf_path = Path("tests/fixtures/sample.pdf")

    parser = PDFParser()

    document = parser.parse(
        str(pdf_path)
    )

    assert document is not None

    assert document.page_count > 0

    assert document.text

    assert len(document.text) > 0