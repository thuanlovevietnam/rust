# Project Foundation System (PFS)

PFS is a reusable system for designing, establishing, validating and governing the foundations of new projects — combining a foundation methodology, structured project knowledge, AI-assisted engineering and deterministic (Rust) validation into one coherent system.

**Current milestone:** M0 — Foundation Methodology — **v1.1.0, ACCEPTED (Approved by Project Owner via [PFS-M0-OWNER-DECISIONS-002](file:///C:/Users/OK259/rust/docs/M0-foundation/decisions/PFS-M0-OWNER-DECISIONS-002.md))**
**Next milestone:** M1 — Documentation & Architecture Foundation (Authorized to start; dependency on M0 unblocked)

## Repository Layout

```
docs/
  specs/PFS-M0-SPEC-001.md        Parent spec — v1.1.0 (authority for M0)
  specs/PFS-M0-REVIEW-001.md      Independent review & mandatory amendment spec (F01–F12)
  M0-foundation/                  M0 documentation package (00-M0-INDEX … 15-M0-REVIEW-REPORT)
  archive/m0-v1.0.0/              Superseded v1.0.0 spec and D01–D12 deliverables (history)
  index.md                        Documentation index (authoritative registry)
```

## Reading Order

1. `docs/specs/PFS-M0-SPEC-001.md` (v1.1.0) — the authority.
2. `docs/specs/PFS-M0-REVIEW-001.md` — what changed and why.
3. `docs/M0-foundation/00-M0-INDEX.md` — package registry and v1.0.0 → v1.1.0 mapping.
4. Package files 01–15 in order; `14-M0-ACCEPTANCE-CRITERIA.md` for the AC-01..28 catalog; `15-M0-REVIEW-REPORT.md` for disposition and open items.

## Status and Governance

- Milestone M0 v1.1.0 has been **Approved and Accepted** by the Project Owner via [PFS-M0-OWNER-DECISIONS-002](file:///C:/Users/OK259/rust/docs/M0-foundation/decisions/PFS-M0-OWNER-DECISIONS-002.md).
- PFS-M0-SPEC-001 v1.0.0 was independently reviewed (PFS-M0-REVIEW-001); findings F01–F12 were mandatory amendments, now incorporated and verified in v1.1.0. All 28 acceptance criteria were assessed (20 Pass including owner acceptance gate, 8 deferred to runtime milestones M2–M4).
- **M0 does not authorize implementation of the Rust engine** (SPEC-001 §19, §21; deferred to M2–M4).
- Changes follow the change management model (11-VERSION-AND-CHANGE-MANAGEMENT.md); AI-generated content is Proposed at best; only the authorized decision authority approves.

## Working on This Repository

- SPEC-001 is read-only except through the change process; package files must not redefine it normatively.
- Keep document IDs, statuses and cross-references consistent (integrity rules: 07-ARTIFACT-AND-TRACEABILITY-MODEL.md §7).
- M1 work must comply with SPEC-001 v1.1.0 and the M1 dependency list (13-MILESTONE-ROADMAP.md §3).
