# CaseLens OCR GitHub Growth Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a trustworthy GitHub discovery-to-feedback funnel that helps Chinese medical/CRO users and international OCR developers understand, download, verify, discuss, and star CaseLens OCR.

**Architecture:** Keep the OCR implementation unchanged and improve the repository-facing layer in six isolated units: landing page, contributor guidance, structured issue intake, continuous integration, release communication, and GitHub repository metadata. All claims remain grounded in current code and the published Windows asset.

**Tech Stack:** GitHub Markdown, GitHub Issue Forms YAML, GitHub Actions YAML, Python 3.10+, pytest, GitHub REST API, git.

---

## File Structure

- Modify `README.md`: bilingual project landing page and conversion path.
- Modify `CONTRIBUTING.md`: reproducible setup, test, safety, and PR guidance.
- Modify `SECURITY.md`: actionable private-reporting guidance without promising a nonexistent channel.
- Modify `RELEASE_NOTES_v1.0.0.md`: bilingual release summary, install steps, checksum, limits, feedback link.
- Create `.github/workflows/tests.yml`: automated Python test workflow.
- Create `.github/ISSUE_TEMPLATE/bug_report.yml`: general reproducible bug intake.
- Create `.github/ISSUE_TEMPLATE/ocr_failure.yml`: OCR/layout failure intake with sensitive-data warnings.
- Create `.github/ISSUE_TEMPLATE/feature_request.yml`: workflow-focused feature requests.
- Create `.github/ISSUE_TEMPLATE/config.yml`: disable blank issues and route security/contribution questions.
- Create `.github/PULL_REQUEST_TEMPLATE.md`: lightweight verification and privacy checklist.
- Create `ROADMAP.md`: near-term, evidence-based roadmap separated from speculative features.
- Modify GitHub repository settings: description and ten focused topics.
- Modify GitHub release `v1.0.0`: use the verified release notes without replacing the binary asset.

### Task 1: Establish a verified baseline

**Files:**
- Read: `requirements.txt`
- Test: `tests/test_core.py`
- Test: `tests/test_ocr_formatter.py`

- [ ] **Step 1: Confirm the working tree only contains the approved design and plan commits**

Run:

```powershell
git status --short
git log -3 --oneline
```

Expected: no uncommitted product changes; latest commits include the design and plan documents.

- [ ] **Step 2: Create an isolated Python environment**

Run:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Expected: dependencies install successfully under Python 3.10. If Python 3.10 is unavailable, use the newest installed compatible Python and record the exact version.

- [ ] **Step 3: Run the current tests before changing repository files**

Run:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Expected: 14 tests pass. If not, record the exact baseline failure and do not attribute it to the documentation work.

### Task 2: Rebuild the repository landing page

**Files:**
- Modify: `README.md`
- Create: `ROADMAP.md`

- [ ] **Step 1: Replace the README opening with a concise bilingual value proposition**

Use this opening structure and wording:

```markdown
# CaseLens OCR · 病例透镜

**Local-first PDF OCR for Chinese medical and clinical-research documents.**<br>
**面向中文医学与临床研究文档的本地优先 PDF OCR 工具。**

[![Tests](https://github.com/zhhtong/caselens-ocr/actions/workflows/tests.yml/badge.svg)](https://github.com/zhhtong/caselens-ocr/actions/workflows/tests.yml)
[![Release](https://img.shields.io/github/v/release/zhhtong/caselens-ocr)](https://github.com/zhhtong/caselens-ocr/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/zhhtong/caselens-ocr)](LICENSE)
[![Local first](https://img.shields.io/badge/data-local--first-2ea44f)](#privacy-and-safety--隐私与安全)

[下载 Windows 版](https://github.com/zhhtong/caselens-ocr/releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip) · [查看使用指南](docs/USING_WINDOWS_EXE.md) · [报告问题](https://github.com/zhhtong/caselens-ocr/issues/new/choose)
```

Follow it with a two-sentence summary that says PDFs are processed locally by default, mixed text/scanned pages are supported, and output requires human review.

- [ ] **Step 2: Organize the README into the visitor journey**

Use these sections in this order:

```markdown
## Why CaseLens OCR? · 为什么选择它
## Current capabilities · 当前能力
## Quick start · 快速开始
### Windows (recommended for first use)
### Python
## How it works · 工作流程
## Output and limitations · 输出与限制
## Privacy and safety · 隐私与安全
## Feedback and contributing · 反馈与贡献
## Roadmap · 路线图
## Repository map · 仓库结构
## License and disclaimer · 许可与声明
```

