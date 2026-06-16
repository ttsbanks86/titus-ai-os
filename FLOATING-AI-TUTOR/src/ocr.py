#!/usr/bin/env python3
"""OCR text extraction from captured images."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtGui import QPixmap, QImage


def pil_image_from_pixmap(pixmap: QPixmap) -> object | None:
    """Convert QPixmap to PIL Image for OCR processing."""
    try:
        from PIL import Image
        # Save to bytes and reload
        img = pixmap.toImage()
        ptr = img.bits()
        ptr.setsize(img.sizeInBytes())
        arr = bytes(ptr.asstring())
        pil_img = Image.frombytes(
            "RGBA" if img.hasAlphaChannel() else "RGB",
            (img.width(), img.height()),
            arr,
            "raw",
            "BGRA" if img.hasAlphaChannel() else "BGR",
        )
        return pil_img
    except ImportError:
        return None


def ocr_pytesseract(pixmap: QPixmap) -> Optional[str]:
    """OCR using pytesseract (requires Tesseract-OCR installed)."""
    try:
        import pytesseract
        pil_img = pil_image_from_pixmap(pixmap)
        if pil_img is None:
            return None
        text = pytesseract.image_to_string(pil_img)
        return text.strip() if text.strip() else None
    except (ImportError, Exception):
        return None


def ocr_easyocr(pixmap: QPixmap) -> Optional[str]:
    """OCR using easyocr (downloads models on first use)."""
    try:
        import easyocr
        pil_img = pil_image_from_pixmap(pixmap)
        if pil_img is None:
            return None
        reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        results = reader.readtext(pil_img)
        texts = [r[1] for r in results if r[2] > 0.3]
        return "\n".join(texts) if texts else None
    except (ImportError, Exception):
        return None


def ocr_windows(pixmap: QPixmap) -> Optional[str]:
    """Attempt OCR using Windows built-in tools (fallback)."""
    # Save pixmap to temp file
    import tempfile
    tmp = Path(tempfile.gettempdir()) / "ai-tutor-ocr-temp.png"
    pixmap.save(str(tmp), "PNG")

    try:
        # Try using Windows.Media.Ocr via PowerShell (Windows 10+)
        ps_script = f"""
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        $asTask = [System.WindowsRuntimeSystemExtensions].GetMethod('AsTask', [System.Type[]]@([Windows.Foundation.IAsyncOperation`1], [System.Threading.CancellationToken]))
        $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync('{tmp}').AsTask().GetAwaiter().GetResult()
        $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).AsTask().GetAwaiter().GetResult()
        $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).AsTask().GetAwaiter().GetResult()
        $bitmap = $decoder.GetSoftwareBitmapAsync().AsTask().GetAwaiter().GetResult()
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
        if ($engine) {{
            $result = $engine.RecognizeAsync($bitmap).AsTask().GetAwaiter().GetResult()
            $result.Text
        }}
        """
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
            capture_output=True, text=True, timeout=30,
        )
        text = result.stdout.strip()
        if text:
            return text
    except Exception:
        pass
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
    return None


def extract_text(pixmap: QPixmap) -> str:
    """Extract text from a captured screen region using best available OCR."""
    # Try pytesseract first (fastest if installed)
    text = ocr_pytesseract(pixmap)
    if text:
        return text

    # Try easyocr
    text = ocr_easyocr(pixmap)
    if text:
        return text

    # Try Windows built-in OCR
    text = ocr_windows(pixmap)
    if text:
        return text

    return ""


def get_ocr_status() -> dict:
    """Check which OCR engines are available."""
    status = {
        "pytesseract": False,
        "easyocr": False,
        "windows": True,  # Always attempt
        "pillow": False,
    }
    try:
        import pytesseract
        status["pytesseract"] = True
    except ImportError:
        pass
    try:
        import easyocr
        status["easyocr"] = True
    except ImportError:
        pass
    try:
        from PIL import Image
        status["pillow"] = True
    except ImportError:
        pass
    return status
