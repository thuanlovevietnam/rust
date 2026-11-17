# Foundation Lifecycle

**Document ID:** PFS-M0-D03  
**Title:** Foundation Lifecycle  
**Version:** 1.0.0  
**Status:** Proposed  
**Owner:** Project Owner (unassigned — see PFS-M0-D12, Open Item OI-01)  
**Created:** 2026-11-17  
**Updated:** 2026-11-17  
**Related documents:** PFS-M0-SPEC-001 (§5), PFS-M0-D08 (Quality Gate Model), PFS-M0-D06 (Documentation Governance), PFS-M0-D07 (Agent System Concept)  
**Approval reference:** None — awaiting owner approval  

> Source of truth: PFS-M0-SPEC-001 §5. The lifecycle below is reproduced with stage-to-gate mapping added; gate details live in PFS-M0-D08. Conflicts resolve in favor of the spec.

## 1. Lifecycle Overview

PFS establishes a standardized eleven-stage lifecycle, Stage 0 through Stage 10, from project initialization to approved baseline. Stages are sequential by dependency but findings may force regression to an earlier stage (see §4).

## 2. Stage Definitions

### Stage 0 — Initialization
- **Purpose:** Establish a project workspace; identify the project owner; record initial project information; select a project category.
- **Output:** Project identity; initial project profile; initial workspace.
- **Gate:** G0 (Initialization).

### Stage 1 — Discovery
- **Purpose:** Understand the project; identify stakeholders; establish objectives; identify constraints; discover risks; identify unknown information.
- **Output:** Project Charter; Scope Definition; Stakeholder Map; Initial Risk Register.
- **Gate:** G1 (Project Definition).

### Stage 2 — Requirements Engineering
- **Purpose:** Identify functional and non-functional requirements; define system boundaries; establish measurable acceptance criteria; identify dependencies and constraints.
- **Output:** Requirements Specification; Requirements Traceability Matrix; Acceptance Criteria; Requirements Baseline Proposal.
- **Gate:** G2 (Requirements).

### Stage 3 — Architecture Design
- **Purpose:** Analyze architectural alternatives; design system boundaries; define modules and responsibilities; define data and security models; define interfaces and contracts; evaluate scalability and maintainability.
- **Output:** Architecture Specification; Architecture Diagrams; Dependency Map; Architecture Decision Proposals.
- **Gate:** G3 (Architecture).

### Stage 4 — Governance Establishment
- **Purpose:** Establish decision authority; define change management; define documentation authority; define approval requirements; establish project rules.
- **Output:** Governance Specification; Decision Register; Change Management Rules.
- **Gate:** G4 (Governance).

### Stage 5 — Documentation Foundation
- **Purpose:** Generate the documentation structure; establish authoritative documents; define document relationships; establish versioning and status conventions.
- **Output:** Documentation Repository Structure; Document Templates; Documentation Index; Traceability Structure.
- **Gate:** G5 (Documentation).

### Stage 6 — Agent Foundation
- **Purpose:** Establish universal AI instructions; define policies; create skills and workflows; define agent roles; establish platform adapters.
- **Output:** AGENTS.md; .agents/; Agent Capability Registry; Platform Integration Specifications.
- **Gate:** G6 (Agent Foundation).

### Stage 7 — Quality Foundation
- **Purpose:** Define quality standards; define validation procedures; define testing requirements; establish quality gates; define verification evidence.
- **Output:** Quality Specification; Validation Rules; Test Strategy; Quality Gate Definitions.
- **Gate:** G7 (Quality Foundation).

### Stage 8 — Bootstrap
- **Purpose:** Generate the initial project structure; create minimal configuration; establish development tooling; generate required source-code skeletons when applicable; verify the initial build or equivalent project artifact.
- **Output:** Initial Repository; Build Configuration; Test Infrastructure; Bootstrap Report.
- **Gate:** G8 (Bootstrap).

### Stage 9 — Independent Audit
- **Purpose:** Verify consistency; identify architectural conflicts; detect missing requirements; detect incomplete documentation; verify agent instructions; verify acceptance evidence.
- **Output:** Audit Report; Findings Register; Remediation Plan.
- **Gate:** G9 (Independent Audit).

### Stage 10 — Baseline Approval
- **Purpose:** Consolidate approved decisions; confirm quality gate results; establish the official foundation version.
- **Output:** Approved Foundation Baseline; Baseline Manifest; Approval Record; Development Readiness Status.
- **Gate:** G10 (Baseline Approval).

## 3. Stage-to-Gate Mapping

| Stage | Gate | Lifecycle question answered |
|---|---|---|
| 0 Initialization | G0 | Is the project workspace and ownership established? |
| 1 Discovery | G1 | Is the project understood and defined? |
| 2 Requirements | G2 | Are requirements complete, measurable and traceable? |
| 3 Architecture | G3 | Is the architecture derived from requirements and approved? |
| 4 Governance | G4 | Is decision authority and change control established? |
| 5 Documentation | G5 | Is the documentation system authoritative and consistent? |
| 6 Agent Foundation | G6 | Are agent instructions, policies and roles defined? |
| 7 Quality | G7 | Are quality gates and evidence requirements defined? |
| 8 Bootstrap | G8 | Does the initial artifact build/verify? |
| 9 Independent Audit | G9 | Does an independent review confirm consistency? |
| 10 Baseline Approval | G10 | Is the foundation approved and versioned as baseline? |

## 4. Regression and Iteration Rules

- A gate may not pass while its required deliverables are missing or invalid (PFS-M0-D08 §4).
- A failed audit (Stage 9) or a conflict discovered in any stage forces stop-the-affected-work, per architecture change protection (PFS-M0-D09 §4), and regression to the affected stage.
- Regression does not erase history: prior decisions remain in the Decision Register; superseded documents are marked Superseded, never deleted (spec §11, §8.3).

## 5. Lifecycle Invariants

1. No stage is entered on an assumption about an unapproved prior gate (spec §6.4).
2. Evidence precedes approval; approval precedes baseline.
3. The lifecycle is identical across project categories; category differences are configuration, not process forks (PFS-M0-D02).
4. Stages 6 and 7 produce instructions and controls; they do not authorize bypassing Stage 9 independent audit.

## 6. Verification

Lifecycle completeness is verified against AC-02 (PFS-M0-D12): every stage has purpose, outputs, a gate, and traceable deliverables in this document.
