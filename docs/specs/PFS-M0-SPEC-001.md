# PROJECT FOUNDATION SYSTEM (PFS)
# M0 — FOUNDATION METHODOLOGY SPECIFICATION

**Document ID:** PFS-M0-SPEC-001  
**Version:** 1.1.0  
**Status:** Proposed — Awaiting Owner Approval  
**Milestone:** M0 — Foundation Methodology  
**Project:** Project Foundation System  
**Scope:** Universal  
**Execution Model:** Hybrid (AI + Deterministic Automation)  
**Core Technology Direction:** Rust  
**Architecture Principle:** Provider-independent, modular, extensible  
**Parent review:** PFS-M0-REVIEW-001 (incorporated as mandatory amendments)  
**Supersedes:** v1.0.0 (archived at docs/archive/m0-v1.0.0/PFS-M0-SPEC-001-v1.0.0.md)  

---

# 1. PURPOSE

## 1.1. Objective

Project Foundation System (PFS) is a reusable system for designing, establishing, validating and governing the foundations of new projects.

PFS aims to eliminate the need to manually design project structures, documentation systems, architecture specifications, AI agent instructions and quality controls for every new project.

PFS must provide a repeatable methodology that transforms an initial project idea into an approved and verifiable Project Foundation.

The generated foundation must provide sufficient information for humans and AI agents to understand, implement, maintain and extend the project without relying on undocumented assumptions.

## 1.2. Core Mission

PFS must be able to:

1. Understand the project's objectives and requirements.
2. Identify the project's nature, scope and constraints.
3. Analyze functional and non-functional requirements.
4. Design an appropriate architecture.
5. Establish architecture decisions and governance.
6. Generate a structured documentation system.
7. Generate a universal AI Agent system.
8. Establish automated validation and quality controls.
9. Produce a verified project baseline.
10. Support controlled evolution throughout the project lifecycle.

## 1.3. Fundamental Philosophy

PFS follows these principles:

- Architecture before implementation.
- Requirements before architecture.
- Decisions before irreversible changes.
- Documentation as an engineering asset.
- Explicit ownership of important decisions.
- Automation for deterministic tasks.
- AI for reasoning, analysis and design.
- Verification based on evidence.
- Reusable foundations without forcing identical architectures.
- Technology independence at the methodology level.

---

# 2. PRODUCT DEFINITION

## 2.1. Product Identity

PFS is an independent Project Foundation Generator and Governance System.

It is not merely:
- A prompt collection.
- A project template repository.
- An AI coding assistant.
- A code generator.
- A documentation generator.
- An agent orchestration framework.

It combines methodology, structured project knowledge, AI-assisted engineering and deterministic validation into one coherent system.

## 2.2. Universal Scope

PFS must support different categories of projects via an extensible category model (§5.2) and a capability-based tailoring mechanism (§5.3–5.4).

Categories are classification aids, not mandatory architectural templates. PFS must not force every project to use the same software architecture; it must select the appropriate methodology and foundation according to project characteristics.

## 2.3. Universal Does Not Mean One-Size-Fits-All

PFS must distinguish between:

**Universal principles:**
- Requirements traceability.
- Decision governance.
- Documentation integrity.
- Security awareness.
- Quality assurance.
- Version management.
- Clear ownership.
- Verifiable acceptance criteria.

**Project-specific decisions:**
- Programming languages.
- Frameworks.
- Database technologies.
- Deployment environments.
- Architectural styles.
- Testing strategies.
- Agent capabilities.
- Infrastructure requirements.

Universal principles are shared. Project-specific decisions are configurable.

---

# 3. SYSTEM BOUNDARIES

## 3.1. PFS Responsibilities

PFS owns:

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

## 3.2. External Responsibilities

PFS does not automatically own:

- The actual business operations of the generated project.
- All application source code.
- External infrastructure.
- Third-party service availability.
- AI model quality.
- Final approval of architecture decisions.
- Business decisions belonging to project owners.

PFS may generate specifications and supporting code for these areas, but their implementation remains subject to project-specific scope and approval.

## 3.3. Separation of Concerns

PFS must distinguish four separate layers:

1. Methodology: How a project should be established.
2. Project knowledge: What the project is and how it is designed.
3. Agent system: How AI agents interact with project knowledge.
4. Automation: How deterministic tasks are executed and verified.

