import re

def parse_criteria(text: str, kind: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        line = line.strip(" -•\t")
        if line:
            rows.append({"kind": kind, "criterion": line})
    return rows

def evaluate(criteria: list[dict], case: dict) -> list[dict]:
    evidence_parts = []
    for group in case.values():
        if isinstance(group, list):
            for item in group:
                evidence_parts.append(item.get("evidence", "") if isinstance(item, dict) else str(item))
    haystack = " ".join(evidence_parts).lower()
    results = []
    for row in criteria:
        criterion = row["criterion"]
        time_rule = re.search(r"(?:停药|治疗结束|末次用药).{0,8}(?:至少|不少于|超过)?\s*(\d+)\s*(天|日|周|个月|月)", criterion)
        if time_rule:
            periods = case.get("washout_periods", [])
            if periods:
                actual = periods[0]["value"]
                unit = periods[0]["unit"]
                actual_days = actual * (30 if unit in {"月", "个月"} else 7 if unit == "周" else 1)
                target = int(time_rule.group(1)) * (30 if time_rule.group(2) in {"月", "个月"} else 7 if time_rule.group(2) == "周" else 1)
                passed = actual_days >= target
                results.append({**row, "status": "符合" if passed else "不符合", "evidence": f"已记录洗脱期{actual}{unit}"})
                continue
            results.append({**row, "status": "需人工核对", "evidence": "未找到明确停药或治疗结束日期"})
            continue
        if "且" in criterion or re.search(r"\bAND\b", criterion, re.I):
            parts = [p.strip() for p in re.split(r"且|\bAND\b", criterion, flags=re.I) if p.strip()]
            matched_parts = [p for p in parts if any(token.lower() in haystack for token in re.findall(r"[A-Za-z][A-Za-z0-9+.-]*|[\u4e00-\u9fff]{2,}", p))]
            if len(matched_parts) == len(parts):
                results.append({**row, "status": "不符合" if row["kind"] == "排除" else "符合", "evidence": "；".join(matched_parts)})
                continue
            if row["kind"] == "入组" and matched_parts:
                results.append({**row, "status": "需人工核对", "evidence": f"仅匹配：{'；'.join(matched_parts)}"})
                continue
        # Simple OR criteria are evaluated by alternatives independently.
        if "或" in criterion or re.search(r"\bOR\b", criterion, re.I):
            alternatives = re.split(r"或|\bOR\b", criterion, flags=re.I)
            matched_alt = [a.strip() for a in alternatives if a.strip() and any(token.lower() in haystack for token in re.findall(r"[A-Za-z][A-Za-z0-9+.-]*|[\u4e00-\u9fff]{2,}", a))]
            if matched_alt:
                results.append({**row, "status": "不符合" if row["kind"] == "排除" else "符合", "evidence": f"命中条件：{matched_alt[0]}"})
                continue
        numbers = re.findall(r"(?:≥|>=|不少于|不低于)\s*([0-9]+(?:\.[0-9]+)?)", criterion)
        age_match = re.search(r"年龄\s*(?:≥|>=|不少于|不低于)\s*(\d+)", criterion)
        if age_match and isinstance(case.get("age"), int):
            results.append({**row, "status": "符合" if case["age"] >= int(age_match.group(1)) else "不符合", "evidence": f"年龄{case['age']}岁"})
            continue
        lab_match = re.search(r"(血小板|PLT|血红蛋白|HGB|Hb|肌酐|Scr|Cr)\s*(?:≥|>=|不少于|不低于|≤|<=|不超过|低于)\s*([0-9]+(?:\.[0-9]+)?)", criterion, re.I)
        if lab_match:
            target_name = {"plt": "血小板", "hgb": "血红蛋白", "hb": "血红蛋白", "scr": "肌酐", "cr": "肌酐"}.get(lab_match.group(1).lower(), lab_match.group(1))
            labs = [x for x in case.get("labs", []) if x["name"] == target_name]
            if labs:
                actual = labs[0]["value"]; target = float(lab_match.group(2))
                op = "<=" if re.search(r"≤|<=|不超过|低于", criterion) else ">="
                passed = actual <= target if op == "<=" else actual >= target
                results.append({**row, "status": "符合" if passed else "不符合", "evidence": labs[0]["evidence"]})
                continue
        if "乳腺癌" in criterion and case.get("diagnosis"):
            results.append({**row, "status": "符合", "evidence": case["diagnosis"][0]["evidence"]})
            continue
        if "HER2" in criterion.upper():
            matches = [x for x in case.get("biomarkers", []) if x["name"].upper() == "HER2"]
            if matches and matches[0].get("status") in {"positive", "negative"}:
                results.append({**row, "status": "符合", "evidence": matches[0]["evidence"]})
                continue
        if row["kind"] == "排除" and re.search(r"(?:无|未见|未发现|否认)", criterion):
            target = re.sub(r"(?:无|未见|未发现|否认)", "", criterion).strip()
            if target and target not in haystack:
                results.append({**row, "status": "符合", "evidence": "病历中未发现该排除项"})
                continue
        matched = any(token.lower() in haystack for token in re.findall(r"[A-Za-z][A-Za-z0-9+.-]*|[\u4e00-\u9fff]{2,}", criterion))
        if matched and not numbers:
            status = "不符合" if row["kind"] == "排除" else "符合"
        else:
            status = "需人工核对"
        results.append({**row, "status": status, "evidence": "自动匹配到相关病历文本" if matched else "未找到明确证据"})
    return results
