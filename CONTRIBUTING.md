# Contributing

Contributions are welcome for OCR robustness, synthetic test cases, vocabulary normalization, documentation, and usability.

Please do not submit patient or participant data, real clinical PDFs, confidential protocols, proprietary SOPs, credentials, or paywalled source text. Use fully synthetic examples or public metadata only.

Before opening a pull request:

```powershell
python -m pytest -q
git diff --check
git status --short
```

Changes to medical vocabulary or rules should include provenance, a short rationale, and an explicit note about whether the result should trigger manual review.