These layers must not be merged into one undifferentiated collection of prompts or scripts.

---

# 4. CORE SYSTEM PRINCIPLES

## 4.1. Requirements-Driven Architecture

Architecture must be derived from validated requirements, constraints and risks.

AI agents must not select architectural patterns simply because they are familiar or popular.

Every important architectural decision must have an identifiable justification traceable to requirements, constraints or documented risks (see §8.4).

## 4.2. Single Source of Truth

Every important project concept must have one authoritative location.

Examples:

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

Other files may reference authoritative information but must not silently redefine it.

Ownership, domains, conflict detection and resolution are defined in §12.

## 4.3. Explicit Decision Ownership

AI agents may:
- Analyze.
- Recommend.
- Compare alternatives.
- Draft specifications.
- Identify risks.
- Propose changes.

Only an authorized project owner or delegated decision authority may approve decisions requiring owner approval.

AI-generated content must not automatically become an approved decision (see §12.4, §13).

## 4.4. Progressive Disclosure

PFS must organize information so that agents load only the information needed for their current task.

The system must avoid:
- Excessively large instruction files.
- Unnecessary context loading.
- Repeated knowledge across documents.
- Conflicting rules.
- Unstructured prompt collections.

## 4.5. Evidence-Based Validation

A task cannot be marked as verified merely because an agent reports success.

Verification must reference observable evidence, such as:
- Test results.
- Build results.
- Static analysis.
- Schema validation.
- Architecture checks.
- Document consistency checks.
- Human approval records.

## 4.6. Reproducibility

Given the same:
- Project inputs.
- Approved decisions.
- Template versions.
- Configuration.
- Generator version.

PFS should produce equivalent structural outputs.

AI-generated reasoning may vary, but deterministic generation and validation must be reproducible (see §10).

## 4.7. Controlled Evolution

The generated foundation must support changes without losing historical decisions or traceability.

Architecture changes must follow an explicit change process (see §15).

---

# 5. UNIVERSAL PROJECT MODEL

*(Introduced by PFS-M0-REVIEW-001 §3; resolves F01.)*

## 5.1. Project Profile

Every PFS-managed project must have a Project Profile.

The profile must contain:

- Project identity.
- Project category.
- Project objectives.
- Project scope.
- Stakeholders.
- Complexity characteristics.
- Technical characteristics.
- Risk profile.
- Regulatory constraints.
- Operational requirements.
- Delivery constraints.
- Required capabilities.

Unknown information must be explicitly marked as unknown rather than invented. A profile with invented values is invalid input to every downstream stage.

## 5.2. Project Categories

PFS must support extensible project categories.

Initial categories:

- Software.
- Business.
- Research.
- Infrastructure.
- Data and AI.
- Automation.
- Technical operations.
- Other.

Categories are classification aids, not mandatory architectural templates. New categories may be added through the change process (§15).

## 5.3. Capability Model

A project must be described through required capabilities.

Examples:

- Requirements management.
- Architecture management.
- Security management.
- Data management.
- Financial control.
- Experiment tracking.
- Operational management.
- Compliance management.
- Quality management.
- Documentation management.

Capabilities may be mandatory, optional or not applicable.

Each not-applicable decision must have a recorded justification in the Project Profile. A capability without status and justification is unassessed, not absent.

## 5.4. Tailoring Rules

PFS must select project foundation components according to:

- Project characteristics.
- Risk.
- Complexity.
- Stakeholder needs.
- Applicable constraints.
- Required quality level.

PFS must not generate unnecessary documentation solely because a template exists. Tailoring decisions are recorded in the Project Profile and are auditable at G1 (§13.5) and Stage 1.

---

# 6. FOUNDATION LIFECYCLE

Stages, outputs and gates are defined in the M0 package (04-FOUNDATION-METHODOLOGY.md). The normative stage set is:

| Stage | Name | Gate |
|---|---|---|
| 0 | Initialization (establishes Project Profile creation) | G0 |
| 1 | Discovery | G1 |
| 2 | Requirements Engineering | G2 |
| 3 | Architecture Design (evaluates the views of §8.1) | G3 |
| 4 | Governance Establishment | G4 |
| 5 | Documentation Foundation | G5 |
| 6 | Agent Foundation | G6 |
| 7 | Quality Foundation | G7 |
| 8 | Bootstrap | G8 |
| 9 | Independent Audit | G9 |
| 10 | Baseline Approval | G10 |

