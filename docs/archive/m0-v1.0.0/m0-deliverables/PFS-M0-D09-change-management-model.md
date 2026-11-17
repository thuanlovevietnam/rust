# Change Management Model

**Document ID:** PFS-M0-D09  
**Title:** Change Management Model  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§11), PFS-M0-D04, PFS-M0-D06 §8, PFS-M0-D08  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §11. Conflicts resolve in favor of the spec.

## 1. Change Classification (spec §11.1)

| Class | Description | Typical authority |
|---|---|---|
| Documentation change | Content/format of a document | Documentation owner; authority if authoritative |
| Requirement change | Add/modify/remove requirements | Decision authority |
| Architecture change | Change to boundaries, modules, decisions, contracts | Decision authority |
| Security change | Change affecting trust boundaries, policies | Decision authority + security review |
| Agent policy change | Change to policies/instruction hierarchy | Decision authority |
| Template change | Change to artifact templates | Template owner; authority if approved set |
| Generator change | Change to PFS engine/automation behavior | PFS maintainers; authority for behavior affecting gates |
| Baseline change | Change to approved foundation baseline | Decision authority (owner) |

Every change is assigned exactly one primary class; cross-cutting changes list all affected classes.

## 2. Change Process (spec §11.2)

1. Identify the change.
2. Record the reason.
3. Identify affected requirements.
4. Identify affected documents.
5. Evaluate impact and risk.
6. Propose a solution.
7. Obtain required approval.
8. Implement the change.
9. Run validation.
10. Record the result.

Artifacts: a Change Record captures steps 1–6; an approval reference captures 7; validation evidence captures 9; the Decision Register / baseline manifest capture 10. Undocumented changes do not exist — if it isn't recorded, it didn't happen.

## 3. Impact Analysis Minimums

Before approval, the Change Record must state:

- Affected requirement IDs and whether acceptance criteria change.
- Affected documents (IDs) and whether any becomes Superseded/Deprecated.
- Affected gates requiring re-validation.
- Affected baselines and versions (PFS / template / foundation / document / architecture baseline).
- Risk rating and rollback plan.

## 4. Architecture Change Protection (spec §11.3)

An AI agent must **never** silently redefine an approved architecture.

When a conflict is discovered:

1. **Stop** the affected implementation.
2. **Record** the conflict (what, where, which approved decision it contradicts).
3. **Explain** the impact (requirements, documents, gates, baselines).
4. **Propose** alternatives with trade-offs.
5. **Request** an authorized decision.

Execution resumes only after the decision is recorded. This rule applies equally to automation: the engine must not "helpfully" reconcile conflicting artifacts; it fails and reports.

## 5. Version Management (spec §11.4)

PFS supports and keeps distinguishable:

| Version | Scope |
|---|---|
| PFS version | The methodology system itself |
| Template version | Document/artifact templates |
| Generated foundation version | A project's generated foundation |
| Document version | Individual authoritative documents |
| Architecture baseline version | Approved architecture of a project |

Rules:

- Never substitute one version kind for another (a document version is not a baseline version).
- Superseded artifacts retain their version and link forward.
- The Baseline Manifest pins: PFS version, template version(s), document versions, architecture baseline version.

## 6. Baseline Change Control

Changing an approved baseline requires: Change Record + impact analysis + owner approval + re-validation of affected gates + new baseline version + updated Baseline Manifest. Silent or partial baseline edits invalidate the baseline's evidence chain.

## 7. Change Audit Trail

The Decision Register and Change Records together form the complete history: what changed, why, who approved, what validated, which version resulted. Audit (G9) samples this trail; gaps are Critical findings.

## 8. Traceability

AC-09 (Change Governance), AC-03 (Decision Governance, with PFS-M0-D04) — see PFS-M0-D12.
