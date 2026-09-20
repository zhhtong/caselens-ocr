# Contributing to CaseLens OCR

Thank you for helping improve a local-first OCR workflow. The most useful contributions are:

- Minimal, reproducible OCR or page-layout failures made from synthetic or demonstrably de-identified files.
- Tests for extraction, formatting, configuration, and error handling.
- Vocabulary normalization with a documented source and rationale.
- Windows installation diagnostics, documentation fixes, and accessibility improvements.
- Focused usability changes that preserve the local-first data boundary.

## Protect sensitive information

Never submit patient or participant data, identifiable clinical PDFs, confidential protocols, proprietary SOPs, credentials, private model files, paywalled source text, OCR caches, or generated clinical exports. Screenshots and sample files must use synthetic data or material that is demonstrably de-identified.

If a problem cannot be reproduced without sensitive material, describe the structure of the failure without attaching the source document.

## Development setup on Windows

```powershell
git clone https://github.com/zhhtong/caselens-ocr.git
cd caselens-ocr
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the application with:

```powershell
streamlit run ocr_app.py
```

## Before opening a pull request

```powershell
python -m pytest -q
git diff --check
git status --short
```

Behavior changes should include a focused test. Keep pull requests small enough to review and explain why the change is needed, how it was tested, and whether it changes privacy or data-flow behavior.

Changes to medical vocabulary or rules must include provenance, a short rationale, and an explicit note about whether the result should trigger manual review. Demo knowledge files must not be presented as clinical guidelines.
