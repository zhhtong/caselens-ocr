import json
import re
from datetime import date
from .config import load_yaml

def extract_case(pdf_result: dict) -> dict:
    text = pdf_result["text"]
    terms = load_yaml("vocabulary.yaml")
    fields = {"age": None, "sex": None, "stage": None, "reference_date": None, "metastases": [], "diagnosis": [], "biomarkers": [], "treatments": [], "treatment_timeline": [], "treatment_lines": [], "washout_periods": [], "response": [], "lesions": [], "labs": []}
    age = re.search(r"(?:年龄[：:\s]*)?(\d{1,3})\s*岁", text)
    if age:
        fields["age"] = int(age.group(1))
    sex = re.search(r"(?:女|女性|男|男性)", text)
    if sex:
        fields["sex"] = "女" if sex.group(0) in {"女", "女性"} else "男"
    stage = re.search(r"(?:IV|III|II|I|Ⅳ|Ⅲ|Ⅱ|Ⅰ)\s*期", text, re.I)
    if stage:
        fields["stage"] = stage.group(0).replace("Ⅳ", "IV").replace("Ⅲ", "III").replace("Ⅱ", "II").replace("Ⅰ", "I")
    dates = re.findall(r"20\d{2}[./年-]\d{1,2}(?:[./月-]\d{1,2})?", text)
    if dates:
        fields["reference_date"] = dates[-1].replace("年", "-").replace("月", "-").replace(".", "-").replace("/", "-").strip("-")
    for site in ["骨", "肝", "肺", "脑", "胸膜"]:
        for hit in re.finditer(site + r"(?:转移|受累|[、,，\s]{1,8}[^。；\n]{0,8}转移)", text):
            context = text[max(0, hit.start()-12):hit.end()+12]
            if not re.search(r"无|未见|未发现|否认|排除", context):
                fields["metastases"].append(site)
                break
    for m in re.finditer(r"(20\d{2}[./年-]\d{1,2}(?:[./月-]\d{1,2})?).{0,50}?(化疗|放疗|手术|治疗|用药|方案)", text):
        fields["treatment_timeline"].append({"date": m.group(1), "treatment": m.group(2), "evidence": text[max(0, m.start()-20):m.end()+80].replace("\n", " ")})
    for m in re.finditer(r"(?:一|二|三|四|五|1|2|3|4|5)线(?:治疗|用药)?", text):
        fields["treatment_lines"].append(m.group(0))
    for m in re.finditer(r"(?:停药|末次用药|治疗结束).{0,12}(\d+)\s*(天|日|周|个月|月)", text):
        fields["washout_periods"].append({"value": int(m.group(1)), "unit": m.group(2), "evidence": m.group(0)})
    for response in ["CR", "PR", "SD", "PD", "完全缓解", "部分缓解", "疾病稳定", "疾病进展"]:
        if re.search(r"(?:疗效|评效|最佳疗效).{0,10}" + re.escape(response), text, re.I):
            fields["response"].append(response)
    for m in re.finditer(r"(?:病灶|结节)[：:\s]*([^。；\n]{2,40}(?:mm|cm))", text, re.I):
        fields["lesions"].append(m.group(1).strip())
    for category, values in terms.items():
        for item in values:
            aliases = [item["name"], *item.get("aliases", [])]
            for alias in aliases:
                token = re.escape(alias)
                if re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*", alias):
                    token = r"(?<![A-Za-z])" + token + r"(?![A-Za-z0-9])"
                m = re.search(token, text, 0 if re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*", alias) else re.I)
                if m:
                    evidence = text[max(0, m.start()-80):m.end()+120].replace("\n", " ")
                    # labs 在后面按“指标+数值+单位”专门解析，不能把检验名称当作治疗。
                    target = "diagnosis" if category == "diseases" else "biomarkers" if category == "biomarkers" else "treatments" if category == "treatments" else None
                    if target is None:
                        continue
                    status = None
                    if target == "biomarkers":
                        window = text[m.start():m.end()+96]
                        status_window = text[m.start():m.end()+40]
                        low_expression = re.search(r"(?:HER[- ]?2|HER2).{0,24}?1\s*[+＋]", window, re.I)
                        status = "negative" if re.search(r"阴性|阴性表达|未见突变|\(-\)", status_window, re.I) else "low_positive" if low_expression else "positive" if re.search(r"阳性|\(\+\)|突变", status_window, re.I) else "unknown"
                        if item["name"] == "Ki-67":
                            # Ki-67 本质上是百分比指标，不能把邻近病理项目的 (-) 继承过来。
                            status = "unknown"
                    left = max(text.rfind("。", 0, m.start()), text.rfind("；", 0, m.start()), text.rfind("，", 0, m.start()))
                    right_candidates = [x for x in (text.find("。", m.end()), text.find("；", m.end()), text.find("，", m.end())) if x >= 0]
                    right = min(right_candidates) if right_candidates else len(text)
                    local_context = text[left + 1:right]
                    treatment_status = "current" if target == "treatments" and re.search(r"目前|当前|正在|开始", local_context) else "prior" if target == "treatments" and re.search(r"既往|曾用|曾经|历史", local_context) else None
                    fields[target].append({"name": item["name"], "status": status or treatment_status, "evidence": evidence})
                    break
    for item in terms.get("labs", []):
        aliases = [item["name"], *item.get("aliases", [])]
        alias_patterns = []
        for alias in aliases:
            token = re.escape(alias)
            if re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*", alias):
                token = r"(?<![A-Za-z])" + token + r"(?![A-Za-z0-9])"
            alias_patterns.append(token)
        unit = r"(?:×?\s*10[\^\"]?\d+\s*/\s*L|%|mg\s*/\s*dL|(?:μ|u)?mol\s*/\s*L|g\s*/\s*L|mmol\s*/\s*L)"
        pattern = r"(?:" + "|".join(alias_patterns) + r")[：:\s]*([0-9]+(?:\.[0-9]+)?)\s*(" + unit + r")"
        for m in re.finditer(pattern, text, re.I):
            fields["labs"].append({"name": item["name"], "value": float(m.group(1)), "unit": m.group(2), "evidence": m.group(0)})
    for key in ("diagnosis", "biomarkers", "treatments", "treatment_timeline", "response", "lesions", "labs", "metastases", "treatment_lines", "washout_periods"):
        seen = set(); unique = []
        for item in fields[key]:
            marker = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, dict) else str(item)
            if marker not in seen:
                seen.add(marker); unique.append(item)
        fields[key] = unique
    if fields["stage"]:
        fields["stage"] = re.sub(r"\s+", "", fields["stage"])
    return fields