Keep current capabilities factual: batch PDF upload, text-layer extraction, RapidOCR fallback for scanned pages, page cache/resume, Chinese medical vocabulary, TXT/Markdown export, and optional copy-ready downstream prompt. Explicitly state that the project is a research prototype, not a medical device or autonomous eligibility decision system.

- [ ] **Step 3: Make both quick starts executable**

Windows instructions must link directly to the published ZIP, tell users to extract the complete archive, keep `models` beside the EXE, launch `MedicalCaseOCR.exe`, and open `http://127.0.0.1:8501` if the browser does not open.

Python instructions must use:

```powershell
git clone https://github.com/zhhtong/caselens-ocr.git
cd caselens-ocr
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run ocr_app.py
```

- [ ] **Step 4: Add restrained conversion prompts**

Use one call-to-action near the feedback section:

```markdown
If CaseLens OCR helps your workflow, consider giving the repository a ⭐. It helps other teams discover a local-first OCR option. More importantly, please report reproducible OCR/layout failures using synthetic or demonstrably de-identified examples.
```

Do not repeat the Star request elsewhere.

- [ ] **Step 5: Create the focused roadmap**

Create `ROADMAP.md` with three groups:

```markdown
# Roadmap

## Now — reliability and documentation
- Collect reproducible OCR/layout failures using synthetic or demonstrably de-identified files.
- Improve installation diagnostics and Windows packaging documentation.
- Expand automated tests around extraction, formatting, and configuration loading.

## Next — OCR quality and usability
- Evaluate page-layout handling against a documented synthetic benchmark.
- Improve tables, multi-column pages, page rotation, and low-quality scan handling.
- Add export metadata that makes page-level human review easier.

## Later — only with evidence and maintainers
- Additional operating-system packages.
- Optional offline model choices with documented size and accuracy trade-offs.
- Protocol-specific extensions maintained separately from the OCR core.

Roadmap items are intentions, not commitments. Clinical validation, autonomous diagnosis, and autonomous trial-enrollment decisions are not project goals.
```

- [ ] **Step 6: Validate README links and wording**

Run:

```powershell
git diff --check
Select-String -Path README.md -Pattern 'releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip','issues/new/choose','ROADMAP.md'
```

Expected: no whitespace errors and all three destinations appear.

- [ ] **Step 7: Commit the landing-page changes**

```powershell
git add README.md ROADMAP.md
git commit -m "docs: rebuild repository landing page"
```

### Task 3: Build the feedback and contribution funnel

**Files:**
- Modify: `CONTRIBUTING.md`
- Modify: `SECURITY.md`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/ocr_failure.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Expand contributor setup and contribution targets**

`CONTRIBUTING.md` must contain: welcomed contribution categories; prohibited sensitive material; Windows virtual-environment setup; the exact `python -m pytest -q` and `git diff --check` checks; requirements for vocabulary/rule provenance; and a request that behavior changes include tests.

- [ ] **Step 2: Make security reporting accurate**

Update `SECURITY.md` to direct reporters to GitHub private vulnerability reporting only if the repository exposes it. Otherwise request a minimal public issue containing no exploit detail or sensitive data and ask the maintainer to establish a private channel. Do not claim that a private contact channel already exists.

- [ ] **Step 3: Create the general bug form**

`bug_report.yml` must require: problem summary, installation mode (`Windows release`, `Python source`, `Other`), operating system, CaseLens version/commit, reproduction steps, expected behavior, actual behavior, and sanitized logs. Add a required checkbox confirming that no patient data, credentials, confidential protocols, or proprietary files are included.

- [ ] **Step 4: Create the OCR failure form**

`ocr_failure.yml` must require: document type, whether the PDF has a text layer, affected page layout, expected text, OCR result, reproducible steps, and a required privacy confirmation. The description must ask for a minimal synthetic example and prohibit real patient files.

- [ ] **Step 5: Create the feature request form**

`feature_request.yml` must require: workflow/problem, current workaround, proposed outcome, primary user group, and privacy/local-first implications. It must not assume the requested implementation.

- [ ] **Step 6: Configure the issue chooser and PR checklist**

`config.yml` must set `blank_issues_enabled: false` and link to `SECURITY.md` and `CONTRIBUTING.md`. The pull-request template must include summary, validation, privacy/data checklist, and screenshots only when UI behavior changes and only with synthetic data.

- [ ] **Step 7: Parse all YAML files**

Run:

```powershell
.venv\Scripts\python.exe -c "import pathlib, yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in pathlib.Path('.github/ISSUE_TEMPLATE').glob('*.yml')]; print('issue forms: OK')"
```

Expected: `issue forms: OK`.

