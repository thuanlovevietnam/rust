# Core Principles

**Document ID:** PFS-M0-D04  
**Title:** Core Principles  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§4), PFS-M0-D05, PFS-M0-D06, PFS-M0-D08, PFS-M0-D09, PFS-M0-D10  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §4. Principles are assigned stable identifiers (CP-xx) for traceability; identifiers are additive and never reused. Conflicts resolve in favor of the spec.

## Principles

### CP-01 — Requirements-Driven Architecture (spec §4.1)
Architecture must be derived from validated requirements, constraints and risks.

AI agents must not select architectural patterns because they are familiar or popular. Every important architectural decision must have an identifiable justification, traceable to requirements, constraints or risks.

**Check:** every architecture decision in the Decision Register references at least one requirement, constraint or risk identifier.

### CP-02 — Single Source of Truth (spec §4.2)
Every important project concept has one authoritative location. Other files may reference but must not silently redefine it.

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

**Check:** duplicate authoritative definitions are detected by documentation integrity validation (PFS-M0-D06 §6).

### CP-03 — Explicit Decision Ownership (spec §4.3)
AI agents may analyze, recommend, compare alternatives, draft specifications, identify risks and propose changes. Only an authorized project owner or delegated decision authority may approve decisions requiring owner approval.

AI-generated content must not automatically become an approved decision.

**Check:** approval references exist for every Approved decision; absence of approval reference = Not Approved (PFS-M0-D08, PFS-M0-D10 §5).

### CP-04 — Progressive Disclosure (spec §4.4)
Information is organized so agents load only what the current task needs.

The system must avoid excessively large instruction files, unnecessary context loading, repeated knowledge across documents, conflicting rules and unstructured prompt collections.

**Check:** agent-facing instructions follow the hierarchy and precedence policy (PFS-M0-D07 §3); knowledge is layered, not duplicated.

### CP-05 — Evidence-Based Validation (spec §4.5)
A task cannot be marked verified because an agent reports success.

Verification references observable evidence: test results, build results, static analysis, schema validation, architecture checks, document consistency checks, human approval records.

**Check:** every "verified" claim links to an evidence artifact (PFS-M0-D08 §5).

### CP-06 — Reproducibility (spec §4.6)
Given the same project inputs, approved decisions, template versions, configuration and generator version, PFS should produce equivalent structural outputs.

AI-generated reasoning may vary; deterministic generation and validation must be reproducible.

**Check:** generation and validation are deterministic; variance is confined to AI reasoning steps, never to manifests, schemas or integrity results.

### CP-07 — Controlled Evolution (spec §4.7)
The foundation must support change without losing historical decisions or traceability. Architecture changes follow an explicit change process (PFS-M0-D09).

**Check:** the change process was followed; superseded artifacts remain traceable (PFS-M0-D09).

## Decision States (supports CP-03)

| State | Meaning | Who sets it |
|---|---|---|
| Proposed | Drafted, not approved | Any authorized contributor / AI |
| In Review | Under owner/authority review | Decision authority |
| Approved | Authoritative; binding | Authorized decision authority only |
| Superseded | Replaced by a newer approved decision | Decision authority, via change process |
| Deprecated | No longer applicable, retained for history | Decision authority |
| Rejected | Reviewed and not accepted | Decision authority |

AI may only ever produce **Proposed** content. Transitions beyond Proposed require the authorized authority.

## Principle Hierarchy in Conflicts

When principles appear to conflict, resolve in this order:

1. Security and trust principles (PFS-M0-D10) — never overridden.
2. Explicit decision ownership and approval boundaries.
3. Single source of truth and controlled evolution.
4. Evidence-based validation and reproducibility.
5. Progressive disclosure and requirements-driven architecture.

Any unresolved conflict is an M0 exit-condition blocker ("no unresolved critical contradictions remain") and is recorded in PFS-M0-D12.

## Traceability

CP-01..CP-07 → PFS-M0-SPEC-001 §4.1..§4.7 → AC-03, AC-04, AC-05, AC-08 (PFS-M0-D12).
