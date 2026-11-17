# Universal Scope Definition

**Document ID:** PFS-M0-D02  
**Title:** Universal Scope Definition  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§2, §3), PFS-M0-D01, PFS-M0-D04  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §2–3. This document organizes scope and boundaries; conflicts resolve in favor of the spec.

## 1. Universal Scope Statement

PFS must support structurally different categories of projects while sharing one methodology. Universality applies to **principles and process**, not to **decisions**.

## 2. Target Project Categories (initial)

1. Software applications.
2. Web applications.
3. Desktop applications.
4. Mobile applications.
5. Backend and API systems.
6. SaaS platforms.
7. Enterprise information systems.
8. Data and AI systems.
9. Automation systems.
10. Infrastructure and platform projects.
11. Research and technical projects.
12. Other projects describable through structured requirements and deliverables.

Selection rule: the methodology **selects** the appropriate foundation per project characteristics; it never imposes one architecture on all categories.

## 3. Universal Principles (shared, non-configurable)

- Requirements traceability.
- Decision governance.
- Documentation integrity.
- Security awareness.
- Quality assurance.
- Version management.
- Clear ownership.
- Verifiable acceptance criteria.

## 4. Project-Specific Decisions (configurable, per project)

- Programming languages.
- Frameworks.
- Database technologies.
- Deployment environments.
- Architectural styles.
- Testing strategies.
- Agent capabilities.
- Infrastructure requirements.

**Rule:** universal principles are invariants enforced by the quality gates (PFS-M0-D08); project-specific decisions are recorded as project decisions with explicit ownership (PFS-M0-D04 §3, PFS-M0-D09).

## 5. System Boundaries

### 5.1. PFS owns

- Foundation methodology.
- Project discovery process.
- Requirement structuring.
- Architecture design process.
- Decision management.
- Documentation generation.
- Agent system generation.
- Quality gate definitions.
- Validation mechanisms.
- Baseline management.
- Foundation evolution procedures.

### 5.2. PFS does not automatically own

- The actual business operations of the generated project.
- All application source code.
- External infrastructure.
- Third-party service availability.
- AI model quality.
- Final approval of architecture decisions.
- Business decisions belonging to project owners.

PFS may generate specifications and supporting code for these areas; implementation remains subject to project-specific scope and owner approval.

## 6. Layer Separation (mandatory)

| Layer | Question answered | Examples |
|---|---|---|
| Methodology | How should a project be established? | Lifecycle stages, gates, change process |
| Project knowledge | What is the project? | Charter, requirements, architecture, ADRs |
| Agent system | How do agents interact with knowledge? | Policies, skills, workflows, roles |
| Automation | How are deterministic tasks executed and verified? | Generators, validators, manifests |

Layers must remain distinguishable in both design and repositories. Merging them into one collection of prompts or scripts is a boundary violation.

## 7. Scope Limits and Exclusions

- PFS does not guarantee AI model quality; it constrains how AI output is used and verified (PFS-M0-D05, PFS-M0-D10).
- PFS does not override owner authority; only an authorized decision authority approves foundational decisions (spec §6.3, §19).
- PFS does not fix implementation technologies at the methodology level (spec §13).
- M0 itself delivers no implementation (spec §14).

## 8. Category Coverage Verification (M0 self-check)

For each target category, the methodology must be applicable without alteration of its universal principles. Category-specific differences are expressed as **configurable decisions** and **project profile inputs**, never as forks of the methodology. Any category that cannot be expressed this way must be recorded as an open item in the acceptance report rather than silently special-cased.

## 9. Extensibility

New categories may be added only through the change process (PFS-M0-D09): identify category, define its distinguishing decisions, verify gate applicability, record as accepted exception or methodology extension.
