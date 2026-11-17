# M0 Traceability Matrix

**Document ID:** PFS-M0-TRC-001  
**Title:** M0 Requirements Traceability Matrix  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001, PFS-M0-D01…PFS-M0-D12  
**Approval reference:** None — awaiting owner approval  

Maps PFS-M0-SPEC-001 requirements and acceptance criteria to the M0 deliverables, and confirms each mandatory deliverable exists.

## 1. Spec Section → Deliverable

| Spec § | Subject | Deliverable(s) |
|---|---|---|
| §1 | Purpose / objective / mission / philosophy | D01 |
| §2 | Product definition / universal scope | D01, D02 |
| §3 | System boundaries; separation of concerns | D02, D05 |
| §4 | Core system principles | D04 |
| §5 | Project Foundation Lifecycle (Stages 0–10) | D03 |
| §6 | Milestone governance | D11 |
| §7 | Hybrid execution model | D05 |
| §8 | Universal documentation model | D06 |
| §9 | Universal agent system model | D07 |
| §10 | Quality and acceptance model | D08 |
| §11 | Change management; version management | D09 |
| §12 | Security and trust principles | D10 |
| §13 | Technology direction; deferred decisions | D11 §6; D01 §6 |
| §14 | M0 non-goals | D11 §7 |
| §15 | M0 deliverables D01–D12 | this set (see §3 below) |
| §16 | M0 acceptance criteria AC-01…AC-12 | D12 §3 |
| §17 | M0 exit conditions | D12 §4 |
| §18 | M1 scope | D11 §5 |
| §19 | Governing rule | README; D09 |

## 2. Acceptance Criterion → Evidence Documents

| AC | Criterion | Primary evidence | Secondary |
|---|---|---|---|
| AC-01 | Product clarity | D01, D02 | SPEC §1–3 |
| AC-02 | Lifecycle completeness | D03 | D08 (gates map 1:1), TRC §1 |
| AC-03 | Decision governance | D04 §Decision States | D06 §3, D09 |
| AC-04 | Single source of truth | D04 CP-02; D06 §4, §6 | SPEC §4.2, §8.5 |
| AC-05 | Hybrid execution | D05 | D07, D10 |
| AC-06 | Agent independence | D07; D05 §5 | SPEC §7.5, §9 |
| AC-07 | Quality model | D08 | D06 §5–6 |
| AC-08 | Evidence model | D08 §5 | D04 CP-05; SPEC §10.3 |
| AC-09 | Change governance | D09 | D06 §8; D04 CP-07 |
| AC-10 | Security principles | D10 | D05 §4; D07 §2, §9; SPEC §12 |
| AC-11 | Milestone consistency | D11 | TRC §1 (§6, §18) |
| AC-12 | No unapproved technical assumptions | D11 §6 | SPEC §13.4; D01 §6 |

## 3. Mandatory Deliverables (spec §15) — Existence Check

| ID | Deliverable | Required | File | Exists |
|---|---|---|---|---|
| M0-D01 | PFS Vision and Product Definition | Yes | docs/m0/PFS-M0-D01-vision-and-product-definition.md | Yes |
| M0-D02 | Universal Scope Definition | Yes | docs/m0/PFS-M0-D02-universal-scope-definition.md | Yes |
| M0-D03 | Foundation Lifecycle | Yes | docs/m0/PFS-M0-D03-foundation-lifecycle.md | Yes |
| M0-D04 | Core Principles | Yes | docs/m0/PFS-M0-D04-core-principles.md | Yes |
| M0-D05 | Hybrid Execution Model | Yes | docs/m0/PFS-M0-D05-hybrid-execution-model.md | Yes |
| M0-D06 | Documentation Governance Model | Yes | docs/m0/PFS-M0-D06-documentation-governance-model.md | Yes |
| M0-D07 | Agent System Concept | Yes | docs/m0/PFS-M0-D07-agent-system-concept.md | Yes |
| M0-D08 | Quality Gate Model | Yes | docs/m0/PFS-M0-D08-quality-gate-model.md | Yes |
| M0-D09 | Change Management Model | Yes | docs/m0/PFS-M0-D09-change-management-model.md | Yes |
| M0-D10 | Security and Trust Principles | Yes | docs/m0/PFS-M0-D10-security-and-trust-principles.md | Yes |
| M0-D11 | Milestone Roadmap | Yes | docs/m0/PFS-M0-D11-milestone-roadmap.md | Yes |
| M0-D12 | M0 Acceptance Report | Yes | docs/m0/PFS-M0-D12-m0-acceptance-report.md | Yes |

Auxiliary (non-deliverable) documents: TRC-001 (this file), docs/index.md, README.md, docs/specs/PFS-M0-SPEC-001.md.

## 4. Criteria Not Verifiable by Documentation Alone

| Item | Why | Status |
|---|---|---|
| Terminology consistency sweep | Requires independent read-through | Pending (see D12 OI-02) |
| No unresolved critical contradictions | Requires independent review | Pending (see D12 OI-02) |
| Independent review performed | Review must be independent of author | Not performed |
| Owner approval of M0 | Authority decision | Outstanding |

## 5. Versioning Note

All documents at version 1.0.0 with status Proposed (D12: Draft). Approval of the M0 baseline will pin versions in the Baseline Manifest at Stage 10 of the PFS self-application (or an equivalent M0-close record).