Lifecycle invariants:

1. No stage is entered on the assumption that an unapproved prior gate has passed (§7.4).
2. Evidence precedes approval; approval precedes baseline.
3. The lifecycle is identical across categories; category differences are configuration, expressed via the Project Profile and Capability Model (§5), never process forks.

---

# 7. MILESTONE GOVERNANCE

## 7.1. Milestone Structure

PFS uses milestone-based development.

| Milestone | Name | Primary outcome |
|---|---|---|
| M0 | Foundation Methodology | Establish the methodology |
| M1 | Documentation & Architecture | Documentation and architecture specifications |
| M2 | Universal Agent System | Multi-agent instruction system |
| M3 | Validation & Quality Gates | Verification and governance controls |
| M4 | Generator Automation | Rust automation engine |

## 7.2. Milestone Specification Requirements

Every milestone must have: Purpose; Scope; Non-goals; Dependencies; Functional requirements; Non-functional requirements where applicable; Architecture considerations; Deliverables; Acceptance criteria; Verification procedures; Risks; Exit criteria.

## 7.3. Milestone States

Allowed states: Proposed; Approved; In Progress; Blocked; Under Review; Accepted; Rejected; Superseded.

Only an authorized decision authority may mark a milestone Accepted.

## 7.4. Dependency Rules

A milestone must not assume that an unapproved dependency is already established.

If a dependency is missing:
- Record it.
- Identify its impact.
- Propose a resolution.
- Request the required approval.

---

# 8. ARCHITECTURE VIEW MODEL

*(Introduced by PFS-M0-REVIEW-001 §4; resolves F02.)*

## 8.1. View Categories

PFS must evaluate these architecture views:

1. Context.
2. Structure.
3. Behavior.
4. Data.
5. Security.
6. Interface.
7. Deployment.
8. Operations.

## 8.2. Applicability

Each view must be classified as:

- Required.
- Optional.
- Not Applicable.

The classification must include its rationale. A view without classification is unevaluated, not waived.

## 8.3. View Consistency

Architecture views must not contradict one another. In particular:

- Component ownership must agree with dependency maps.
- Data ownership must agree with security boundaries.
- Interface definitions must agree with component responsibilities.
- Deployment topology must agree with operational requirements.

## 8.4. Architecture Traceability

Every important architecture decision must trace to one or more requirements, constraints or documented risks.

---

# 9. ARTIFACT IDENTITY AND TRACEABILITY

*(Extended by PFS-M0-REVIEW-001 §7; resolves F05.)*

## 9.1. Stable Identity

Every authoritative artifact must have a stable unique identifier.

Identifiers must remain stable when filenames or repository locations change.

## 9.2. Artifact Metadata

Required metadata:

- ID.
- Type.
- Title.
- Version.
- Status.
- Owner.
- Creation date.
- Modification date.
- Source.
- Dependencies.
- Related artifacts.
- Approval reference where applicable.

## 9.3. Artifact Relationships

PFS must support explicit relationships:

- Depends on.
- Derived from.
- Implements.
- Verifies.
- Supersedes.
- Conflicts with.
- References.

## 9.4. Traceability

PFS must support the following traceability chain:

Project Objective → Requirement → Architecture → Decision → Specification → Implementation → Test → Evidence → Acceptance.

Not every project must use every relationship type, but required relationships must be verifiable.

PFS must be able to identify:
- Requirements without implementation plans.
- Architecture decisions without supporting requirements.
- Specifications without acceptance criteria.
- Implementation changes without corresponding decisions where required.
- Tests that do not verify declared requirements.

## 9.5. Document Status

Allowed statuses: Draft; Proposed; In Review; Approved; Deprecated; Superseded.

A document being generated does not imply that it is approved. Status transitions are governance acts (§12, §13).

## 9.6. Documentation Integrity

The system must detect:
- Duplicate authoritative definitions.
- Broken internal references.
- Missing required metadata.
- Invalid document statuses.
- Missing approval references.
- Conflicting versions.
- Unresolved mandatory dependencies.

## 9.7. Documentation Categories

