import io
from typing import List
from models.report import UploadedDocument, FileSizeError, EmptyDocumentError

MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
SUPPORTED_FORMATS = {"pdf", "jpg", "jpeg", "png", "txt"}


def load_document(file_bytes: bytes, filename: str) -> UploadedDocument:
    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: .{ext}. Supported: PDF, JPG, PNG, TXT.")

    size = len(file_bytes)
    if size > MAX_SIZE_BYTES:
        raise FileSizeError(f"File too large ({size // (1024*1024)} MB). Maximum allowed: 10 MB.")

    fmt = "jpg" if ext == "jpeg" else ext
    text_content = ""
    images: List[bytes] = []
    page_count = 1

    if fmt == "pdf":
        text_content, images, page_count = _load_pdf(file_bytes)
    elif fmt in ("jpg", "png"):
        images = [file_bytes]
    elif fmt == "txt":
        text_content = file_bytes.decode("utf-8", errors="replace")

    if not text_content.strip() and not images:
        raise EmptyDocumentError("No readable content found in the uploaded file.")

    return UploadedDocument(
        name=filename,
        format=fmt,
        raw_bytes=file_bytes,
        size_bytes=size,
        text_content=text_content,
        images=images,
        page_count=page_count,
    )


def _load_pdf(pdf_bytes: bytes):
    import fitz
    from tools.image_extractor import extract_images_from_pdf

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    text = "\n".join(pages_text).strip()
    images = extract_images_from_pdf(pdf_bytes)
    page_count = len(doc)
    doc.close()
    return text, images, page_count
