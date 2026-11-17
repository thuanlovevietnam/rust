# Hybrid Execution Model

**Document ID:** PFS-M0-D05  
**Title:** Hybrid Execution Model  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§3.3, §7, §12), PFS-M0-D04, PFS-M0-D07, PFS-M0-D10  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §7 (and §3.3, §12). Conflicts resolve in favor of the spec.

## 1. Fundamental Separation (spec §7.1)

PFS combines two execution classes with disjoint responsibilities:

| Class | Responsibility | Character |
|---|---|---|
| AI (reasoning) | Contextual reasoning: discovery, analysis, design, drafting, audit | Variable, judgment-based, untrusted until verified |
| Rust automation (deterministic) | Repeatable, verifiable operations: generation, validation, manifests | Reproducible, schema-bound, evidence-producing |

Rule: **AI proposes, automation verifies and instantiates, authority approves.** No class may silently assume another's approval authority.

## 2. AI Responsibilities (spec §7.2)

AI agents may perform:

- Project discovery.
- Requirements analysis.
- Architecture exploration.
- Alternative evaluation.
- Document drafting.
- Risk identification.
- Skill selection.
- Workflow execution planning.
- Code review.
- Technical audit.

AI output is always **Proposed** quality (CP-03) and **untrusted until validated** (spec §12).

## 3. Automation Responsibilities (spec §7.3)

The Rust automation engine should perform:

- Directory creation.
- File generation from approved templates.
- Schema validation.
- Document metadata validation.
- Reference integrity checks.
- Registry generation.
- Version and manifest management.
- Template consistency checks.
- Deterministic quality checks.
- Generation reports.

Note: the engine is M4 scope. M0 fixes only its responsibilities and boundaries, not its implementation (spec §13.4, §14).

## 4. Approval Boundaries (spec §7.4)

Automation must not silently:

- Approve architecture decisions.
- Change project requirements.
- Upgrade document statuses.
- Override project policies.
- Delete authoritative documents.
- Change protected configurations.

Operations with governance impact require explicit authorization from the delegated decision authority. Authorization is recorded as evidence, not as a flag in generated output.

### 4.1. Boundary matrix

| Operation | AI | Automation | Authority |
|---|---|---|---|
| Draft a spec | May | Must not invent | — |
| Create directories/files from approved templates | May propose | May execute | Pre-authorized by template approval |
| Validate schema/metadata/references | May interpret failures | May execute | — |
| Approve a decision / baseline | Never | Never | Decision authority only |
| Upgrade document status | Never | Never (only report) | Decision authority only |
| Delete authoritative document | Never | Never | Decision authority via change process |
| Override security policy | Never | Never | Never (policies outrank tasks) |

## 5. AI Provider Independence (spec §7.5)

The methodology must not depend on a particular model or provider. Provider-specific integration is isolated in **adapters**.

The core system must not assume:

- One specific context format.
- One specific tool-calling interface.
- One specific subagent implementation.
- One specific AI model.
- One specific commercial provider.

Consequences:

- Agent system logic (PFS-M0-D07) is expressed platform-neutrally; platform adapters translate to concrete platforms (e.g., coding-agent CLIs, MCP hosts) without changing policy semantics.
- Swapping providers must not invalidate methodology artifacts; only adapter bindings change.

## 6. Trust Flow

```
Untrusted input (idea, imported template, third-party instruction, AI output)
        │
        ▼
AI analysis (Proposed artifacts) ──► Automation validation (schema, integrity, gates)
        │                                       │
        ▼                                       ▼
Decision authority review ◄──── evidence (reports, checks, audit)
        │
        ▼
Approved baseline (trusted)
```

Trust is granted only by authority approval backed by evidence — never by an agent's confidence or automation's silence.

## 7. Failure Handling

- AI produces an invalid artifact → automation/validation fails → artifact is rejected or repaired and re-validated; never approved by exception of silence.
- Automation detects integrity violation → gate fails; findings recorded; remediation required (PFS-M0-D08 §4).
- Governance conflict during generation → stop affected work; record; request decision (PFS-M0-D09 §4).

## 8. Traceability

AC-05 (Hybrid Execution), AC-06 (Agent Independence) — see PFS-M0-D12.