PFS must support: Foundation; Requirements; Architecture; Specifications; Decisions; Contracts; Development; Operations; Quality; Governance.

## 9.8. Versioning

PFS must distinguish the version kinds of §15.1. Version increments follow documented intent (major = breaking methodology change, minor = additive, patch = editorial).

---

# 10. HYBRID EXECUTION MODEL AND SAFE AUTOMATION

*(Extended by PFS-M0-REVIEW-001 §8–9; resolves F06, F07.)*

## 10.1. Fundamental Separation

AI is responsible for tasks requiring contextual reasoning. Rust automation is responsible for deterministic, repeatable and verifiable operations.

## 10.2. AI Responsibilities

AI agents may perform: project discovery; requirements analysis; architecture exploration; alternative evaluation; document drafting; risk identification; skill selection; workflow execution planning; code review; technical audit.

## 10.3. Automation Responsibilities

The automation engine should perform: directory creation; file generation from approved templates; schema validation; document metadata validation; reference integrity checks; registry generation; version and manifest management; template consistency checks; deterministic quality checks; generation reports.

## 10.4. Approval Boundaries

Automation must not silently: approve architecture decisions; change project requirements; upgrade document statuses; override project policies; delete authoritative documents; change protected configurations.

Operations with governance impact require explicit authorization (§12, §13).

## 10.5. AI Provider Independence

The methodology must not depend on a particular model or provider. Provider-specific integration must be isolated in adapters.

The core system must not assume:
- One specific context format.
- One specific tool-calling interface.
- One specific subagent implementation.
- One specific AI model.
- One specific commercial provider.

## 10.6. Idempotency

Repeated execution with unchanged inputs and versions must not create duplicate or unintended modifications.

## 10.7. Dry Run

Generation operations must support preview before writing files.

The preview must identify:
- New files.
- Modified files.
- Unchanged files.
- Conflicts.
- Potentially destructive operations.

## 10.8. Ownership Tracking

PFS must distinguish:
- PFS-managed files.
- User-managed files.
- External files.
- Untracked files.

## 10.9. Conflict Handling

Existing files must not be silently overwritten.

Destructive changes require explicit authorization.

## 10.10. Manifest

Generation must produce a manifest describing the generated artifacts, their ownership, versions and integrity information.

## 10.11. Generation Staging

Operations should be prepared in a staging area before being committed to the target project.

## 10.12. Recovery Information

PFS must record:
- Operation identity.
- Target path.
- Previous state where recoverable.
- New state.
- Operation status.
- Completion evidence.

## 10.13. Interruption Handling

If execution stops unexpectedly, PFS must be able to identify incomplete operations. A partially completed generation must not be treated as successful.

## 10.14. Recovery Verification

A recovery operation must be followed by validation of the affected project state.

---

# 11. UNIVERSAL AGENT SYSTEM MODEL

## 11.1. Core Structure

The universal agent system must be independent of any specific coding platform.

Initial logical structure:

.agents/
- policies/
- knowledge/
- skills/
- workflows/
- templates/
- scripts/
- registry/

## 11.2. Agent Instruction Hierarchy

The system must distinguish:

1. Project-level mandatory instructions.
2. Security and governance policies.
3. Project architecture constraints.
4. Task-specific workflows.
5. Domain-specific skills.
6. Platform-specific execution instructions.

Conflicts must be resolved through an explicit precedence policy, not by allowing the agent to choose whichever instruction is convenient.

Higher-priority safety and security requirements must not be overridden by lower-level task instructions.

## 11.3. Agent Roles

PFS should support configurable agent roles, such as: Project Analyst; Requirements Engineer; System Architect; Security Architect; Data Architect; Software Engineer; Documentation Engineer; Quality Engineer; Independent Auditor.

These are logical roles. Their implementation as actual subagents depends on the capabilities of the selected platform. The governance roles of §12.1 are distinct from these execution roles.

## 11.4. Skills

Each skill must contain: unique identifier; name; description; activation conditions; required knowledge; procedure; constraints; expected outputs; completion criteria; references where applicable.

## 11.5. Workflows

Each workflow must define: trigger; preconditions; required inputs; execution steps; decision points; required approvals; outputs; failure handling; completion conditions.

## 11.6. Agent Permission Levels