- [ ] **Step 8: Commit community-health files**

```powershell
git add CONTRIBUTING.md SECURITY.md .github/ISSUE_TEMPLATE .github/PULL_REQUEST_TEMPLATE.md
git commit -m "community: add structured feedback templates"
```

### Task 4: Add continuous integration

**Files:**
- Create: `.github/workflows/tests.yml`

- [ ] **Step 1: Create the GitHub Actions test workflow**

Use this workflow:

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  pytest:
    runs-on: windows-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.10"
          cache: pip
      - name: Install dependencies
        run: python -m pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest -q
```

Windows is intentional because the primary downloadable product is Windows-first and the test suite does not require Linux-specific behavior.

- [ ] **Step 2: Validate workflow YAML**

Run:

```powershell
.venv\Scripts\python.exe -c "import yaml; d=yaml.safe_load(open('.github/workflows/tests.yml', encoding='utf-8')); assert d['jobs']['pytest']['runs-on']=='windows-latest'; print('workflow: OK')"
```

Expected: `workflow: OK`.

- [ ] **Step 3: Run the full local test suite again**

Run:

```powershell
.venv\Scripts\python.exe -m pytest -q
git diff --check
```

Expected: 14 tests pass and no whitespace errors.

- [ ] **Step 4: Commit the workflow**

```powershell
git add .github/workflows/tests.yml
git commit -m "ci: test the project on Windows"
```

### Task 5: Improve the release communication

**Files:**
- Modify: `RELEASE_NOTES_v1.0.0.md`

- [ ] **Step 1: Rewrite the checked-in release notes**

The release notes must include:

- Bilingual one-line positioning.
- Direct Windows download link.
- Five verified capabilities already present in the current notes.
- Installation: extract the complete archive, preserve `models`, run `MedicalCaseOCR.exe`.
- SHA-256: `0373fbef79c7e7f45cf991be64008597bca85aa0f6ccfb75ce1a3a2cc18189fb`.
- Asset size: `139,195,380 bytes`.
- Research-prototype, human-review, and de-identification limits.
- Feedback link to `https://github.com/zhhtong/caselens-ocr/issues/new/choose`.

- [ ] **Step 2: Verify the direct asset**

Run:

```powershell
curl.exe -I -L "https://github.com/zhhtong/caselens-ocr/releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip"
```

Expected: final HTTP `200`, filename `CaseLensOCR-Windows-v1.0.0.zip`, and content length `139195380`.

- [ ] **Step 3: Commit release-note changes**

```powershell
git add RELEASE_NOTES_v1.0.0.md
git commit -m "docs: improve v1.0.0 release guidance"
```

### Task 6: Publish and configure GitHub

**Files:**
- Remote repository: `zhhtong/caselens-ocr`
- Remote release: `v1.0.0`

- [ ] **Step 1: Perform the pre-push safety and quality review**

Run:

```powershell
git status --short
git diff origin/main...HEAD --check
.venv\Scripts\python.exe -m pytest -q
git diff --name-only origin/main...HEAD
```

Expected: only approved documentation, community, workflow, roadmap, design, and plan files; tests pass; no patient data, binaries, caches, environment files, or credentials.

- [ ] **Step 2: Push the commits**

Run:

```powershell
git push origin main
```

Expected: `main` advances successfully.

- [ ] **Step 3: Configure description and topics through the authenticated GitHub API**

Set description exactly to:

```text
Local-first PDF OCR for Chinese medical and clinical-research documents. Windows app + Python/Streamlit.
```

Set topics exactly to:

```text
ocr, pdf-ocr, rapidocr, streamlit, medical-ocr, healthcare, clinical-research, local-first, privacy, chinese-ocr
```

Leave the homepage empty unless a verified working project page exists.

- [ ] **Step 4: Update the existing GitHub release body**

Replace the `v1.0.0` release body with the exact contents of `RELEASE_NOTES_v1.0.0.md`. Preserve the tag, release title, published state, and existing asset. Do not upload or rebuild the ZIP.

- [ ] **Step 5: Verify public repository state**

Confirm via GitHub API or the logged-in browser:

- Description matches the approved text.
- All ten topics are present.
- README renders and direct links work.
- Three issue forms appear in the issue chooser.
- Tests workflow exists and completes successfully.
- Release remains published and the existing ZIP asset remains `139,195,380` bytes.

- [ ] **Step 6: Record the final evidence**

Run:

```powershell
git status --short
git log --oneline origin/main..HEAD
```

Expected: clean working tree and no local commits left unpushed. Report the workflow result, release URL, download URL, and any known limitations to the user.
