# Documentation Governance Model

**Document ID:** PFS-M0-D06  
**Title:** Documentation Governance Model  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§8), PFS-M0-D04 (CP-02), PFS-M0-D08 (G5), PFS-M0-D09  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §8. Conflicts resolve in favor of the spec. M1 (Documentation & Architecture Foundation) operationalizes this model; M0 fixes the rules only.

## 1. Documentation Categories (spec §8.1)

1. Foundation
2. Requirements
3. Architecture
4. Specifications
5. Decisions
6. Contracts
7. Development
8. Operations
9. Quality
10. Governance

Every authoritative document belongs to exactly one primary category. Categories are used for indexing, ownership and review routing — not as permission to duplicate content across categories.

## 2. Document Metadata (spec §8.2)

Every authoritative document should support:

| Field | Required | Notes |
|---|---|---|
| Document ID | Yes | Stable, unique (e.g., PFS-M0-D06) |
| Title | Yes | Human-readable |
| Version | Yes | Document version, distinct from PFS/template/foundation versions |
| Status | Yes | One of §3 |
| Owner | Yes | Accountable role or person |
| Created date | Yes | ISO 8601 |
| Updated date | Yes | ISO 8601 |
| Related documents | Yes | References only; no redefinition |
| Approval reference | If Approved | Record ID of approval evidence |

## 3. Document Status (spec §8.3)

Allowed statuses:

- **Draft** — incomplete; may contain placeholders.
- **Proposed** — complete enough for review; not binding.
- **In Review** — under review by the decision authority.
- **Approved** — authoritative and binding.
- **Deprecated** — no longer current; retained.
- **Superseded** — replaced by a newer document; retained and linked.

Rule: **A document being generated does not imply that it is approved.** Status transitions are governance acts (PFS-M0-D05 §4): only the decision authority approves, deprecates or supersedes.

## 4. Authoritative Source Table (CP-02)

| Information | Authoritative source |
|---|---|
| Project objectives | Project Charter |
| Functional requirements | Requirements Specification |
| Architecture | Architecture Specification |
| Architecture decisions | ADR/DR |
| API contracts | Contract specifications |
| Agent policies | Agent policy documents |
| Implementation status | Project tracking records |
| Acceptance evidence | Validation records |

Other documents may reference these; redefinition is an integrity violation.

## 5. Traceability Chain (spec §8.4)

Requirements → Architecture → Decisions → Specifications → Implementation → Tests → Acceptance Evidence

The system must be able to identify:

- Requirements without implementation plans.
- Architecture decisions without supporting requirements.
- Specifications without acceptance criteria.
- Implementation changes without corresponding decisions where required.
- Tests that do not verify declared requirements.

M1 defines the concrete traceability model (RTM structure, link types, cardinality). M0 mandates capability, not format.

## 6. Documentation Integrity (spec §8.5)

The system must detect:

- Duplicate authoritative definitions.
- Broken internal references.
- Missing required metadata.
- Invalid document statuses.
- Missing approval references (status Approved without approval record).
- Conflicting versions.
- Unresolved mandatory dependencies.

Integrity checks are automation responsibilities (PFS-M0-D05 §3) executed by deterministic validators; results are evidence for G5 (PFS-M0-D08).

## 7. Index and Relationships

The Documentation Index is the registry of authoritative documents: ID, title, category, version, status, owner, path. Relationships are expressed as references from documents; the index is generated/checked by automation, not maintained by hand, once M4 lands.

## 8. Versioning (spec §11.4)

Distinct, non-interchangeable versions:

- PFS version (the methodology system itself)
- Template version
- Generated foundation version
- Document version (this table's Version field)
- Architecture baseline version

Rules: version increments per SemVer-like intent (major = breaking methodology change, minor = additive, patch = editorial); Superseded documents keep their final version and link to the superseding document.

## 9. Governance Rules

1. No authoritative document is deleted; it is Deprecated or Superseded.
2. Every document has exactly one accountable owner.
3. Every cross-document reference uses document IDs, not bare filenames.
4. Approval requires the approval reference field to point at an Approval Record.
5. Conflicts between documents are resolved by authority per the change process — never by silently editing the lower-precedence document to match.

## 10. Traceability

AC-04 (Single Source of Truth), AC-07 (partly), AC-09 — see PFS-M0-D12. M1 scope derives from §1, §2, §5, §6, §8 (see PFS-M0-D11 §5).
