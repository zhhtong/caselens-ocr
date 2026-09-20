# CaseLens OCR

**A lightweight, fully local PDF OCR tool for pharmaceutical and clinical-research teams.**

中文名：**病例透镜** · GitHub：`caselens-ocr`

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Status](https://img.shields.io/badge/status-research%20prototype-orange) ![Privacy](https://img.shields.io/badge/data-local--first-success)

> Designed for pharmaceutical companies, CROs, and clinical-research teams. By default, documents stay on the local computer: no PDF upload, no cloud OCR, and no required large-model API. OCR output can contain errors and must be reviewed by qualified research or medical staff. This project does not diagnose, treat, prescribe, or make clinical-trial enrollment decisions.

CaseLens OCR handles the first step of a pharmaceutical or clinical-research workflow: upload a de-identified PDF, extract text locally with text-layer extraction and RapidOCR, then export the result for human review or optional downstream analysis. It does not require a model API key for OCR and does not need to send documents to the Internet.

## Why teams choose CaseLens OCR

- **Built for pharma and CRO workflows:** prepares admission records, examination reports, laboratory reports, pathology text, and medical orders for study-team review.
- **Privacy by design:** documents are processed on the local computer by default; patient PDFs do not need to leave the organization.
- **No mandatory large model:** the OCR pipeline uses local PDF extraction and OCR models, helping reduce network dependency, token cost, and data-exposure risk.
- **Simple deployment:** use the local web page or the Windows EXE package without configuring a cloud service or API key.
- **Human-controlled output:** exports TXT/Markdown for researchers to inspect and, if permitted by organizational policy, pass to a separate analysis tool.

## What works today

- Local Streamlit web interface with batch PDF upload.
- Text-layer extraction for normal PDFs and RapidOCR for scanned pages.
- Page-level cache and resumable processing.
- Chinese oncology, disease, biomarker, medication, and laboratory vocabulary.
- TXT and page-separated Markdown export.
- Copy-ready prompt for a separate assistant to assess study criteria with evidence and manual-review flags.
- Windows one-click launcher and self-contained EXE distribution option.

## 30-second quick start

### Windows EXE

Download [`CaseLensOCR-Windows-v1.0.0.zip`](https://github.com/zhhtong/caselens-ocr/releases/latest), extract it, and double-click `MedicalCaseOCR.exe`. The browser opens at `http://127.0.0.1:8501`. Keep the `models` folder beside the EXE. See the [Windows EXE guide](docs/USING_WINDOWS_EXE.md).

### Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run ocr_app.py
```

Open `http://127.0.0.1:8501` and upload only de-identified documents. The local OCR workflow does not require network access after installation and model files are available.

## Workflow

```text
de-identified PDF → local text extraction/OCR → TXT/Markdown → human review or approved downstream analysis
```

The bundled vocabulary and knowledge files are seed examples for a Demo. They are not clinical guidelines and are not a substitute for protocol-specific eligibility criteria.

## Data and privacy boundary

- By default, documents are processed locally and are not uploaded to a model provider or remote OCR service.
- Whether a later downstream tool receives exported text is controlled by the user and the organization's data policy; CaseLens OCR itself does not perform that upload.
- Never commit patient PDFs, clinical exports, OCR caches, generated reports, or identifiable data.
- Public examples must be synthetic or demonstrably de-identified.
- Do not upload confidential protocols, proprietary SOPs, credentials, or private model files.
- Local output directories are excluded by `.gitignore`.
- Before every push, inspect `git status` and the staged file list.

## Repository map

```text
ocr_app.py                 Streamlit OCR interface
src/medical_screening/     PDF extraction and OCR pipeline
src/medical_ocr/           TXT/Markdown formatting and prompts
config/                    Editable Demo vocabulary and knowledge rules
tests/                     Unit tests
docs/                      Design and implementation notes
```

## Contributing

Useful contributions include OCR failure cases made with synthetic data, vocabulary normalization, page-layout improvements, reproducible bug reports, and documentation fixes. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Support the project

If CaseLens OCR is useful for your pharmaceutical, CRO, or clinical-research workflow, please consider starring the repository. Stars help other teams discover a privacy-conscious local OCR approach. Feedback on OCR accuracy, document layouts, and synthetic test cases is especially welcome through Issues.

## License and disclaimer

Code is released under the MIT License. Knowledge files may have separate source or attribution requirements; see [`config/README.md`](config/README.md). This is a research prototype, not a medical device or clinical decision-support system.
