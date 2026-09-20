from src.medical_screening.rules import parse_criteria, evaluate
from src.medical_screening.extraction import extract_case
from src.medical_screening.studies import save_study, load_study

def test_criteria_evaluation_has_review_state():
    criteria = parse_criteria("EGFR突变阳性\n年龄≥18岁", "入组")
    case = {"biomarkers": [{"name": "EGFR", "evidence": "EGFR突变阳性"}], "diagnosis": []}
    result = evaluate(criteria, case)
    assert result[0]["status"] == "符合"
    assert result[1]["status"] == "需人工核对"

def test_extracts_common_oncology_fields():
    case = extract_case({"text": "女，68岁，右乳浸润性导管癌（IV期），伴骨、肝转移，HER-2阴性。"})
    assert case["age"] == 68
    assert case["sex"] == "女"
    assert case["stage"] == "IV期"
    assert "骨" in case["metastases"]
    assert "脑" not in case["metastases"]
    assert case["biomarkers"][0]["status"] == "negative"

def test_numeric_lab_rule():
    case = extract_case({"text": "血小板：125 ×10^9/L"})
    result = evaluate(parse_criteria("血小板≥100", "入组"), case)
    assert result[0]["status"] == "符合"

def test_rule_engine_accepts_string_lists():
    result = evaluate(parse_criteria("脑转移", "排除"), {"metastases": ["肝"]})
    assert result[0]["status"] in {"符合", "需人工核对"}

def test_study_round_trip(tmp_path, monkeypatch):
    import src.medical_screening.studies as studies
    monkeypatch.setattr(studies, "STUDY_DIR", tmp_path)
    save_study("测试研究", "年龄≥18岁", "活动性感染", "1.1")
    loaded = load_study("测试研究")
    assert loaded["version"] == "1.1"
    assert loaded["inclusion"] == "年龄≥18岁"

def test_extracts_timeline_and_response():
    case = extract_case({"text": "2026.7开始治疗，最佳疗效PR。可测量病灶：肝脏病灶16mm。"})
    assert case["response"] == ["PR"]
    assert case["treatment_timeline"]
    assert case["lesions"]

def test_extracts_treatment_status_and_washout():
    case = extract_case({"text": "既往使用奥希替尼，停药3个月。目前开始铂类化疗，二线治疗。"})
    assert case["treatments"]
    assert any(x["status"] == "prior" for x in case["treatments"])
    assert case["washout_periods"][0]["value"] == 3
    assert case["treatment_lines"] == ["二线治疗"]

def test_exclusion_hit_is_not_eligible():
    case = {"diagnosis": [{"name": "活动性感染", "evidence": "存在活动性感染"}]}
    result = evaluate(parse_criteria("活动性感染", "排除"), case)
    assert result[0]["status"] == "不符合"

def test_and_rule_requires_all_parts():
    case = {"diagnosis": [{"name": "乳腺癌", "evidence": "乳腺癌"}], "biomarkers": [{"name": "HER2", "evidence": "HER2阴性"}]}
    result = evaluate(parse_criteria("乳腺癌且HER2", "入组"), case)
    assert result[0]["status"] == "符合"

def test_washout_rule():
    case = {"washout_periods": [{"value": 3, "unit": "个月", "evidence": "停药3个月"}]}
    result = evaluate(parse_criteria("停药至少2个月", "入组"), case)
    assert result[0]["status"] == "符合"

def test_extracts_reference_date():
    case = extract_case({"text": "2024年3月确诊，2026.07复查。"})
    assert case["reference_date"] == "2026-07"

def test_filters_metric_false_positives_and_normalizes_units():
    case = extract_case({"text": "eGFR 81.48 mL/min，肌酐66.6 umol/L，CR5/6(-)，HER-2（1+）。"})
    assert not any(x["name"] == "EGFR" for x in case["biomarkers"])
    assert any(x["name"] == "肌酐" and x["value"] == 66.6 for x in case["labs"])
    assert not any(x["value"] == 5.0 for x in case["labs"])
    assert any(x["name"] == "HER2" and x["status"] == "low_positive" for x in case["biomarkers"])
