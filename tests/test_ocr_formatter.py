from src.medical_ocr.formatter import build_doubao_prompt, format_markdown


def test_markdown_contains_page_boundaries():
    result = format_markdown("病例.pdf", [{"page": 1, "text": "主诉"}, {"page": 2, "text": "检查"}])
    assert "病例.pdf" in result
    assert "第 1 页" in result
    assert "第 2 页" in result


def test_prompt_requires_evidence_and_manual_review():
    prompt = build_doubao_prompt()
    assert "入组标准" in prompt
    assert "排除标准" in prompt
    assert "原文" in prompt
    assert "人工审核" in prompt
