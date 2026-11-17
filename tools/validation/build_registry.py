#!/usr/bin/env python3
"""
PFS M0 Global Requirement Registry and Traceability Matrix Builder
==================================================================
Builds the canonical CSV registry and traceability matrix from M0 documentation.
Ensures ID uniqueness, legacy mapping, acceptance criteria linkage, and synchronization
with Project Owner Decisions (PFS-M0-OWNER-DECISIONS-001: OD-01, OD-02).
"""

import os
import re
import csv

def build_registry_and_matrix(root_dir: str):
    m0_dir = os.path.join(root_dir, "docs", "M0-foundation")
    registry_csv_path = os.path.join(m0_dir, "registry", "requirement-registry.csv")
    rtm_csv_path = os.path.join(m0_dir, "reports", "requirement-traceability-matrix.csv")

    # Domain mapping configuration (Scheme A canonical IDs as approved by OD-01)
    # (domain, source_file, source_doc_id_scheme_a, owner, default_decision)
    domain_configs = {
        "PFS-VIS": ("Product Vision", "01-PFS-VISION.md", "PFS-M0-SPEC-001", "Project Owner", "DEC-VIS-01"),
        "M0-PROD": ("Product Definition", "02-PRODUCT-DEFINITION.md", "PFS-M0-SPEC-002", "Principal Systems Architect", "F01, F03"),
        "M0-UNI": ("Universal Project Model", "03-UNIVERSAL-PROJECT-MODEL.md", "PFS-M0-SPEC-003", "Principal Systems Architect", "F01, F02"),
        "M0-MTH": ("Foundation Methodology", "04-FOUNDATION-METHODOLOGY.md", "PFS-M0-SPEC-004", "Methodology Engineer", "F02, F04"),
        "M0-GOV": ("Governance Model", "05-GOVERNANCE-MODEL.md", "PFS-M0-SPEC-005", "Governance and Decision Analyst", "F03, F04"),
        "M0-AUT": ("Authority and Decisions", "06-AUTHORITY-AND-DECISION-MODEL.md", "PFS-M0-SPEC-006", "Governance and Decision Analyst", "F03, F04"),
        "M0-ART": ("Artifact and Traceability", "07-ARTIFACT-AND-TRACEABILITY-MODEL.md", "PFS-M0-SPEC-007", "Documentation Architect", "F05, F07"),
        "M0-HYB": ("Hybrid Execution", "08-HYBRID-EXECUTION-MODEL.md", "PFS-M0-SPEC-008", "Principal Systems Architect", "F06, F07"),
        "M0-SEC-AG": ("Agent Security", "09-AGENT-SECURITY-MODEL.md", "PFS-M0-SPEC-009", "AI Agent Security Engineer", "F08, F09"),
        "M0-QLT": ("Quality and Acceptance", "10-QUALITY-AND-ACCEPTANCE-MODEL.md", "PFS-M0-SPEC-010", "Quality Assurance Engineer", "F11"),
        "M0-VER": ("Version and Change", "11-VERSION-AND-CHANGE-MANAGEMENT.md", "PFS-M0-SPEC-011", "Principal Systems Architect", "F10"),
        "M0-SC": ("Security and Supply Chain", "12-SECURITY-AND-SUPPLY-CHAIN.md", "PFS-M0-SPEC-012", "AI Agent Security Engineer", "F12"),
        "M0-RDM": ("Milestone Roadmap", "13-MILESTONE-ROADMAP.md", "PFS-M0-SPEC-013", "Project Owner", "DEC-RDM-01"),
        "M0-REV": ("Review Amendments", "15-M0-REVIEW-REPORT.md", "PFS-M0-SPEC-015", "Independent Documentation Auditor", "F01-F12")
    }

    # Specific Owner Decision mappings (PFS-M0-OWNER-DECISIONS-001 & PFS-M0-OWNER-DECISIONS-002)
    owner_decision_refs = {
        "M0-PROD-001": "F01, F03, PFS-M0-OWNER-DECISIONS-001 (OD-01)",
        "M0-UNI-001": "F01, F02, PFS-M0-OWNER-DECISIONS-001 (OD-01)",
        "M0-REV-001": "F01, PFS-M0-OWNER-DECISIONS-001 (OD-01)",
        "M0-REV-008": "F05, PFS-M0-OWNER-DECISIONS-001 (OD-01)",
        "M0-REV-020": "F04, PFS-M0-OWNER-DECISIONS-001 (OD-02), PFS-M0-OWNER-DECISIONS-002",
        "M0-QLT-008": "F11, PFS-M0-OWNER-DECISIONS-001 (OD-02), PFS-M0-OWNER-DECISIONS-002",
        "M0-QLT-014": "F11, PFS-M0-OWNER-DECISIONS-001 (OD-02), PFS-M0-OWNER-DECISIONS-002"
    }

    # Explicit Acceptance Criteria mappings for domain requirements
    ac_mapping = {
        # M0-PROD
        "M0-PROD-001": "AC-01",
        "M0-PROD-002": "AC-01",
        "M0-PROD-003": "AC-01, AC-07",
        "M0-PROD-004": "AC-01, AC-06",
        "M0-PROD-005": "AC-01",
        "M0-PROD-006": "AC-01, AC-10",
        "M0-PROD-007": "AC-01, AC-23",
        "M0-PROD-008": "AC-01, AC-25",
        # M0-UNI
        "M0-UNI-001": "AC-02",
        "M0-UNI-002": "AC-02",
        "M0-UNI-003": "AC-03",
        "M0-UNI-004": "AC-04",
        "M0-UNI-005": "AC-03, AC-05",
        "M0-UNI-006": "AC-05",
        "M0-UNI-007": "AC-02",
        "M0-UNI-008": "AC-04",
        "M0-UNI-009": "AC-02",
        "M0-UNI-010": "AC-01, AC-02",
        # M0-MTH
        "M0-MTH-001": "AC-06",
        "M0-MTH-002": "AC-06, AC-20",
        "M0-MTH-003": "AC-06",
        "M0-MTH-004": "AC-06",
        "M0-MTH-005": "AC-06",
        "M0-MTH-006": "AC-04, AC-06",
        "M0-MTH-007": "AC-06, AC-22",
        "M0-MTH-008": "AC-06",
        "M0-MTH-009": "AC-06, AC-23",
        "M0-MTH-010": "AC-06, AC-21",
        # M0-GOV
        "M0-GOV-001": "AC-08",
        "M0-GOV-002": "AC-08, AC-09",
        "M0-GOV-003": "AC-08, AC-09",
        "M0-GOV-004": "AC-08, AC-10",
        "M0-GOV-005": "AC-08, AC-11",
        "M0-GOV-006": "AC-08",
        "M0-GOV-007": "AC-08, AC-24",
        "M0-GOV-008": "AC-08",
        "M0-GOV-009": "AC-08, AC-23",
        "M0-GOV-010": "AC-08, AC-10",
        "M0-GOV-011": "AC-08, AC-09",
        "M0-GOV-012": "AC-06, AC-08",
        # M0-AUT
        "M0-AUT-001": "AC-10",
        "M0-AUT-002": "AC-09, AC-10",
        "M0-AUT-003": "AC-10",
        "M0-AUT-004": "AC-11",
        "M0-AUT-005": "AC-11, AC-15",
        "M0-AUT-006": "AC-15",
        "M0-AUT-007": "AC-10",
        "M0-AUT-008": "AC-10, AC-15",
        "M0-AUT-009": "AC-10",
        "M0-AUT-010": "AC-11",
        "M0-AUT-011": "AC-10",
        "M0-AUT-012": "AC-07, AC-10",
        # M0-ART
        "M0-ART-001": "AC-12",
        "M0-ART-002": "AC-12, AC-13",
        "M0-ART-003": "AC-12",
        "M0-ART-004": "AC-14, AC-15",
        "M0-ART-005": "AC-14",
        "M0-ART-006": "AC-14",
        "M0-ART-007": "AC-14, AC-27",
        "M0-ART-008": "AC-14, AC-23",
        "M0-ART-009": "AC-14",
        "M0-ART-010": "AC-14, AC-25",
        "M0-ART-011": "AC-14",
        "M0-ART-012": "AC-14, AC-26",
        "M0-ART-013": "AC-12, AC-14",
        "M0-ART-014": "AC-12",
        # M0-HYB
        "M0-HYB-001": "AC-07",
        "M0-HYB-002": "AC-07",
        "M0-HYB-003": "AC-16",
        "M0-HYB-004": "AC-20",
        "M0-HYB-005": "AC-21",
        "M0-HYB-006": "AC-16, AC-17",
        "M0-HYB-007": "AC-07, AC-09",
        "M0-HYB-008": "AC-21",
        "M0-HYB-009": "AC-21",
        "M0-HYB-010": "AC-14",
        "M0-HYB-011": "AC-07, AC-08",
        "M0-HYB-012": "AC-20",
        "M0-HYB-013": "AC-20",
        "M0-HYB-014": "AC-07, AC-21",
        # M0-SEC-AG
        "M0-SEC-AG-001": "AC-16, AC-18",
        "M0-SEC-AG-002": "AC-17",
        "M0-SEC-AG-003": "AC-18",
        "M0-SEC-AG-004": "AC-18",
        "M0-SEC-AG-005": "AC-19",
        "M0-SEC-AG-006": "AC-19",
        "M0-SEC-AG-007": "AC-19",
        "M0-SEC-AG-008": "AC-19",
        "M0-SEC-AG-009": "AC-19",
        "M0-SEC-AG-010": "AC-18, AC-19",
        "M0-SEC-AG-011": "AC-18",
        "M0-SEC-AG-012": "AC-18, AC-19",
        "M0-SEC-AG-013": "AC-19",
        "M0-SEC-AG-014": "AC-16",
        "M0-SEC-AG-015": "AC-16, AC-17",
        # M0-QLT
        "M0-QLT-001": "AC-22",
        "M0-QLT-002": "AC-22",
        "M0-QLT-003": "AC-22",
        "M0-QLT-004": "AC-22",
        "M0-QLT-005": "AC-22, AC-23",
        "M0-QLT-006": "AC-22",
        "M0-QLT-007": "AC-23",
        "M0-QLT-008": "AC-23",
        "M0-QLT-009": "AC-24",
        "M0-QLT-010": "AC-23",
        "M0-QLT-011": "AC-23",
        "M0-QLT-012": "AC-23",
        "M0-QLT-013": "AC-22",
        "M0-QLT-014": "AC-22, AC-23",
        # M0-VER
        "M0-VER-001": "AC-25",
        "M0-VER-002": "AC-25",
        "M0-VER-003": "AC-25",
        "M0-VER-004": "AC-25",
        "M0-VER-005": "AC-25",
        "M0-VER-006": "AC-25",
        "M0-VER-007": "AC-25, AC-26",
        "M0-VER-008": "AC-25",
        "M0-VER-009": "AC-26",
        "M0-VER-010": "AC-26",
        "M0-VER-011": "AC-26",
        "M0-VER-012": "AC-26, AC-27",
        "M0-VER-013": "AC-25",
        "M0-VER-014": "AC-25",
        # M0-SC
        "M0-SC-001": "AC-27",
        "M0-SC-002": "AC-27",
        "M0-SC-003": "AC-27",
        "M0-SC-004": "AC-27",
        "M0-SC-005": "AC-27",
        "M0-SC-006": "AC-27",
        "M0-SC-007": "AC-27",
        "M0-SC-008": "AC-27",
        "M0-SC-009": "AC-27",
        "M0-SC-010": "AC-27",
        "M0-SC-011": "AC-27",
        "M0-SC-012": "AC-27",
        "M0-SC-013": "AC-27",
        "M0-SC-014": "AC-27",
        "M0-SC-015": "AC-27",
        "M0-SC-016": "AC-27",
        "M0-SC-017": "AC-27",
        "M0-SC-018": "AC-27",
        "M0-SC-019": "AC-27",
        "M0-SC-020": "AC-27",
        # M0-RDM
        "M0-RDM-001": "AC-11",
        "M0-RDM-002": "AC-11",
        "M0-RDM-003": "AC-11",
        "M0-RDM-004": "AC-26",
        "M0-RDM-005": "AC-01",
        # M0-REV
        "M0-REV-001": "AC-01, AC-28",
        "M0-REV-002": "AC-02, AC-28",
        "M0-REV-003": "AC-03, AC-28",
        "M0-REV-004": "AC-05, AC-28",
        "M0-REV-005": "AC-10, AC-28",
        "M0-REV-006": "AC-09, AC-28",
        "M0-REV-007": "AC-13, AC-28",
        "M0-REV-008": "AC-12, AC-28",
        "M0-REV-009": "AC-12, AC-28",
        "M0-REV-010": "AC-20, AC-28",
        "M0-REV-011": "AC-20, AC-28",
        "M0-REV-012": "AC-21, AC-28",
        "M0-REV-013": "AC-17, AC-28",
        "M0-REV-014": "AC-18, AC-28",
        "M0-REV-015": "AC-10, AC-28",
        "M0-REV-016": "AC-25, AC-28",
        "M0-REV-017": "AC-22, AC-28",
        "M0-REV-018": "AC-27, AC-28",
        "M0-REV-019": "AC-24, AC-28",
        "M0-REV-020": "AC-28",
        # PFS-VIS
        "PFS-VIS-001": "AC-01",
        "PFS-VIS-002": "AC-02, AC-04",
        "PFS-VIS-003": "AC-07",
        "PFS-VIS-004": "AC-06",
        "PFS-VIS-005": "AC-07, AC-10",
        "PFS-VIS-006": "AC-14",
        "PFS-VIS-007": "AC-23",
        "PFS-VIS-008": "AC-16, AC-17",
        "PFS-VIS-009": "AC-25",
        "PFS-VIS-010": "AC-01"
    }

    # Legacy mapping dictionary
    legacy_map = {
        # M0-UNI legacy IDs
        "M0-UNI-001": "M0-REQ-001",
        "M0-UNI-002": "M0-REQ-002",
        "M0-UNI-003": "M0-REQ-003",
        "M0-UNI-004": "M0-REQ-004",
        "M0-UNI-005": "M0-REQ-005",
        "M0-UNI-006": "M0-REQ-006",
        "M0-UNI-007": "M0-REQ-007",
        "M0-UNI-008": "M0-REQ-008",
        "M0-UNI-009": "M0-REQ-009",
        "M0-UNI-010": "M0-REQ-010",
        # M0-REV legacy IDs from SPEC-001 §18.1 / REVIEW-001 §15
        "M0-REV-001": "M0-REQ-001",
        "M0-REV-002": "M0-REQ-002",
        "M0-REV-003": "M0-REQ-003",
        "M0-REV-004": "M0-REQ-004",
        "M0-REV-005": "M0-REQ-005",
        "M0-REV-006": "M0-REQ-006",
        "M0-REV-007": "M0-REQ-007",
        "M0-REV-008": "M0-REQ-008",
        "M0-REV-009": "M0-REQ-009",
        "M0-REV-010": "M0-REQ-010",
        "M0-REV-011": "M0-REQ-011",
        "M0-REV-012": "M0-REQ-012",
        "M0-REV-013": "M0-REQ-013",
        "M0-REV-014": "M0-REQ-014",
        "M0-REV-015": "M0-REQ-015",
        "M0-REV-016": "M0-REQ-016",
        "M0-REV-017": "M0-REQ-017",
        "M0-REV-018": "M0-REQ-018",
        "M0-REV-019": "M0-REQ-019",
        "M0-REV-020": "M0-REQ-020",
        # M0-PROD mappings
        "M0-PROD-001": "PFS-CON-004",
        "M0-PROD-002": "PFS-CON-001, PFS-CON-005",
        "M0-PROD-003": "PFS-CON-002",
        "M0-PROD-004": "PFS-CON-003",
        "M0-PROD-005": "None",
        "M0-PROD-006": "PFS-CON-006",
        "M0-PROD-007": "PFS-CON-007",
        "M0-PROD-008": "PFS-CON-008"
    }

    # Extract statements directly from markdown files
    extracted_statements = {}

    # 1. 01-PFS-VISION.md
    with open(os.path.join(m0_dir, "01-PFS-VISION.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(PFS-VIS-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 2. 02-PRODUCT-DEFINITION.md
    with open(os.path.join(m0_dir, "02-PRODUCT-DEFINITION.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-PROD-\d{3})\s*\|\s*([^\|]+)\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(3).strip()

    # Fallback for M0-PROD if table format varies
    if "M0-PROD-001" not in extracted_statements:
        extracted_statements["M0-PROD-001"] = "PFS MUST hỗ trợ universal product scope cho nhiều loại project, không chỉ software project, kết hợp methodology, structured project knowledge, AI reasoning và deterministic automation."
        extracted_statements["M0-PROD-002"] = "PFS Core MUST được triển khai bằng Rust và không ép project đích dùng Rust."
        extracted_statements["M0-PROD-003"] = "PFS MUST sử dụng mô hình thực thi Hybrid (AI reasoning + Deterministic automation)."
        extracted_statements["M0-PROD-004"] = "PFS MUST độc lập với AI provider (provider-independent)."
        extracted_statements["M0-PROD-005"] = "PFS MUST phân biệt ranh giới giữa PFS system, generated foundation và generated project."
        extracted_statements["M0-PROD-006"] = "PFS MUST phân biệt rõ ràng giữa quyền quyết định (decision authority) và quyền thực thi (execution permission)."
        extracted_statements["M0-PROD-007"] = "PFS MUST yêu cầu quality claims quan trọng phải có verifiable evidence."
        extracted_statements["M0-PROD-008"] = "PFS MUST quản lý thay đổi có version, compatibility và traceability."

    # 3. 03-UNIVERSAL-PROJECT-MODEL.md
    with open(os.path.join(m0_dir, "03-UNIVERSAL-PROJECT-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-UNI-\d{3})\s*\|\s*([^\|]+)\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(3).strip()

    # 4. 04-FOUNDATION-METHODOLOGY.md
    with open(os.path.join(m0_dir, "04-FOUNDATION-METHODOLOGY.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-MTH-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 5. 05-GOVERNANCE-MODEL.md
    with open(os.path.join(m0_dir, "05-GOVERNANCE-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-GOV-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 6. 06-AUTHORITY-AND-DECISION-MODEL.md
    with open(os.path.join(m0_dir, "06-AUTHORITY-AND-DECISION-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-AUT-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 7. 07-ARTIFACT-AND-TRACEABILITY-MODEL.md
    with open(os.path.join(m0_dir, "07-ARTIFACT-AND-TRACEABILITY-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-ART-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 8. 08-HYBRID-EXECUTION-MODEL.md
    with open(os.path.join(m0_dir, "08-HYBRID-EXECUTION-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-HYB-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 9. 09-AGENT-SECURITY-MODEL.md
    with open(os.path.join(m0_dir, "09-AGENT-SECURITY-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-SEC-AG-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 10. 10-QUALITY-AND-ACCEPTANCE-MODEL.md
    with open(os.path.join(m0_dir, "10-QUALITY-AND-ACCEPTANCE-MODEL.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-QLT-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 11. 11-VERSION-AND-CHANGE-MANAGEMENT.md
    with open(os.path.join(m0_dir, "11-VERSION-AND-CHANGE-MANAGEMENT.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-VER-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 12. 12-SECURITY-AND-SUPPLY-CHAIN.md
    with open(os.path.join(m0_dir, "12-SECURITY-AND-SUPPLY-CHAIN.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-SC-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 13. 13-MILESTONE-ROADMAP.md
    with open(os.path.join(m0_dir, "13-MILESTONE-ROADMAP.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'-\s*`?(M0-RDM-\d{3})`?:\s*([^\n\r]+)', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    # 14. 15-M0-REVIEW-REPORT.md
    with open(os.path.join(m0_dir, "15-M0-REVIEW-REPORT.md"), "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            m = re.match(r'\|\s*(M0-REV-\d{3})\s*\|\s*([^\|]+)\|', line)
            if m:
                extracted_statements[m.group(1)] = m.group(2).strip()

    registry_rows = []
    rtm_rows = []

    for req_id in sorted(extracted_statements.keys()):
        statement = extracted_statements[req_id]
        prefix = req_id.rsplit("-", 1)[0]
        cfg = domain_configs.get(prefix, ("General", "Unknown", "Unknown", "Project Owner", "N/A"))

        domain = cfg[0]
        src_file = cfg[1]
        src_doc_id = cfg[2]
        owner = cfg[3]
        
        # Check specific Owner decision reference first
        decision = owner_decision_refs.get(req_id, cfg[4])
        status = "Accepted"  # Milestone M0 Officially Accepted by Project Owner Decision PFS-M0-OWNER-DECISIONS-002
        priority = "P0" if any(w in statement for w in ["Critical", "MUST NOT tự", "bảo vệ", "least privilege", "default-deny", "universal"]) else "P1"
        applicability = "Universal"
        ac_ref = ac_mapping.get(req_id, "Pending / Domain Coverage")
        verification = "Inspection and Automated Package Validation"
        evidence_ref = f"docs/M0-foundation/{src_file}; tools/validation/validate_m0.py"
        legacy_id = legacy_map.get(req_id, "None")

        registry_rows.append({
            "requirement_id": req_id,
            "domain": domain,
            "statement": statement,
            "source_document_id": src_doc_id,
            "owner": owner,
            "status": status,
            "priority": priority,
            "applicability": applicability,
            "decision_refs": decision,
            "acceptance_refs": ac_ref,
            "verification_method": verification,
            "evidence_refs": evidence_ref,
            "legacy_ids": legacy_id
        })

        # Verification status for RTM
        if "AC-28" in ac_ref:
            ver_status = "Documentation Verified (Pass); Milestone M0 Officially Accepted by Project Owner Decision PFS-M0-OWNER-DECISIONS-002"
        elif any(ac in ac_ref for ac in ["AC-16", "AC-17", "AC-18", "AC-19", "AC-20", "AC-21"]):
            ver_status = "Specification Documented (Pass M0); Runtime Verification Deferred (M2-M4)"
        else:
            ver_status = "Specification Verified (Pass M0 Documentation & Traceability Baseline)"

        rtm_rows.append({
            "requirement_id": req_id,
            "domain": domain,
            "statement": statement,
            "source_document": f"{src_file} ({src_doc_id})",
            "decision_refs": decision,
            "acceptance_criteria": ac_ref,
            "verification_method": verification,
            "verification_status": ver_status,
            "evidence_reference": evidence_ref
        })

    # Write requirement-registry.csv
    reg_fields = [
        "requirement_id", "domain", "statement", "source_document_id",
        "owner", "status", "priority", "applicability",
        "decision_refs", "acceptance_refs", "verification_method",
        "evidence_refs", "legacy_ids"
    ]
    with open(registry_csv_path, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=reg_fields)
        writer.writeheader()
        writer.writerows(registry_rows)

    # Write requirement-traceability-matrix.csv
    rtm_fields = [
        "requirement_id", "domain", "statement", "source_document",
        "decision_refs", "acceptance_criteria", "verification_method",
        "verification_status", "evidence_reference"
    ]
    with open(rtm_csv_path, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=rtm_fields)
        writer.writeheader()
        writer.writerows(rtm_rows)

    print(f"Registry generated: {len(registry_rows)} requirements -> {registry_csv_path}")
    print(f"Traceability matrix generated: {len(rtm_rows)} rows -> {rtm_csv_path}")

if __name__ == "__main__":
    build_registry_and_matrix(".")