*(Introduced by PFS-M0-REVIEW-001 §10; resolves F08.)*

PFS must support the following logical permission levels:

- L0: Read-only.
- L1: Analysis and proposal.
- L2: Draft artifact creation.
- L3: Authorized project modification.
- L4: Approved script and test execution.
- L5: Privileged or destructive operations requiring explicit authorization.

These levels are logical classifications and must be mapped to actual platform capabilities by adapters.

## 11.7. Permission Scope

Permissions must be constrained by: resource; operation; project; environment; time or execution session; approval requirements.

## 11.8. Least Privilege

An agent must receive only the permissions necessary for its assigned task.

## 11.9. Untrusted Input

External documents, imported templates, model output and generated instructions must be treated as untrusted inputs until validated.

## 11.10. Prohibited Implicit Actions

An agent must not:

- Delete authoritative project information without authorization.
- Modify approved architecture decisions without change approval.
- Execute arbitrary privileged commands.
- Expose secrets.
- Change access controls without authorization.
- Send restricted project data to external providers without authorization.

## 11.11. Multi-Agent Conflict Management

*(Introduced by PFS-M0-REVIEW-001 §11; resolves F09.)*

PFS must distinguish the following conflict categories:

- Factual conflict.
- Requirement conflict.
- Architecture conflict.
- Security conflict.
- Implementation conflict.
- Policy conflict.
- Evidence conflict.

Resolution process:

1. Record each agent's position.
2. Identify supporting evidence.
3. Identify assumptions.
4. Evaluate impact.
5. Produce alternatives.
6. Escalate unresolved decisions.
7. Record the authorized outcome.

Critical decisions must support review by an independent role or reviewer. Agent consensus must not replace owner approval.

---

# 12. AUTHORITY AND DECISION MODEL

*(Introduced by PFS-M0-REVIEW-001 §5–6; resolves F03, F04.)*

## 12.1. Roles

PFS must support:

- Project Owner.
- Decision Approver.
- Project Architect.
- Requirements Engineer.
- Security Reviewer.
- Operator.
- AI Agent.
- Independent Auditor.
- Observer.

A role may be held by a human, an authorized process, or — for non-authoritative roles only — an AI agent. Authoritative approval is never granted to an AI agent.

## 12.2. Authoritative Ownership

Every authoritative artifact must declare its information domain and owner.

Two documents must not independently define the same authoritative fact without an explicit relationship (e.g., supersedes, derived-from).

## 12.3. Source Authority

PFS must distinguish:

- Governance authority.
- Requirements authority.
- Architecture authority.
- Contract authority.
- Implementation authority.
- Agent policy authority.
- Verification authority.

Authority is assigned by information domain and approval status, not by filename.

## 12.4. Separation of Duties and Approval Boundaries

PFS must support separation between proposal, approval, execution and verification.

For high-impact operations, the proposing agent must not be able to grant itself the approval required to execute the operation.

The following do not constitute approval (no implicit approval):

- File creation.
- Successful generation.
- Agent agreement.
- Passing tests.
- A document marked complete by an AI agent.

Approval requires an identifiable authorized action recorded as an Approval Record.

## 12.5. Approval Record

An approval record must contain:

- Decision ID.
- Approver identity.
- Approver authority.
- Decision.
- Timestamp.
- Approved version.
- Approval scope.
- Relevant evidence.

## 12.6. Conflict Resolution

When authoritative information conflicts:

1. Detect the conflict.
2. Record the conflicting artifacts.
3. Identify the affected requirements and components.
4. Evaluate the impact.
5. Suspend dependent changes where necessary.
6. Escalate to the responsible authority.
7. Record the resolution.
8. Update affected artifacts.
9. Validate consistency.

Agents must never resolve a governance conflict by silently choosing one document.

---

# 13. QUALITY AND ACCEPTANCE MODEL

*(Extended by PFS-M0-REVIEW-001 §13; resolves F11.)*

## 13.1. Quality Dimensions

PFS must evaluate:

- Completeness.
- Consistency.
- Traceability.
- Correctness.
- Security.
- Maintainability.
- Reproducibility.
- Verifiability.
- Portability.
- Extensibility.

## 13.2. Evidence

Every measurable quality claim must have supporting evidence.

