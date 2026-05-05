import pytest
from tools.document_loader import load_document
from models.report import FileSizeError, EmptyDocumentError


def test_txt_loading():
    content = b"This is a test document with some content."
    doc = load_document(content, "test.txt")
    assert doc.format == "txt"
    assert "test document" in doc.text_content
    assert doc.size_bytes == len(content)


def test_unsupported_format_raises():
    with pytest.raises(ValueError, match="Unsupported"):
        load_document(b"data", "file.docx")


def test_empty_file_raises():
    with pytest.raises(ValueError, match="empty"):
        load_document(b"", "empty.txt")


def test_oversized_file_raises():
    big = b"x" * (11 * 1024 * 1024)
    with pytest.raises(FileSizeError):
        load_document(big, "big.txt")


def test_jpeg_alias():
    from PIL import Image
    import io
    img = Image.new("RGB", (10, 10), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    doc = load_document(buf.getvalue(), "photo.jpeg")
    assert doc.format == "jpg"
    assert len(doc.images) == 1


def test_png_loading():
    from PIL import Image
    import io
    img = Image.new("RGB", (10, 10), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    doc = load_document(buf.getvalue(), "image.png")
    assert doc.format == "png"
    assert len(doc.images) == 1


def test_empty_txt_raises_empty_document():
    with pytest.raises(EmptyDocumentError):
        load_document(b"   ", "blank.txt")
