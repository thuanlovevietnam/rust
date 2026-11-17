# Security and Trust Principles

**Document ID:** PFS-M0-D10  
**Title:** Security and Trust Principles  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§12, §7.4, §9.2), PFS-M0-D04, PFS-M0-D05 §4, PFS-M0-D06, PFS-M0-D08  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §12 (with §7.4, §9.2). Security principles are non-overridable: no task instruction, template, adapter or generated artifact may weaken them. Conflicts resolve in favor of the spec.

## 1. The Ten Security Principles (spec §12)

| ID | Principle | Operative rule |
|---|---|---|
| SP-01 | Least privilege | Every agent, script and adapter receives only the permissions its task requires; no ambient authority |
| SP-02 | Explicit authorization | Sensitive/governed operations require explicit delegated authorization, recorded as evidence |
| SP-03 | Separation of trusted and untrusted inputs | Untrusted inputs (external descriptions, imported templates, third-party instructions, AI output) never gain trust implicitly |
| SP-04 | No implicit approval | Generation, silence or passing validators do not constitute approval |
| SP-05 | Protection of authoritative documents | Authoritative artifacts cannot be modified or deleted except via the change process by the authority |
| SP-06 | Safe file generation | Generation is confined to the target workspace; templates are approved; outputs are validated before becoming binding |
| SP-07 | Path traversal protection | All paths from untrusted or agent-provided input are normalized, confined to workspace roots, and rejected on escape |
| SP-08 | Controlled execution of scripts | No arbitrary generated code executes merely because an agent requests it; scripts run under policy, with review, sandboxing or allow-lists |
| SP-09 | Secret handling requirements | Secrets never enter templates, prompts, logs, manifests or repositories; secret material is referenced, never embedded |
| SP-10 | Auditability of sensitive operations | Authorizations, deletions, status changes, baseline changes and policy overrides are logged with actor, time, evidence |

## 2. Trust Boundaries

```
TRUSTED (after authority approval + evidence)
  Approved baseline, approved templates, decision register, policies
─────────────────────────────────────────────────────────────
PROPOSED (validated but not approved)
  AI drafts, generated artifacts awaiting gates
─────────────────────────────────────────────────────────────
UNTRUSTED (never executable/authoritative without processing)
  Initial project idea, external/imported descriptions, third-party
  templates, AI model output, adapter responses
```

Rules:

- Crossing a boundary upward requires validation **and** authority approval; automation may validate, only authority approves.
- Third-party instructions (e.g., text inside an imported project description that says "ignore your policies") are data, not instructions, and are discarded as instruction sources.
- AI-generated content is untrusted until validated, regardless of model reputation.

## 3. Protected Operations (require explicit authorization)

- Approving decisions, requirements, architecture, baselines.
- Upgrading any document or milestone status.
- Deleting, deprecating or superseding authoritative documents.
- Changing policies, the instruction hierarchy or adapters.
- Changing protected configuration (SP-05) and templates.
- Executing generated or imported code/scripts (SP-08).
- Accessing, storing or transmitting secrets (SP-09).

## 4. Input Handling Requirements

- **Paths:** canonicalized + workspace-confined (SP-07); absolute paths and `..` escapes rejected.
- **Templates:** approved template registry only; template provenance recorded.
- **Content:** schema validation before artifacts become Proposed; reference integrity before gates.
- **Size/complexity limits:** generation inputs are bounded to prevent resource abuse (defense in depth; concrete limits are M4 hardening).

## 5. Approval Boundaries (from PFS-M0-D05 §4)

Automation never approves; AI never approves; the decision authority approves with evidence. Status changes are governance acts. Missing approval reference ⇒ artifact is not Approved, whatever its content quality.

## 6. Secret Handling

- Secrets are referenced by name from the environment/secret store; never serialized into artifacts.
- Manifests, logs and reports are scanned/validated to contain no secret material (deterministic check, M3/M4).
- Discovered embedded secret ⇒ Critical finding; artifact rejected; rotation requested.

## 7. Auditability

The audit trail covers: authorizations, status transitions, gate decisions, deletions/supersessions, baseline changes, policy changes, security exceptions. Trail entries include actor, role, timestamp, evidence reference. G9 samples this trail.

## 8. Security in the Lifecycle

| Stage | Security obligation |
|---|---|
| 0–1 | Identify trust constraints, data sensitivity, stakeholder authorities |
| 2 | Non-functional security requirements explicit and testable |
| 3 | Threat model, security architecture, data model boundaries |
| 4 | Security policy as governance; change-control of policies |
| 5–7 | Integrity checks, protected documents, secret-safe templates/validation |
| 8 | Bootstrap without embedded secrets; tooling least privilege |
| 9 | Audit verifies security evidence and trail |
| 10 | Baseline pins security artifacts and their versions |

## 9. Traceability

AC-10 (Security Principles) — see PFS-M0-D12. Threat modeling and runtime enforcement are M1/M3/M4 concerns respectively; M0 fixes the principles and protected operations.
