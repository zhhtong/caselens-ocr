# CaseLens OCR v1.0.0

首个可下载的 Windows 版本：面向中文医学与临床研究文档的本地优先 PDF OCR 工具。<br>
First downloadable Windows release: local-first PDF OCR for Chinese medical and clinical-research documents.

## 下载 / Download

[`CaseLensOCR-Windows-v1.0.0.zip`](https://github.com/zhhtong/caselens-ocr/releases/download/v1.0.0/CaseLensOCR-Windows-v1.0.0.zip)

- 文件大小 / Size: `139,195,380 bytes`
- SHA-256: `0373fbef79c7e7f45cf991be64008597bca85aa0f6ccfb75ce1a3a2cc18189fb`

## 主要能力 / Highlights

- 本地 PDF 文本层提取，并使用 RapidOCR 识别扫描页。
- 支持合成或可靠脱敏病例 PDF 的 TXT/Markdown 导出。
- 日常 OCR 流程不要求大模型 API 或云端 OCR 服务。
- 提供 Windows EXE，目标电脑无需单独安装 Python。
- 附带用于演示的中文医学词表和肿瘤相关规则文件。

## 安装 / Install

1. 下载并完整解压 ZIP。
2. 保持 `models` 文件夹与 `MedicalCaseOCR.exe` 的相对位置不变。
3. 双击 `MedicalCaseOCR.exe`。如果浏览器没有自动打开，请访问 `http://127.0.0.1:8501`。
4. 仅使用合成或可靠脱敏的文档，并人工复核输出。

## 使用边界 / Limitations

这是研究和教学原型，不是医疗器械、诊断工具或临床决策支持系统。OCR 可能出现漏字、错字、表格错位、阅读顺序和单位识别错误，输出必须由具备相应能力的人员复核。

请勿上传或公开未脱敏的患者资料、受试者信息、保密方案、凭据、专有文件或商业机密。

发现问题？请通过[结构化 Issue 表单](https://github.com/zhhtong/caselens-ocr/issues/new/choose)提交可复现步骤，并且只使用合成或可靠脱敏的示例。
