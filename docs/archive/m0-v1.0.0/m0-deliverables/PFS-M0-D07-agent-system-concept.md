# Agent System Concept

**Document ID:** PFS-M0-D07  
**Title:** Agent System Concept  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§9), PFS-M0-D04 (CP-04), PFS-M0-D05, PFS-M0-D08 (G6), PFS-M0-D10  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §9. This is a **concept** document: it fixes structure, hierarchy, roles, skills and workflows. It does not implement orchestration, adapters or platform bindings (M2 scope; spec §14, §18).

## 1. Core Structure (spec §9.1)

Platform-independent logical layout:

```
.agents/
  policies/
  knowledge/
  skills/
  workflows/
  templates/
  scripts/
  registry/
```

Plus the project-root `AGENTS.md` as the mandatory platform entry point.

| Directory | Contains | Authoritative for |
|---|---|---|
| policies/ | Security, governance, change policies | Non-negotiable rules |
| knowledge/ | Project knowledge packs (layered) | What the project is |
| skills/ | Task skills (see §5) | How to perform task types |
| workflows/ | Multi-step procedures (see §6) | Order and approvals of steps |
| templates/ | Document/artifact templates | Canonical artifact shapes |
| scripts/ | Automation entry points (governed) | Deterministic helper invocation |
| registry/ | Capability registry, indexes | What exists and how to find it |

## 2. Agent Instruction Hierarchy and Precedence (spec §9.2)

Precedence, highest first:

1. Project-level mandatory instructions (AGENTS.md)
2. Security and governance policies (.agents/policies/)
3. Project architecture constraints (architecture spec, ADRs)
4. Task-specific workflows (.agents/workflows/)
5. Domain-specific skills (.agents/skills/)
6. Platform-specific execution instructions (adapters)

Rules:

- Conflicts resolve by this precedence, never by agent convenience or whichever instruction loads last.
- Higher-priority safety and security requirements are never overridden by lower-level task instructions.
- An agent detecting an unresolvable conflict must stop, record it and request an authorized decision (PFS-M0-D09 §4).
- Instructions at each level reference — never copy-redefine — the level above.

## 3. Agent Roles (spec §9.3)

Configurable logical roles (implementation depends on platform capabilities):

| Role | Primary responsibility |
|---|---|
| Project Analyst | Discovery, stakeholder and risk identification |
| Requirements Engineer | Requirements, acceptance criteria, RTM |
| System Architect | Alternatives, architecture spec, dependency map |
| Security Architect | Threat modeling, security model, policy checks |
| Data Architect | Data model, storage decisions, data governance |
| Software Engineer | Implementation from approved specs |
| Documentation Engineer | Documentation structure, integrity, index |
| Quality Engineer | Gates, validation, evidence collection |
| Independent Auditor | Stage 9 audit, findings register |

Roles are logical. A single platform agent may implement several roles; a role may also map to no agent and a human. Role definitions live in the Agent Capability Registry (Stage 6 output).

## 4. Progressive Disclosure (CP-04)

- AGENTS.md is small and mandatory; it points to policies and registry, never duplicates them.
- Agents load knowledge/skills only when a workflow requires them.
- Knowledge packs are layered: core → category → project-specific. Loading all layers for a small task is a defect, not thoroughness.

## 5. Skills (spec §9.4)

Each skill must contain:

- Unique identifier
- Name
- Description
- Activation conditions
- Required knowledge
- Procedure
- Constraints
- Expected outputs
- Completion criteria
- References where applicable

Skills are invocable units of know-how with explicit entry/exit. A skill without completion criteria is invalid.

## 6. Workflows (spec §9.5)

Each workflow must define:

- Trigger
- Preconditions
- Required inputs
- Execution steps
- Decision points
- Required approvals
- Outputs
- Failure handling
- Completion conditions

Workflows encode approvals explicitly; an approval step has no default and cannot be satisfied by the agent itself (CP-03).

## 7. Capability Registry

Stage 6 output `Agent Capability Registry` is the single index of roles, skills, workflows, policies and adapter bindings with IDs, versions and statuses. It is generated/validated by automation (PFS-M0-D05 §3), reviewed by the decision authority, and checked at G6.

## 8. Platform Adapters (concept)

Provider- or platform-specific instructions (context format, tool calling, subagent binding) live in adapters only (spec §7.5). Adapters contain no policy semantics; they translate. An adapter that adds, removes or rewrites policies is a critical defect.

## 9. Explicit Non-Capabilities

Agents must not: approve decisions, change requirements, upgrade statuses, override policies, delete authoritative documents, or execute arbitrary generated code without control (PFS-M0-D05 §4, PFS-M0-D10).

## 10. Traceability

AC-06 (Agent Independence) — the concept is platform-neutral by construction; verification of concrete adapters is M2/M4 scope. See PFS-M0-D12.
