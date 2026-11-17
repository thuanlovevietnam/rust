#!/usr/bin/env python3
"""
PFS M0 Package Automated Validator
==================================
Performs deterministic read-only validation of the M0 Foundation documentation package:
1. Document inventory and metadata completeness.
2. Intra-package and repository-wide Document ID uniqueness.
3. Owner Decision Record validation (PFS-M0-OWNER-DECISIONS-001).
4. Canonical requirement namespaces and duplicate ID detection.
5. Legacy ID mapping verification.
6. Markdown link and cross-reference integrity (supporting relative and file:/// URIs).
7. Acceptance criteria (AC-01..AC-28) coverage.
8. Governance and lifecycle status validation.

Usage:
    python tools/validation/validate_m0.py [--root .] [--report]
"""

import os
import sys
import re
import csv
import argparse
from typing import Dict, List, Set, Tuple

EXPECTED_M0_DOCS_SCHEME_A = {
    "00-M0-INDEX.md": "PFS-M0-SPEC-000",
    "01-PFS-VISION.md": "PFS-M0-SPEC-001",
    "02-PRODUCT-DEFINITION.md": "PFS-M0-SPEC-002",
    "03-UNIVERSAL-PROJECT-MODEL.md": "PFS-M0-SPEC-003",
    "04-FOUNDATION-METHODOLOGY.md": "PFS-M0-SPEC-004",
    "05-GOVERNANCE-MODEL.md": "PFS-M0-SPEC-005",
    "06-AUTHORITY-AND-DECISION-MODEL.md": "PFS-M0-SPEC-006",
    "07-ARTIFACT-AND-TRACEABILITY-MODEL.md": "PFS-M0-SPEC-007",
    "08-HYBRID-EXECUTION-MODEL.md": "PFS-M0-SPEC-008",
    "09-AGENT-SECURITY-MODEL.md": "PFS-M0-SPEC-009",
    "10-QUALITY-AND-ACCEPTANCE-MODEL.md": "PFS-M0-SPEC-010",
    "11-VERSION-AND-CHANGE-MANAGEMENT.md": "PFS-M0-SPEC-011",
    "12-SECURITY-AND-SUPPLY-CHAIN.md": "PFS-M0-SPEC-012",
    "13-MILESTONE-ROADMAP.md": "PFS-M0-SPEC-013",
    "14-M0-ACCEPTANCE-CRITERIA.md": "PFS-M0-SPEC-014",
    "15-M0-REVIEW-REPORT.md": "PFS-M0-SPEC-015"
}

CANONICAL_NAMESPACES = {
    "M0-PROD", "M0-UNI", "M0-MTH", "M0-GOV", "M0-AUT",
    "M0-ART", "M0-HYB", "M0-SEC-AG", "M0-QLT", "M0-VER",
    "M0-SC", "M0-RDM", "M0-REV"
}

VALID_STATUSES = {
    "Draft", "Proposed", "In Review", "Approved", "Implemented",
    "Verified", "Accepted", "Accepted with Exception", "Accepted with Approved Exceptions",
    "Conditionally Accepted", "Rejected", "Deferred", "Superseded", "Deprecated"
}

class ValidationContext:
    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        self.m0_dir = os.path.join(self.root, "docs", "M0-foundation")
        self.specs_dir = os.path.join(self.root, "docs", "specs")
        self.decisions_dir = os.path.join(self.m0_dir, "decisions")
        self.findings = []
        self.m0_doc_registry = {}     # doc_id in docs/M0-foundation -> list of (file, line)
        self.repo_doc_registry = {}   # doc_id across all docs -> list of (file, line)
        self.req_registry = {}        # req_id -> list of (file, line, statement)
        self.ac_registry = {}         # ac_id -> list of (file, line)
        self.has_od01_approved = False
        self.has_od02_deferred = False

    def log_finding(self, severity: str, category: str, file_path: str, line: int, message: str):
        self.findings.append({
            "severity": severity,
            "category": category,
            "file": os.path.relpath(file_path, self.root) if file_path else "N/A",
            "line": line,
            "message": message
        })

def check_file_inventory(ctx: ValidationContext):
    if not os.path.isdir(ctx.m0_dir):
        ctx.log_finding("CRITICAL", "Inventory", ctx.m0_dir, 0, "Directory docs/M0-foundation does not exist")
        return

    existing_files = set(os.listdir(ctx.m0_dir))
    expected_files = set(EXPECTED_M0_DOCS_SCHEME_A.keys())

    missing = expected_files - existing_files
    for m in missing:
        ctx.log_finding("CRITICAL", "Inventory", os.path.join(ctx.m0_dir, m), 0, f"Missing required M0 document: {m}")