| Claim | Required evidence |
|---|---|
| Build succeeds | Build output and exit status |
| Tests pass | Test report |
| Architecture is compliant | Architecture validation results |
| Documents are complete | Document validation report |
| Decisions are approved | Approval records |
| Agent understands project | Independent clean-room assessment |

Evidence must be distinguishable from claims.

## 13.3. Critical Requirements

Critical requirements cannot be compensated for by high scores in unrelated quality dimensions.

## 13.4. Exceptions

A failed requirement may only be accepted as an exception through an authorized and documented exception process. The exception must include:

- Reason.
- Risk.
- Scope.
- Mitigation.
- Expiration or review condition.
- Approver.

A failed gate remains failed until findings are resolved or formally excepted by an authorized authority.

## 13.5. Quality Gates

PFS must support the gates G0–G10 (Initialization; Project Definition; Requirements; Architecture; Governance; Documentation; Agent Foundation; Quality Foundation; Bootstrap; Independent Audit; Baseline Approval).

Each gate defines: entry conditions; required deliverables; validation rules; required evidence; approval authority; exit conditions.

## 13.6. Independent Audit

The audit must be performed independently of the agent or process that produced the foundation wherever practical. The auditor must not simply repeat the implementation agent's conclusions.

---

# 14. DATA CLASSIFICATION AND SUPPLY CHAIN SECURITY

*(Introduced by PFS-M0-REVIEW-001 §14; resolves F12.)*

## 14.1. Data Classification

PFS must support:

- Public.
- Internal.
- Confidential.
- Restricted.

Projects may extend this classification model.

## 14.2. Template Provenance

External templates and skills must record available provenance information:

- Source.
- Publisher.
- Version.
- License.
- Integrity hash.
- Required permissions.
- Validation status.

## 14.3. Untrusted Templates

Imported instructions must not override PFS security or governance policies.

## 14.4. Sensitive Data

Secrets must not be embedded in generated documents, prompts, manifests or logs.

PFS must define data handling requirements for each supported AI provider adapter.

## 14.5. Security Principles

1. Least privilege.
2. Explicit authorization.
3. Separation of trusted and untrusted inputs.
4. No implicit approval.
5. Protection of authoritative documents.
6. Safe file generation.
7. Path traversal protection.
8. Controlled execution of scripts.
9. Secret handling requirements.
10. Auditability of sensitive operations.

AI-generated content must be treated as untrusted until validated. External project descriptions, imported templates and third-party instructions must not be allowed to override system security policies. PFS must not execute arbitrary generated code merely because an AI agent requests it.

---

# 15. CHANGE, VERSION AND COMPATIBILITY MANAGEMENT

*(Extended by PFS-M0-REVIEW-001 §12; resolves F10.)*

## 15.1. Version Kinds

PFS must distinguish:

- Engine version.
- Methodology version.
- Template version.
- Schema version.
- Agent instruction version.
- Generated foundation version.
- Architecture baseline version.
- Document version.

These versions must be distinguishable and must not be substituted for one another.

## 15.2. Compatibility

Compatibility must be explicit. PFS must not assume that a newer engine can safely process every older project format.

## 15.3. Migration

Migration must include:

- Source version.
- Target version.
- Migration procedure.
- Preconditions.
- Expected changes.
- Backup or recovery strategy.
- Post-migration validation.

## 15.4. Backward Compatibility

Breaking changes must be identified and documented. A migration must not silently change approved project decisions.

## 15.5. Change Classification

PFS must classify changes into:

- Documentation changes.
- Requirement changes.
- Architecture changes.
- Security changes.
- Agent policy changes.
- Template changes.
- Generator changes.
- Baseline changes.

## 15.6. Change Process

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

## 15.7. Architecture Change Protection

An AI agent must never silently redefine an approved architecture.

When a conflict is discovered:
- Stop the affected implementation.
- Record the conflict.
- Explain its impact.
- Propose alternatives.
- Request an authorized decision.

---

# 16. TECHNOLOGY DIRECTION

## 16.1. Core Technology

Rust is the selected technology for the PFS core automation engine.

## 16.2. Architectural Principle

The methodology and generated project formats must remain independent of the implementation language of the PFS engine.

Rust is an implementation choice for PFS, not a requirement imposed on every project generated by PFS.

## 16.3. Proposed Core Responsibilities

