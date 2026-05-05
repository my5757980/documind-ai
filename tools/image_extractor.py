import io
from typing import List


def extract_images_from_pdf(pdf_bytes: bytes) -> List[bytes]:
    import fitz
    from PIL import Image

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    result: List[bytes] = []

    for page in doc:
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                result.append(buf.getvalue())
            except Exception:
                continue

    doc.close()
    return result


def image_to_base64(img_bytes: bytes) -> str:
    import base64
    return base64.b64encode(img_bytes).decode("utf-8")
