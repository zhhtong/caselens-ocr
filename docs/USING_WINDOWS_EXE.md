# Windows EXE 使用说明

## 下载

在 GitHub 的 Releases 页面下载 `CaseLensOCR-Windows-v1.0.0.zip`，解压到本地文件夹。

## 启动

双击 `MedicalCaseOCR.exe`。程序会启动本地网页并自动打开浏览器：

```text
http://127.0.0.1:8501
```

请保持 `models` 文件夹与 EXE 位于同一目录。首次启动可能需要数秒加载 OCR 运行库。

## 使用

1. 上传已经脱敏的 PDF。
2. 点击“开始 OCR”。
3. 下载 TXT 或 Markdown 结果。
4. 由研究人员人工检查 OCR 结果后，再按照企业数据政策进行后续分析。

## 注意

程序默认在本机处理 PDF，不需要云端 OCR 或大模型 API。OCR 结果可能存在漏字、错字和表格布局问题，不能直接作为医学结论或临床试验入组结论。