The Rust engine is expected to handle: project initialization; structured configuration; template processing; filesystem operations; document metadata validation; schema validation; reference validation; manifest generation; deterministic validation; execution reporting.

## 16.4. Deferred Technical Decisions

M0 does not finalize:

- CLI framework.
- Async runtime.
- Serialization framework.
- Template engine.
- Database selection.
- AI provider integration.
- MCP implementation.
- GUI framework.
- Plugin architecture.

These decisions belong to later milestones after technical evaluation.

No technology dependency should be introduced without a documented justification.

---

# 17. M0 DOCUMENT PACKAGE

The M0 documentation package is organized as follows:

docs/
└── M0-foundation/
    ├── 00-M0-INDEX.md
    ├── 01-PFS-VISION.md
    ├── 02-PRODUCT-DEFINITION.md
    ├── 03-UNIVERSAL-PROJECT-MODEL.md
    ├── 04-FOUNDATION-METHODOLOGY.md
    ├── 05-GOVERNANCE-MODEL.md
    ├── 06-AUTHORITY-AND-DECISION-MODEL.md
    ├── 07-ARTIFACT-AND-TRACEABILITY-MODEL.md
    ├── 08-HYBRID-EXECUTION-MODEL.md
    ├── 09-AGENT-SECURITY-MODEL.md
    ├── 10-QUALITY-AND-ACCEPTANCE-MODEL.md
    ├── 11-VERSION-AND-CHANGE-MANAGEMENT.md
    ├── 12-SECURITY-AND-SUPPLY-CHAIN.md
    ├── 13-MILESTONE-ROADMAP.md
    ├── 14-M0-ACCEPTANCE-CRITERIA.md
    └── 15-M0-REVIEW-REPORT.md

The package must not contain duplicate authoritative definitions. This specification remains the parent; PFS-M0-REVIEW-001 defines the amendments incorporated by v1.1.0.

---

# 18. M0 REQUIREMENTS AND ACCEPTANCE CRITERIA

## 18.1. Mandatory M0 Requirements (from PFS-M0-REVIEW-001 §15)

| Requirement ID | Description |
|---|---|
| M0-REQ-001 | PFS must support universal project classification |
| M0-REQ-002 | PFS must support project-specific tailoring |
| M0-REQ-003 | PFS must define architecture views |
| M0-REQ-004 | PFS must define authoritative information ownership |
| M0-REQ-005 | PFS must detect authoritative information conflicts |
| M0-REQ-006 | PFS must define decision authority |
| M0-REQ-007 | PFS must support stable artifact identity |
| M0-REQ-008 | PFS must support traceability |
| M0-REQ-009 | PFS generation must be idempotent |
| M0-REQ-010 | PFS must support dry-run and conflict preview |
| M0-REQ-011 | PFS must define recovery requirements |
| M0-REQ-012 | PFS must define AI permission boundaries |
| M0-REQ-013 | PFS must support multi-agent conflict management |
| M0-REQ-014 | PFS must define version compatibility |
| M0-REQ-015 | PFS must define quality evidence |
| M0-REQ-016 | PFS must support documented exceptions |
| M0-REQ-017 | PFS must classify sensitive data |
| M0-REQ-018 | PFS must track template provenance |
| M0-REQ-019 | PFS must prevent unauthorized approval |
| M0-REQ-020 | PFS must support independent auditing |

## 18.2. Acceptance Criteria

Original criteria (retained, verbatim intent):

- **AC-01: Product Clarity** — objectives, boundaries and universal scope explicitly defined.
- **AC-02: Lifecycle Completeness** — lifecycle defined from initialization to baseline approval.
- **AC-03: Decision Governance** — proposed, approved and superseded decisions clearly distinguished.
- **AC-04: Single Source of Truth** — authoritative documentation ownership defined.
- **AC-05: Hybrid Execution** — AI and deterministic automation responsibilities clearly separated.
- **AC-06: Agent Independence** — methodology does not depend on a single AI provider.
- **AC-07: Quality Model** — quality dimensions and gate requirements defined.
- **AC-08: Evidence Model** — verification claims require identifiable evidence.
- **AC-09: Change Governance** — architecture and documentation change procedures defined.
- **AC-10: Security Principles** — trust boundaries and protected operations defined.
- **AC-11: Milestone Consistency** — M1–M4 have clearly defined boundaries and dependencies.
- **AC-12: No Unapproved Technical Assumptions** — deferred implementation decisions identified rather than silently finalized.

