import json


def format_markdown(filename: str, pages: list[dict]) -> str:
    lines = [f"# OCR文本：{filename}", "", f"页数：{len(pages)}", ""]
    for item in pages:
        lines.extend([f"## 第 {item.get('page', '?')} 页", "", item.get("text", "").strip() or "（本页未识别到文字）", ""])
    return "\n".join(lines)


def build_doubao_prompt() -> str:
    return """请根据下面提供的病例OCR文本和研究方案，逐条核对入组标准与排除标准。

要求：
1. 每条标准分别输出：符合、不符合、无法判断；
2. 每条结论都引用病例原文，并尽量注明页码；
3. 病例中没有明确记载的内容不得推测，统一标记为无法判断；
4. 注意区分既往史、当前情况、治疗前后和阴性描述；
5. 最后给出需要研究医生人工审核的项目清单；
6. 这只是预筛整理，不替代研究医生的最终审核。

入组标准：
（请粘贴研究方案的入组标准）

排除标准：
（请粘贴研究方案的排除标准）

病例OCR文本：
（请粘贴本工具生成的TXT或Markdown文本）
"""
