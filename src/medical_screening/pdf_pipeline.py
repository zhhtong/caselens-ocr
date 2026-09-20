from pathlib import Path
import json
import time
import fitz

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError:
    RapidOCR = None

# RapidOCR is the tested offline engine bundled with this project. PaddleOCR
# is intentionally not imported here: an unrelated partial installation must
# not silently take over the input contract and produce empty pages.
PaddleOCR = None

def extract_pdf(path: str | Path, cache_dir: str | Path | None = None, force_ocr: bool = False) -> dict:
    path = Path(path)
    doc = fitz.open(path)
    pages = []
    cache = Path(cache_dir) if cache_dir else None
    if cache:
        cache.mkdir(parents=True, exist_ok=True)
    ocr = PaddleOCR(lang="ch", use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False) if PaddleOCR else RapidOCR() if RapidOCR else None
    for i, page in enumerate(doc, 1):
        started = time.perf_counter()
        cached = cache / f"page-{i:04d}.json" if cache else None
        if cached and cached.exists() and not force_ocr:
            item = json.loads(cached.read_text(encoding="utf-8"))
            if item.get("text", "").strip():
                pages.append(item)
                continue
        text = page.get_text("text").strip()
        # Some scanners leave a tiny, broken text layer on every page. Treat
        # short text as incomplete and OCR the page, keeping the better result.
        original_text = text
        # OCR only pages with no reliable text. A manual force mode is
        # available for poor-quality embedded text layers.
        if (force_ocr or len(text) < 50) and ocr:
            # Cap raster size for CPU OCR. Oversized scans make OCR several
            # times slower without improving recognition of normal print.
            rect = page.rect
            scale = min(1.5, 2200 / max(rect.width, rect.height))
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            if RapidOCR:
                import numpy as np
                image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                result, _ = ocr(image)
                chunks = [] if result is None else [str(item[1]).strip() for item in result if str(item[1]).strip()]
                ocr_text = "\n".join(chunks)
                if len(ocr_text) > len(text):
                    text = ocr_text
            elif PaddleOCR:
                result = ocr.predict(pix.tobytes("png"))
                chunks = []
                for item in result:
                    data = item.json if hasattr(item, "json") else item
                    if isinstance(data, dict):
                        for line in data.get("res", {}).get("rec_texts", []): chunks.append(line)
                ocr_text = "\n".join(chunks)
                if len(ocr_text) > len(text):
                    text = ocr_text
        item = {"page": i, "text": text, "ocr_used": len(text) > len(original_text), "elapsed_seconds": round(time.perf_counter() - started, 3)}
        pages.append(item)
        if cached:
            cached.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"file": path.name, "pages": pages, "text": "\n\n".join(p["text"] for p in pages)}