Additional criteria (PFS-M0-REVIEW-001 §16):

| ID | Acceptance criterion |
|---|---|
| AC-13 | Universal Project Model is defined |
| AC-14 | Project tailoring is defined |
| AC-15 | Architecture View Model is defined |
| AC-16 | Authority and conflict resolution are defined |
| AC-17 | Decision authority is defined |
| AC-18 | Artifact identity and traceability are defined |
| AC-19 | Safe generation requirements are defined |
| AC-20 | Recovery requirements are defined |
| AC-21 | Agent permissions are defined |
| AC-22 | Multi-agent conflict handling is defined |
| AC-23 | Version compatibility is defined |
| AC-24 | Evidence-based quality evaluation is defined |
| AC-25 | Data classification is defined |
| AC-26 | Template provenance is defined |
| AC-27 | Exception management is defined |
| AC-28 | No unresolved critical contradiction remains |

---

# 19. M0 EXIT CONDITIONS

M0 may be submitted for owner acceptance only when (PFS-M0-REVIEW-001 §18):

1. All critical findings have been resolved.
2. All mandatory requirements are represented in the M0 document package.
3. Requirements and acceptance criteria are traceable.
4. The Universal Project Model is sufficiently defined.
5. Authority and approval boundaries are explicit.
6. Agent execution governance is defined.
7. Automation safety requirements are defined.
8. Quality and evidence requirements are defined.
9. The M1–M4 boundaries are consistent.
10. An independent review finds no unresolved critical issue.

M0 does not authorize implementation of the Rust engine.

---

# 20. NEXT MILESTONE AND GOVERNING RULE

## 20.1. M1 — Documentation & Architecture Foundation

M1 must use the following approved M0 foundations (PFS-M0-REVIEW-001 §19):

- Project Profile.
- Capability Model.
- Artifact Identity.
- Document Authority.
- Traceability.
- Architecture Views.
- Decision Governance.
- Versioning.
- Quality Evidence.

M1 must not redefine these principles independently. If M1 identifies a deficiency, it must submit a change proposal against M0.

Expected M1 subjects: canonical repository structure; document taxonomy; document metadata schema; SPEC engineering standard; ADR/DR engineering standard; requirements traceability model; architecture specification framework; contract documentation; documentation versioning; cross-document consistency; documentation templates; documentation validation requirements.

## 20.2. Governing Rule

This document establishes the proposed foundation methodology for PFS.

All subsequent PFS milestones must comply with its approved principles.

If a later milestone discovers that an M0 principle is insufficient, it must propose a formal change rather than silently bypassing it.

The project owner remains the final authority for foundational decisions.

---

# 21. NON-GOALS OF M0

M0 is a methodology milestone. Explicitly excluded:

1. Implementing the Rust engine.
2. Building a graphical interface.
3. Implementing AI provider integrations.
4. Implementing MCP servers.
5. Implementing actual agent orchestration.
6. Building a complete project generator.
7. Generating production application code.
8. Implementing a persistent database.
9. Creating every possible project template.
10. Supporting every AI coding platform immediately.

---

# 22. CHANGE HISTORY

| Version | Date | Change | Authority |
|---|---|---|---|
| 1.0.0 | 2026-11-17 | Initial M0 Foundation Methodology Specification | Project Owner (proposed) |
| 1.1.0 | 2026-11-17 | Incorporated PFS-M0-REVIEW-001: F01–F12 amendments; new §5 Universal Project Model, §8 Architecture View Model, §12 Authority and Decision Model; extended §9 (artifact identity/relationships/traceability), §10 (safe generation & recovery), §11 (agent permissions, multi-agent conflicts), §13 (evidence, critical requirements, exceptions), §14 (data classification & supply chain), §15 (version kinds, compatibility, migration); revised §17 document package; added M0-REQ-001..020 and AC-13..28; revised exit conditions; added §20 M1 dependency list. v1.0.0 archived at docs/archive/m0-v1.0.0/. | PFS-M0-REVIEW-001 (independent review; pending owner approval) |

---

**END OF PFS-M0-SPEC-001**
