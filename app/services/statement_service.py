import fitz


def extract_text_from_pdf(file_path: str) -> str:
    document = fitz.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)