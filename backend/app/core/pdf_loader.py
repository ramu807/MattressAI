from dataclasses import dataclass, field
from pathlib import Path
from PyPDF2 import PdfReader


@dataclass
class PageContent:
    text: str
    metadata: dict = field(default_factory=dict)


def load_pdf(file_path: str) -> list[PageContent]:
    """Extract text from a PDF file, returning content per page."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(str(path))
    pages: list[PageContent] = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append(PageContent(
                text=text,
                metadata={
                    "source": path.name,
                    "page": page_num,
                    "total_pages": len(reader.pages),
                }
            ))

    return pages


def load_pdfs_from_directory(directory: str) -> list[PageContent]:
    """Load all PDFs from a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    all_pages: list[PageContent] = []
    for pdf_file in sorted(dir_path.glob("*.pdf")):
        pages = load_pdf(str(pdf_file))
        all_pages.extend(pages)

    return all_pages
