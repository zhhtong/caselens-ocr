import tempfile
from pathlib import Path

import streamlit as st

from src.medical_ocr.formatter import build_doubao_prompt, format_markdown
from src.medical_screening.pdf_pipeline import extract_pdf


def summarize_result(result: dict) -> dict:
    pages = result.get("pages", [])
    return {"pages": len(pages), "characters": len(result.get("text", "")), "ocr_pages": sum(bool(p.get("ocr_used")) for p in pages)}


st.set_page_config(page_title="病例 PDF OCR", layout="wide")
st.title("病例 PDF OCR 工具")
st.caption("本地离线提取 PDF 文字，不进行医学判断；结果可复制给豆包继续分析。")
files = st.file_uploader("上传一个或多个脱敏 PDF", type=["pdf"], accept_multiple_files=True)
st.info("首次处理扫描版 PDF 可能需要几分钟。程序不会把病例内容上传到外部服务。")

if st.button("开始 OCR", type="primary"):
    if not files:
        st.warning("请先上传至少一个 PDF 文件。")
    else:
        progress = st.progress(0, text="准备处理...")
        merged_text, merged_md = [], []
        for index, uploaded in enumerate(files):
            st.write(f"正在处理 {index + 1}/{len(files)}：{uploaded.name}")
            try:
                with st.spinner("正在提取文字并进行 OCR..."):
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp.write(uploaded.getbuffer())
                        pdf_path = tmp.name
                    cache_dir = Path("data/ocr_cache") / Path(uploaded.name).stem
                    result = extract_pdf(pdf_path, cache_dir=cache_dir)
                    md = format_markdown(uploaded.name, result["pages"])
                summary = summarize_result(result)
                st.success(f"完成：{summary['pages']} 页，{summary['characters']} 字符，OCR页 {summary['ocr_pages']} 页")
                base = Path(uploaded.name).stem
                c1, c2 = st.columns(2)
                c1.download_button("下载 TXT", result["text"], f"{base}.txt", "text/plain")
                c2.download_button("下载 Markdown", md, f"{base}.md", "text/markdown")
                merged_text.append(f"===== {uploaded.name} =====\n{result['text']}")
                merged_md.append(md)
            except Exception as exc:
                st.error(f"处理失败：{type(exc).__name__}: {exc}")
            progress.progress((index + 1) / len(files), text=f"已完成 {index + 1}/{len(files)}")
        if merged_text:
            st.subheader("批量合并下载")
            st.download_button("下载合并 TXT", "\n\n".join(merged_text), "病例OCR-合并.txt", "text/plain")
            st.download_button("下载合并 Markdown", "\n\n".join(merged_md), "病例OCR-合并.md", "text/markdown")

st.subheader("豆包分析提示词")
st.text_area("复制下面提示词，并把入排标准和上方生成的 TXT/MD 一起交给豆包", build_doubao_prompt(), height=300)
st.warning("OCR 结果可能存在识别错误；入排标准结论必须由研究医生人工审核。")