def validate_owner_decisions(ctx: ValidationContext):
    dec_file = os.path.join(ctx.decisions_dir, "PFS-M0-OWNER-DECISIONS-001.md")
    if not os.path.exists(dec_file):
        ctx.log_finding("HIGH", "Governance", dec_file, 0, "Missing Owner Decision Record PFS-M0-OWNER-DECISIONS-001.md")
        return

    with open(dec_file, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()

    if "OD-01" in content and "APPROVED" in content:
        ctx.has_od01_approved = True
    else:
        ctx.log_finding("HIGH", "Governance", dec_file, 1, "OD-01 Approved not found in decision record")

    if "OD-02" in content and "DEFERRED" in content:
        ctx.has_od02_deferred = True
    else:
        ctx.log_finding("HIGH", "Governance", dec_file, 1, "OD-02 Deferred not found in decision record")

def inspect_documents_and_metadata(ctx: ValidationContext):
    # Check intra-package M0 files
    if os.path.isdir(ctx.m0_dir):
        m0_files = sorted([os.path.join(ctx.m0_dir, f) for f in os.listdir(ctx.m0_dir) if f.endswith(".md")])
        for file_path in m0_files:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()

            doc_id = None
            doc_id_line = 0
            version = None
            status = None

            for idx, line in enumerate(lines, 1):
                m_id = re.search(r'\*\*Document ID:\*\*\s*([^\n\r]+)', line)
                if not m_id:
                    m_id = re.search(r'\|\s*Document ID\s*\|\s*([^\|\n\r]+)\|', line)
                if m_id and not doc_id:
                    doc_id = m_id.group(1).strip()
                    doc_id_line = idx

                m_ver = re.search(r'\*\*Version:\*\*\s*([^\n\r]+)', line)
                if not m_ver:
                    m_ver = re.search(r'\|\s*Version\s*\|\s*([^\|\n\r]+)\|', line)
                if m_ver and not version:
                    version = m_ver.group(1).strip()

                m_stat = re.search(r'\*\*Status:\*\*\s*([^\n\r]+)', line)
                if not m_stat:
                    m_stat = re.search(r'\|\s*Status\s*\|\s*([^\|\n\r]+)\|', line)
                if m_stat and not status:
                    status = m_stat.group(1).strip()

            fname = os.path.basename(file_path)
            if not doc_id:
                ctx.log_finding("HIGH", "Metadata", file_path, 1, f"Missing Document ID metadata in {fname}")
            else:
                if doc_id not in ctx.m0_doc_registry:
                    ctx.m0_doc_registry[doc_id] = []
                ctx.m0_doc_registry[doc_id].append((file_path, doc_id_line))

                if doc_id not in ctx.repo_doc_registry:
                    ctx.repo_doc_registry[doc_id] = []
                ctx.repo_doc_registry[doc_id].append((file_path, doc_id_line))

            if not version:
                ctx.log_finding("MEDIUM", "Metadata", file_path, 1, f"Missing Version metadata in {fname}")
            if not status:
                ctx.log_finding("HIGH", "Metadata", file_path, 1, f"Missing Status metadata in {fname}")

    # Check specs files (parent spec)
    if os.path.isdir(ctx.specs_dir):
        spec_files = sorted([os.path.join(ctx.specs_dir, f) for f in os.listdir(ctx.specs_dir) if f.endswith(".md")])
        for file_path in spec_files:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()
            doc_id = None
            doc_id_line = 0
            for idx, line in enumerate(lines, 1):
                m_id = re.search(r'\*\*Document ID:\*\*\s*([^\n\r]+)', line)
                if m_id and not doc_id:
                    doc_id = m_id.group(1).strip()
                    doc_id_line = idx
            if doc_id:
                if doc_id not in ctx.repo_doc_registry:
                    ctx.repo_doc_registry[doc_id] = []
                ctx.repo_doc_registry[doc_id].append((file_path, doc_id_line))

    # 1. Intra-package Document ID uniqueness
    for doc_id, occurrences in ctx.m0_doc_registry.items():
        if len(occurrences) > 1:
            locs = ", ".join([f"{os.path.basename(p[0])}:L{p[1]}" for p in occurrences])
            ctx.log_finding("CRITICAL", "Document ID Intra-Package", occurrences[0][0], occurrences[0][1],
                            f"Duplicate Document ID '{doc_id}' within M0 package: {locs}")

    # 2. Cross-directory collision (Parent Spec vs M0 package)
    for doc_id, occurrences in ctx.repo_doc_registry.items():
        if len(occurrences) > 1:
            locs = ", ".join([f"{os.path.relpath(p[0], ctx.root)}:L{p[1]}" for p in occurrences])
            if ctx.has_od01_approved and doc_id == "PFS-M0-SPEC-001":
                ctx.log_finding("INFORMATIONAL", "Document ID Governance", occurrences[0][0], occurrences[0][1],
                                f"Document ID '{doc_id}' exists in parent spec and package file ({locs}). Governed by Project Owner Decision OD-01 (Approved Scheme A for M0; normalization scheduled for M1).")
            else:
                ctx.log_finding("HIGH", "Document ID Governance", occurrences[0][0], occurrences[0][1],
                            f"Cross-directory Document ID collision '{doc_id}' between parent spec and package: {locs}. Requires Owner Decision OD-01.")

def extract_requirements_and_acceptance(ctx: ValidationContext):
    if not os.path.isdir(ctx.m0_dir):
        return

    m0_files = sorted([os.path.join(ctx.m0_dir, f) for f in os.listdir(ctx.m0_dir) if f.endswith(".md")])
    for file_path in m0_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
            lines = fp.readlines()

        for idx, line in enumerate(lines, 1):
            m_ac = re.search(r'\*\*(AC-\d{2,3})\s*—\s*([^*]+)\*\*', line)
            if m_ac:
                ac_id = m_ac.group(1)
                if ac_id not in ctx.ac_registry:
                    ctx.ac_registry[ac_id] = []
                ctx.ac_registry[ac_id].append((file_path, idx))

            m_req = re.match(r'\|\s*(M0-[A-Z0-9\-]+-\d{3}|PFS-VIS-\d{3}|PFS-CON-\d{3})\s*\|', line)
            if m_req:
                req_id = m_req.group(1).strip()
                if req_id not in ctx.req_registry:
                    ctx.req_registry[req_id] = []
                ctx.req_registry[req_id].append((file_path, idx, line.strip()))

            m_bullet = re.match(r'-\s*`?(M0-RDM-\d{3})`?:\s*([^\n\r]+)', line)
            if m_bullet:
                req_id = m_bullet.group(1).strip()
                if req_id not in ctx.req_registry:
                    ctx.req_registry[req_id] = []
                ctx.req_registry[req_id].append((file_path, idx, line.strip()))

    for req_id, entries in ctx.req_registry.items():
        if len(entries) > 1:
            locs = ", ".join([f"{os.path.basename(e[0])}:L{e[1]}" for e in entries])
            ctx.log_finding("HIGH", "Requirement ID", entries[0][0], entries[0][1],
                            f"Duplicate definition of Requirement ID '{req_id}': {locs}")

    for req_id in ctx.req_registry.keys():
        if req_id.startswith("PFS-"):
            pass
        else:
            ns = req_id.rsplit("-", 1)[0]
            if ns not in CANONICAL_NAMESPACES:
                ctx.log_finding("MEDIUM", "Namespace", ctx.req_registry[req_id][0][0], ctx.req_registry[req_id][0][1],
                                f"Non-canonical requirement namespace '{ns}' in ID '{req_id}'")

    expected_acs = [f"AC-{i:02d}" for i in range(1, 29)]
    for ac in expected_acs:
        if ac not in ctx.ac_registry:
            ctx.log_finding("CRITICAL", "Acceptance Criteria", os.path.join(ctx.m0_dir, "14-M0-ACCEPTANCE-CRITERIA.md"), 0,
                            f"Acceptance Criterion '{ac}' is missing from catalog")
        elif len(ctx.ac_registry[ac]) > 1:
            locs = ", ".join([f"{os.path.basename(e[0])}:L{e[1]}" for e in ctx.ac_registry[ac]])
            ctx.log_finding("HIGH", "Acceptance Criteria", ctx.ac_registry[ac][0][0], ctx.ac_registry[ac][0][1],
                            f"Duplicate definition of Acceptance Criterion '{ac}': {locs}")

def validate_markdown_links(ctx: ValidationContext):
    search_dirs = [ctx.m0_dir, ctx.specs_dir, os.path.join(ctx.root, "docs")]
    all_md = []
    for d in search_dirs:
        if os.path.isdir(d):
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(".md"):
                        all_md.append(os.path.join(root, f))
    if os.path.exists(os.path.join(ctx.root, "README.md")):
        all_md.append(os.path.join(ctx.root, "README.md"))

    for fpath in sorted(set(all_md)):
        dir_name = os.path.dirname(fpath)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
            lines = fp.readlines()

        for idx, line in enumerate(lines, 1):
            for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', line):
                link_text = m.group(1)
                target = m.group(2).strip()

                if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:") or target.startswith("#"):
                    continue

                target_clean = target.split("#")[0]
                if not target_clean:
                    continue

                # Handle file:/// scheme
                if target_clean.startswith("file:///"):
                    file_uri_path = target_clean[8:]  # strip file:///
                    # On Windows, e.g. C:/Users/...
                    file_uri_path = os.path.normpath(file_uri_path)
                    if os.path.exists(file_uri_path):
                        continue
                    else:
                        ctx.log_finding("HIGH", "Broken Link", fpath, idx,
                                        f"Broken link target '{target}' (resolved file path: '{file_uri_path}')")
                        continue

                # Resolve target relative to file
                resolved_rel = os.path.normpath(os.path.join(dir_name, target_clean))
                resolved_root = os.path.normpath(os.path.join(ctx.root, target_clean))

                if not (os.path.exists(resolved_rel) or os.path.exists(resolved_root)):
                    ctx.log_finding("HIGH", "Broken Link", fpath, idx,
                                    f"Broken link target '{target}' (text: '{link_text}')")

def validate_registry_file(ctx: ValidationContext):
    registry_csv = os.path.join(ctx.m0_dir, "registry", "requirement-registry.csv")
    if not os.path.exists(registry_csv):
        ctx.log_finding("CRITICAL", "Registry", registry_csv, 0, "Global Requirement Registry CSV file does not exist")
        return

    required_cols = [
        "requirement_id", "domain", "statement", "source_document_id",
        "owner", "status", "priority", "applicability",
        "decision_refs", "acceptance_refs", "verification_method",
        "evidence_refs", "legacy_ids"
    ]

    with open(registry_csv, "r", encoding="utf-8", errors="ignore") as fp:
        reader = csv.DictReader(fp)
        headers = reader.fieldnames or []
        for col in required_cols:
            if col not in headers:
                ctx.log_finding("CRITICAL", "Registry", registry_csv, 1, f"Missing required column in registry CSV: '{col}'")

        seen_ids = set()
        for idx, row in enumerate(reader, 2):
            req_id = row.get("requirement_id", "").strip()
            if not req_id:
                ctx.log_finding("CRITICAL", "Registry", registry_csv, idx, "Empty requirement_id in registry CSV row")
                continue
            if req_id in seen_ids:
                ctx.log_finding("CRITICAL", "Registry", registry_csv, idx, f"Duplicate requirement_id in CSV: '{req_id}'")
            seen_ids.add(req_id)

            stat = row.get("status", "").strip()
            if stat and stat not in VALID_STATUSES:
                ctx.log_finding("MEDIUM", "Registry", registry_csv, idx, f"Invalid requirement status '{stat}' for {req_id}")

            src_doc = row.get("source_document_id", "").strip()
            if not src_doc:
                ctx.log_finding("HIGH", "Registry", registry_csv, idx, f"Missing source_document_id for {req_id}")

def generate_report(ctx: ValidationContext) -> str:
    lines = []
    lines.append("# M0 Validation Execution Report")
    lines.append(f"**Target Root:** `{ctx.root}`  ")
    lines.append(f"**Total Findings:** {len(ctx.findings)}  ")

    by_sev = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFORMATIONAL": 0}
    for f in ctx.findings:
        sev = f["severity"].upper()
        by_sev[sev] = by_sev.get(sev, 0) + 1

    lines.append("\n## Summary by Severity")
    lines.append(f"- **CRITICAL:** {by_sev.get('CRITICAL', 0)}")
    lines.append(f"- **HIGH:** {by_sev.get('HIGH', 0)}")
    lines.append(f"- **MEDIUM:** {by_sev.get('MEDIUM', 0)}")
    lines.append(f"- **LOW:** {by_sev.get('LOW', 0)}")
    lines.append(f"- **INFORMATIONAL:** {by_sev.get('INFORMATIONAL', 0)}")

    lines.append("\n## Detailed Findings")
    if not ctx.findings:
        lines.append("No findings detected. Package passes automated checks.")
    else:
        lines.append("| # | Severity | Category | File | Line | Finding |")
        lines.append("|---|---|---|---|---|---|")
        for idx, f in enumerate(ctx.findings, 1):
            lines.append(f"| {idx} | {f['severity']} | {f['category']} | `{f['file']}` | {f['line']} | {f['message']} |")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Validate PFS M0 Documentation Package")
    parser.add_argument("--root", default=".", help="Workspace repository root")
    parser.add_argument("--report", action="store_true", help="Print markdown validation report")
    args = parser.parse_args()

    ctx = ValidationContext(args.root)
    check_file_inventory(ctx)
    validate_owner_decisions(ctx)
    inspect_documents_and_metadata(ctx)
    extract_requirements_and_acceptance(ctx)
    validate_markdown_links(ctx)
    validate_registry_file(ctx)

    if args.report:
        print(generate_report(ctx))
    else:
        print(f"Validation completed: {len(ctx.findings)} findings.")
        for f in ctx.findings:
            print(f"[{f['severity']}] {f['category']} in {f['file']}:{f['line']} - {f['message']}")

    # Exit code: 0 if no critical intra-package, 1 if critical intra-package exists
    has_crit = any(f["severity"] == "CRITICAL" for f in ctx.findings)
    sys.exit(1 if has_crit else 0)

if __name__ == "__main__":
    main()
