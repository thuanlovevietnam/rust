# Milestone Roadmap

**Document ID:** PFS-M0-D11  
**Title:** Milestone Roadmap  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§6, §13.4, §14, §18), PFS-M0-D03, PFS-M0-D08, PFS-M0-D12  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §6, §13.4, §18. This document defines milestone boundaries and dependencies; it does not approve any milestone. Only the decision authority marks a milestone Accepted.

## 1. Roadmap Overview (spec §6.1)

| Milestone | Name | Primary outcome | State | Depends on |
|---|---|---|---|---|
| M0 | Foundation Methodology | Establish the methodology | Proposed (this document set) | — |
| M1 | Documentation & Architecture Foundation | Documentation and architecture specifications | Not started | M0 Accepted |
| M2 | Universal Agent System | Multi-agent instruction system | Not started | M1 Accepted (see §4) |
| M3 | Validation & Quality Gates | Verification and governance controls | Not started | M1 Accepted (see §4) |
| M4 | Generator Automation | Rust automation engine | Not started | M2 + M3 Accepted (see §4) |

## 2. Milestone Specification Standard (spec §6.2)

Every milestone specification must contain:

1. Purpose 2. Scope 3. Non-goals 4. Dependencies 5. Functional requirements 6. Non-functional requirements (where applicable) 7. Architecture considerations 8. Deliverables 9. Acceptance criteria 10. Verification procedures 11. Risks 12. Exit criteria

M0 itself conforms: this document set covers 1–12 across D01–D12 (see PFS-M0-TRC-001).

## 3. Milestone States and Transitions (spec §6.3)

Proposed → Approved → In Progress → Under Review → Accepted (or Rejected / Superseded / Blocked).

Only an authorized decision authority may mark a milestone Accepted. AI and automation may never set state to Accepted (PFS-M0-D05 §4).

## 4. Boundaries and Dependencies

### M1 — Documentation & Architecture Foundation
- **Outcome:** Operational documentation and architecture specification system.
- **In scope (spec §18):** canonical repository structure; document taxonomy; document metadata schema; SPEC engineering standard; ADR/DR engineering standard; requirements traceability model; architecture specification framework; contract documentation; documentation versioning; cross-document consistency; documentation templates; documentation validation requirements.
- **Non-goals:** agent system implementation; gate automation code; Rust engine; project-specific templates beyond the generic documentation set.
- **Dependencies:** M0 Accepted. (Operationally usable immediately after M0; no M0 redesign required — spec §17.)
- **Exit:** M1 acceptance criteria pass; M2/M3 can be specified without revisiting M0.

### M2 — Universal Agent System
- **Outcome:** The multi-agent instruction system: AGENTS.md model, .agents/ structure, policies, skills, workflows, roles, capability registry, platform adapters.
- **In scope:** concrete policies; skill/workflow catalogs; registry schema; reference platform adapter(s).
- **Non-goals:** gate validation engine; Rust engine internals; provider lock-in (adapters only).
- **Dependencies:** M1 Accepted (templates, taxonomy, metadata schema needed for knowledge packs and registry). Soft dependency on M0 only; hard dependency on M1.

### M3 — Validation & Quality Gates
- **Outcome:** Executable verification: validation rules, gate definitions as enforceable checks, evidence model, integrity validators (docs, references, schemas), audit tooling support.
- **In scope:** rule catalog; check implementations (or their specification for M4 automation); evidence schemas; gate evaluation reports.
- **Non-goals:** repository scaffolding engine; AI provider adapters; GUI.
- **Dependencies:** M1 Accepted (validation targets defined there). Parallelizable with M2 (no hard dependency either way; both consume M1).

### M4 — Generator Automation
- **Outcome:** The Rust automation engine: project initialization, template processing, filesystem operations, metadata/schema/reference validation, manifest generation, deterministic checks, generation reports.
- **In scope:** Rust implementation per approved specs; CLI; template engine; manifest/version management; integration of M3 validation as automation.
- **Non-goals:** AI policy decisions; architecture approvals; changing M0–M3 semantics; covering every platform at launch.
- **Dependencies:** M2 and M3 Accepted (engine instantiates templates/registry and enforces gates). M4 does not start before both are approved.

### Dependency graph

```
M0 ──► M1 ──► M2 ──┐
         │         ├──► M4
         └──► M3 ──┘
```

## 5. M1 Scope Derivation (proving M0 sufficiency, spec §17)

| M1 subject (spec §18) | Derived from (M0) |
|---|---|
| 1. Canonical repository structure | D03 Stage 5; D06 §7 |
| 2. Document taxonomy | D06 §1 |
| 3. Document metadata schema | D06 §2 |
| 4. SPEC engineering standard | D04 (CP-02), D06 §3, D08 |
| 5. ADR/DR engineering standard | D04 §Decision States, D06 §4, D09 §4 |
| 6. Requirements traceability model | D06 §5, D03 Stage 2 |
| 7. Architecture specification framework | D04 CP-01, D09 §4 |
| 8. Contract documentation | D06 §4 (authoritative sources) |
| 9. Documentation versioning | D06 §8, D09 §5 |
| 10. Cross-document consistency | D06 §6, D08 (G5) |
| 11. Documentation templates | D05 §3, D06 §7 |
| 12. Documentation validation requirements | D06 §6, D08 §2 |

No M1 subject requires redesigning M0 principles; all derive from approved M0 content.

## 6. Deferred Technical Decisions (spec §13.4)

Deferred to post-M0 technical evaluation (earliest M4, some possibly M1–M3 with justification):

- CLI framework; async runtime; serialization framework; template engine; database selection; AI provider integration; MCP implementation; GUI framework; plugin architecture.

No technology dependency may be introduced without a documented justification and the change process (PFS-M0-D09). Rust as core-engine language is fixed by M0 (spec §13.1); everything else above is open.

## 7. M0 Non-Goals Restated (spec §14)

Not authorized by M0: Rust engine implementation; GUI; AI provider integrations; MCP servers; agent orchestration; complete generator; production app code; persistent database; every template; every AI platform.

## 8. Roadmap Governance

- Changing milestone boundaries or dependencies requires a change record and owner approval (PFS-M0-D09).
- If a milestone cannot proceed because a dependency is missing/unapproved: record it, identify impact, propose resolution, request approval (spec §6.4). Never assume.
- Superseding this roadmap requires the same rigor as any baseline change.

## 9. Traceability

AC-11 (Milestone Consistency), AC-12 (No Unapproved Technical Assumptions) — see PFS-M0-D12.
