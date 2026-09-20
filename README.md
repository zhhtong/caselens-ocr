# CaseLens OCR · 病例透镜

**Local-first PDF OCR for Chinese medical and clinical-research documents.**<br>
**面向中文医学与临床研究文档的本地优先 PDF OCR 工具。**

[![Tests](https://github.com/zhhtong/caselens-ocr/actions/workflows/tests.yml/badge.svg)](https://github.com/zhhtong/caselens-ocr/actions/workflows/tests.yml)
[![Release](https://img.shields.io/github/v/release/zhhtong/caselens-ocr)](https://github.com/zhhtong/caselens-ocr/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/zhhtong/caselens-ocr)](LICENSE)
[![Local first](https://img.shields.io/badge/data-local--first-2ea44f)](#privacy-and-safety--隐私与安全)

[**下载 Windows 版**](https://github.com/zhhtong/caselens-ocr/releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip) · [Windows 使用指南](docs/USING_WINDOWS_EXE.md) · [报告问题或建议](https://github.com/zhhtong/caselens-ocr/issues/new/choose)

CaseLens OCR 在本地提取普通 PDF 的文本层，并使用 RapidOCR 识别扫描页；文档默认不需要上传到云端 OCR 或大模型服务。它面向药企、CRO、医学部和临床研究团队的脱敏资料整理场景，输出 TXT/Markdown 供人工复核，而不是替代专业判断。

CaseLens OCR extracts text layers from regular PDFs and applies RapidOCR to scanned pages on the local computer. It is a research prototype for human-reviewed document workflows—not a medical device, diagnostic system, or autonomous trial-enrollment tool.

## Why CaseLens OCR? · 为什么选择它

- **本地优先 / Local-first:** OCR 默认在本机完成，不要求云端 OCR 或大模型 API。
- **中文医学文档 / Chinese medical documents:** 内置肿瘤、疾病、药物、生物标志物和实验室指标的示例词表。
- **兼顾电子与扫描 PDF / Mixed PDFs:** 优先提取文本层，扫描页回退到 RapidOCR。
- **开箱即用 / Easy to start:** 提供 Windows 压缩包，也支持 Python + Streamlit 运行。
- **人工可核对 / Human-reviewable:** 按页导出 TXT/Markdown，保留页面边界和证据上下文。

## Current capabilities · 当前能力

| Capability | Status | Notes |
| --- | --- | --- |
| Batch PDF upload / 批量 PDF 上传 | Available | Local Streamlit interface |
| Text-layer extraction / 文本层提取 | Available | For digitally generated PDFs |
| Scanned-page OCR / 扫描页识别 | Available | RapidOCR fallback |
| Page cache and resume / 页面缓存与续跑 | Available | Reduces repeated work |
| TXT and Markdown export | Available | Page-separated, review-friendly output |
| Windows packaged application | Available | Download from the v1.0.0 release |
| Fully automated medical decisions | **Not supported** | All output requires qualified human review |

The bundled vocabulary and knowledge files are demonstration seeds, not clinical guidelines or protocol-specific eligibility criteria.

## Quick start · 快速开始

### Windows（首次使用推荐）

1. 下载 [`CaseLensOCR-Windows-v1.0.0.zip`](https://github.com/zhhtong/caselens-ocr/releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip)。
2. 完整解压压缩包，不要单独移动 EXE；保持 `models` 文件夹与 `MedicalCaseOCR.exe` 的相对位置不变。
3. 双击 `MedicalCaseOCR.exe`。程序通常会自动打开浏览器；如未打开，请访问 `http://127.0.0.1:8501`。
4. 仅使用合成或可靠脱敏的 PDF，并人工复核 OCR 结果。

更多排障信息见 [Windows 使用指南](docs/USING_WINDOWS_EXE.md)。发布包大小为 `139,195,380` 字节，SHA-256 为 `0373fbef79c7e7f45cf991be64008597bca85aa0f6ccfb75ce1a3a2cc18189fb`。

### Python

```powershell
git clone https://github.com/zhhtong/caselens-ocr.git
cd caselens-ocr
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run ocr_app.py
```

打开 `http://127.0.0.1:8501`。首次安装依赖和准备 OCR 模型时可能需要网络；模型文件准备完成后，日常 OCR 流程可在本地运行。

## How it works · 工作流程

```text
合成或脱敏 PDF
    ↓
文本层提取 ── 扫描页使用 RapidOCR
    ↓
页面级缓存与人工检查
    ↓
TXT / 按页 Markdown
    ↓
人工复核或经组织批准的后续分析
```

CaseLens OCR 本身不会把导出的文本发送给第三方工具。是否将结果交给其他分析系统，取决于使用者和所在组织的数据政策。

## Output and limitations · 输出与限制

- OCR 可能出现漏字、错字、表格错位、阅读顺序错误和单位识别错误。
- 复杂表格、多栏排版、旋转页面、手写文字和低质量扫描件仍需重点人工核对。
- 示例医学词表和规则不能替代研究方案、临床指南或专业人员判断。
- 项目尚未经过医疗器械、临床决策支持或生产级安全系统的验证。
- 不公布未经可复现基准测试支持的准确率或性能数字。

## Privacy and safety · 隐私与安全

- 只处理合成数据或可靠脱敏的文档。
- 不要在 Issue、Pull Request、日志或截图中提交患者资料、受试者信息、凭据、保密方案、商业机密或专有 SOP。
- 提交公开示例前，应确认无法通过上下文重新识别个人。
- OCR 缓存、导出报告和本地模型目录不应提交到仓库。
- 安全问题请遵循 [`SECURITY.md`](SECURITY.md)，贡献前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## Feedback and contributing · 反馈与贡献

最有帮助的反馈包括：可复现的 OCR/版面失败、安装问题、合成测试样例、词表规范化、文档修复和页面布局改进。

- [报告普通 Bug](https://github.com/zhhtong/caselens-ocr/issues/new?template=bug_report.yml)
- [报告 OCR 或版面识别问题](https://github.com/zhhtong/caselens-ocr/issues/new?template=ocr_failure.yml)
- [提出功能建议](https://github.com/zhhtong/caselens-ocr/issues/new?template=feature_request.yml)

If CaseLens OCR helps your workflow, consider giving the repository a ⭐. It helps other teams discover a local-first OCR option. More importantly, please report reproducible OCR/layout failures using synthetic or demonstrably de-identified examples.

## Roadmap · 路线图

近期重点是可复现的 OCR 质量改进、Windows 安装诊断和自动化测试，而不是扩展未经验证的临床功能。详见 [`ROADMAP.md`](ROADMAP.md)。

## Repository map · 仓库结构

```text
ocr_app.py                 Streamlit OCR interface
src/medical_screening/     PDF extraction and OCR pipeline
src/medical_ocr/           TXT/Markdown formatting and prompts
config/                    Editable demo vocabulary and knowledge rules
tests/                     Unit tests
docs/                      Windows guide, design, and implementation notes
```

## License and disclaimer · 许可与声明

代码以 [MIT License](LICENSE) 发布。知识文件可能有独立的来源或署名要求，详见 [`config/README.md`](config/README.md)。本项目是研究和教学原型，不是医疗器械、诊断工具或临床决策支持系统；OCR 输出必须由具备相应能力的人员复核。
