# Quality Gate Model

**Document ID:** PFS-M0-D08  
**Title:** Quality Gate Model  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§10), PFS-M0-D03 (lifecycle), PFS-M0-D06, PFS-M0-D09, PFS-M0-D12  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §10. Gate definitions here are the methodology-level contract; concrete validation rules and evidence formats are M1/M3 scope (spec §18; roadmap in PFS-M0-D11). Conflicts resolve in favor of the spec.

## 1. Quality Dimensions (spec §10.1)

PFS must evaluate:

| # | Dimension | Question |
|---|---|---|
| QD-01 | Completeness | Are all required deliverables present? |
| QD-02 | Consistency | Do artifacts agree with each other? |
| QD-03 | Traceability | Is the chain Requirements→…→Acceptance Evidence navigable? |
| QD-04 | Correctness | Do artifacts meet their declared criteria? |
| QD-05 | Security | Are trust boundaries and least-privilege rules honored? |
| QD-06 | Maintainability | Can the foundation evolve without loss of control? |
| QD-07 | Reproducibility | Are deterministic outputs reproducible? |
| QD-08 | Portability | Is the methodology provider- and language-independent? |
| QD-09 | Extensibility | Can categories, templates and adapters be added safely? |
| QD-10 | Verifiability | Can every claim be evidenced? |

## 2. Gate Contract (spec §10.2)

Every gate defines six elements:

1. **Entry conditions** — what must hold before the gate is evaluated.
2. **Required deliverables** — the artifacts under assessment.
3. **Validation rules** — how artifacts are checked.
4. **Required evidence** — what must be produced and retained.
5. **Approval authority** — who may pass the gate.
6. **Exit conditions** — what is true after a pass.

Rules:

- A failed gate remains failed until findings are resolved or formally accepted as exceptions by an authorized authority. Exceptions are recorded, time-bounded where possible, and never silent.
- Gates are independent: passing G_n does not waive G_{n+1}.
- Approval authority may not be the same agent that produced the deliverables for G9 (Independent Audit) — independence is mandatory (PFS-M0-SPEC-001 §10.4).

## 3. The Eleven Gates

| Gate | Name | Entry condition | Required deliverables | Approval authority |
|---|---|---|---|---|
| G0 | Initialization | Project workspace requested | Identity; profile; workspace record | Decision authority |
| G1 | Project Definition | G0 passed | Charter; Scope Definition; Stakeholder Map; Risk Register | Decision authority |
| G2 | Requirements | G1 passed | Requirements Spec; RTM; Acceptance Criteria; Baseline Proposal | Decision authority |
| G3 | Architecture | G2 passed | Architecture Spec; Diagrams; Dependency Map; ADRs | Decision authority |
| G4 | Governance | G3 passed | Governance Spec; Decision Register; Change Mgmt Rules | Decision authority |
| G5 | Documentation | G4 passed | Doc structure; Templates; Index; Traceability structure; integrity report | Decision authority |
| G6 | Agent Foundation | G5 passed | AGENTS.md; .agents/; Capability Registry; platform specs | Decision authority |
| G7 | Quality Foundation | G6 passed | Quality Spec; Validation Rules; Test Strategy; Gate Definitions | Decision authority |
| G8 | Bootstrap | G7 passed | Repository; build config; test infrastructure; Bootstrap Report | Decision authority |
| G9 | Independent Audit | G8 passed | Audit Report; Findings Register; Remediation Plan | Independent auditor (authorized) |
| G10 | Baseline Approval | G9 passed, findings resolved/accepted | Baseline Manifest; Approval Record; Readiness Status | Decision authority (owner) |

## 4. Failure Handling

1. Findings are registered with severity: Critical / Major / Minor / Observation.
2. Critical findings block the gate unconditionally. Major findings block unless formally accepted as exceptions by the authority with recorded rationale. Minor/Observation do not block but are tracked.
3. Re-evaluation requires new evidence; prior failures remain in history.
4. Exceptions are revisited at the next gate; an expired exception re-fails the gate.

## 5. Evidence Model (spec §10.3)

| Claim | Required evidence |
|---|---|
| Build succeeds | Build output and exit status |
| Tests pass | Test report |
| Architecture is compliant | Architecture validation results |
| Documents are complete | Document validation report |
| Decisions are approved | Approval records |
| Agent understands project | Independent clean-room assessment |

Evidence requirements:

- Evidence is distinguishable from claims — an agent's summary is neither.
- Evidence artifacts are retained, referenceable and versioned with the baseline manifest.
- Every gate decision cites its evidence IDs.

## 6. Independent Audit (spec §10.4)

- The auditor must be independent of the producing agent/process wherever practical.
- The auditor does not repeat the implementation agent's conclusions; it re-derives findings from artifacts and evidence.
- Audit output feeds G9 only after findings are dispositioned in the Findings Register.

## 7. Gate-to-Lifecycle Mapping

See PFS-M0-D03 §3. Each lifecycle stage exits through exactly one gate; gates G0–G10 map one-to-one to Stages 0–10.

## 8. Traceability

AC-07 (Quality Model), AC-08 (Evidence Model) — see PFS-M0-D12. Detailed validation rules and gate automation are M3 scope.
