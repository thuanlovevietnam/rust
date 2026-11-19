# PFS-M1-DOC-000 — Milestone M1 Architecture Index & Master Package Registry

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-000 |
| Document Title | Milestone M1 Architecture Index & Master Package Registry |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Target Reviewer | Project Owner (Nguyễn Thế Thuận) |
| Classification | Internal |
| Parent Baseline | PFS M0 Foundation Package v1.1.0 ([PFS-M0-SPEC-001](file:///C:/Users/OK259/rust/docs/specs/PFS-M0-SPEC-001.md)) |
| Owner Decision Reference | [PFS-M0-OWNER-DECISIONS-001](file:///C:/Users/OK259/rust/docs/M0-foundation/decisions/PFS-M0-OWNER-DECISIONS-001.md), [PFS-M0-OWNER-DECISIONS-002](file:///C:/Users/OK259/rust/docs/M0-foundation/decisions/PFS-M0-OWNER-DECISIONS-002.md) |

---

## 1. Executive Summary & Purpose

Tài liệu này đóng vai trò là Danh mục Chủ quản (Master Package Registry) và Điểm truy cập chuẩn hóa cho toàn bộ gói hồ sơ kiến trúc **Milestone M1 (Documentation & Architecture Foundation)** của Dự án **Project Foundation System (PFS)**.

Milestone M1 chuyển hóa các định nghĩa phương pháp luận, mô hình quản trị và nguyên tắc cơ bản đã được nghiệm thu tại Milestone M0 thành một **Architecture Baseline** hoàn chỉnh, có tính xác định, có thể kiểm chứng, độc lập với AI provider và chuẩn bị trực tiếp cho việc triển khai thực tế bằng ngôn ngữ Rust trong Milestone M2–M4.

M1 tuân thủ nghiêm ngặt các bất biến (invariants) từ M0:
1. **Universal Scope:** PFS không bị giới hạn trong Software Engineering; hỗ trợ Business, Research, Operations, Organizational và Custom domains.
2. **Hybrid Execution Model:** Kết hợp chặt chẽ giữa AI Reasoning (phân tích, đề xuất, sinh cấu trúc) và Deterministic Automation (thực thi quy tắc, xác thực, phân quyền, quản lý state bằng Rust).
3. **Explicit Authority & Least Privilege:** Mô hình phân quyền L0–L5; AI không tự cấp quyền và không tự duyệt; Project Owner nắm quyền quyết định tối cao.
4. **Provider-Independent Architecture:** Lớp lõi PFS Core độc lập hoàn toàn với bất kỳ AI model hay provider cụ thể nào thông qua Gateway/Adapter Pattern.
5. **Idempotent & Safe Generation:** Sinh foundation có kiểm soát, có dry-run preview, atomic commit, ownership manifest, không ghi đè trái phép.

---

## 2. Structure of M1 Architecture Package

Gói tài liệu M1 bao gồm **29 tài liệu kiến trúc chính thức** (đánh số từ `00` đến `28`) được phân bổ thành 8 phân hệ chuyên môn, cùng hệ thống tài liệu hỗ trợ bao gồm 20 Architecture Decision Records (ADRs), 16 Architecture Diagrams, hệ thống Schemas, Contracts, Matrices và Báo cáo kiểm định độc lập.

```
docs/M1-architecture/
├── 00-governance/
│   ├── 00-M1-INDEX.md                                 (PFS-M1-DOC-000)
│   ├── 01-M1-SCOPE-AND-BOUNDARIES.md                  (PFS-M1-DOC-001)
│   ├── 02-M1-ARCHITECTURE-METHOD.md                   (PFS-M1-DOC-002)
│   └── 03-ARCHITECTURE-REQUIREMENTS.md                (PFS-M1-DOC-003)
├── 01-product-architecture/
│   ├── 04-PFS-PRODUCT-ARCHITECTURE.md                 (PFS-M1-DOC-004)
│   ├── 05-SYSTEM-CONTEXT-AND-STAKEHOLDERS.md          (PFS-M1-DOC-005)
│   └── 06-CAPABILITY-ARCHITECTURE.md                  (PFS-M1-DOC-006)
├── 02-domain-architecture/
│   ├── 07-UNIVERSAL-DOMAIN-MODEL.md                   (PFS-M1-DOC-007)
│   ├── 08-PROJECT-AND-FOUNDATION-LIFECYCLE.md         (PFS-M1-DOC-008)
│   ├── 09-REQUIREMENT-DECISION-AND-TRACEABILITY.md    (PFS-M1-DOC-009)
│   └── 10-ARTIFACT-KNOWLEDGE-AND-VERSIONING.md        (PFS-M1-DOC-010)
├── 03-system-architecture/
│   ├── 11-LOGICAL-ARCHITECTURE.md                     (PFS-M1-DOC-011)
│   ├── 12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md       (PFS-M1-DOC-012)
│   ├── 13-CORE-AND-APPLICATION-ARCHITECTURE.md        (PFS-M1-DOC-013)
│   └── 14-APPLICATION-CONTRACTS-AND-EVENTS.md         (PFS-M1-DOC-014)
├── 04-execution-architecture/
│   ├── 15-WORKFLOW-AND-STATE-MACHINES.md              (PFS-M1-DOC-015)
│   ├── 16-AGENT-ORCHESTRATION-ARCHITECTURE.md         (PFS-M1-DOC-016)
│   ├── 17-AI-PROVIDER-AND-TOOL-ADAPTERS.md            (PFS-M1-DOC-017)
│   └── 18-GENERATION-AND-RECOVERY-ARCHITECTURE.md     (PFS-M1-DOC-018)
├── 05-trust-and-quality/
│   ├── 19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md (PFS-M1-DOC-019)
│   ├── 20-SECURITY-THREAT-MODEL.md                    (PFS-M1-DOC-020)
│   ├── 21-QUALITY-AND-EVIDENCE-ARCHITECTURE.md        (PFS-M1-DOC-021)
│   └── 22-DATA-PRIVACY-AND-SUPPLY-CHAIN.md            (PFS-M1-DOC-022)
├── 06-platform-operations/
│   ├── 23-DEPLOYMENT-AND-OPERATIONS-ARCHITECTURE.md   (PFS-M1-DOC-023)
│   ├── 24-API-CLI-AND-USER-INTERFACE-ARCHITECTURE.md  (PFS-M1-DOC-024)
│   └── 25-OBSERVABILITY-AND-RELIABILITY.md            (PFS-M1-DOC-025)
├── 07-delivery/
│   ├── 26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md     (PFS-M1-DOC-026)
│   ├── 27-M1-ACCEPTANCE-CRITERIA.md                   (PFS-M1-DOC-027)
│   └── 28-M1-FINAL-ARCHITECTURE-REVIEW.md             (PFS-M1-DOC-028)
├── decisions/                                         (ADR-001 to ADR-020)
├── diagrams/                                          (DIA-001 to DIA-016)
├── schemas/                                           (Core JSON Schemas)
├── contracts/                                         (API & Trait Contracts)
├── matrices/                                          (Completeness & Traceability)
├── threat-model/                                      (STRIDE-AI Catalog)
├── reports/                                           (Validation & Review Reports)
└── registry/                                          (CSV & MD Registries)
```

---

## 3. Authoritative Document Catalog (29 Core Deliverables)

| Index | Document ID | Tên tài liệu | Phân hệ | Đường dẫn |
|---|---|---|---|---|
| 00 | PFS-M1-DOC-000 | Architecture Index & Master Package Registry | Governance | [00-M1-INDEX.md](file:///C:/Users/OK259/rust/docs/M1-architecture/00-governance/00-M1-INDEX.md) |
| 01 | PFS-M1-DOC-001 | Scope and System Boundaries | Governance | [01-M1-SCOPE-AND-BOUNDARIES.md](file:///C:/Users/OK259/rust/docs/M1-architecture/00-governance/01-M1-SCOPE-AND-BOUNDARIES.md) |
| 02 | PFS-M1-DOC-002 | Architecture Method and Standards Basis | Governance | [02-M1-ARCHITECTURE-METHOD.md](file:///C:/Users/OK259/rust/docs/M1-architecture/00-governance/02-M1-ARCHITECTURE-METHOD.md) |
| 03 | PFS-M1-DOC-003 | Global Architecture Requirements Specification | Governance | [03-ARCHITECTURE-REQUIREMENTS.md](file:///C:/Users/OK259/rust/docs/M1-architecture/00-governance/03-ARCHITECTURE-REQUIREMENTS.md) |
| 04 | PFS-M1-DOC-004 | PFS Product Architecture & Layered Engine | Product Architecture | [04-PFS-PRODUCT-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/01-product-architecture/04-PFS-PRODUCT-ARCHITECTURE.md) |
| 05 | PFS-M1-DOC-005 | System Context and Stakeholder Concerns | Product Architecture | [05-SYSTEM-CONTEXT-AND-STAKEHOLDERS.md](file:///C:/Users/OK259/rust/docs/M1-architecture/01-product-architecture/05-SYSTEM-CONTEXT-AND-STAKEHOLDERS.md) |
| 06 | PFS-M1-DOC-006 | Capability Architecture & Dynamic Registry | Product Architecture | [06-CAPABILITY-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/01-product-architecture/06-CAPABILITY-ARCHITECTURE.md) |
| 07 | PFS-M1-DOC-007 | Universal Domain Model & Domain Test Profiles | Domain Architecture | [07-UNIVERSAL-DOMAIN-MODEL.md](file:///C:/Users/OK259/rust/docs/M1-architecture/02-domain-architecture/07-UNIVERSAL-DOMAIN-MODEL.md) |
| 08 | PFS-M1-DOC-008 | Project and Foundation Lifecycle Model | Domain Architecture | [08-PROJECT-AND-FOUNDATION-LIFECYCLE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/02-domain-architecture/08-PROJECT-AND-FOUNDATION-LIFECYCLE.md) |
| 09 | PFS-M1-DOC-009 | Requirement, Decision and Traceability Architecture | Domain Architecture | [09-REQUIREMENT-DECISION-AND-TRACEABILITY.md](file:///C:/Users/OK259/rust/docs/M1-architecture/02-domain-architecture/09-REQUIREMENT-DECISION-AND-TRACEABILITY.md) |
| 10 | PFS-M1-DOC-010 | Artifact, Knowledge and Versioning Architecture | Domain Architecture | [10-ARTIFACT-KNOWLEDGE-AND-VERSIONING.md](file:///C:/Users/OK259/rust/docs/M1-architecture/02-domain-architecture/10-ARTIFACT-KNOWLEDGE-AND-VERSIONING.md) |
| 11 | PFS-M1-DOC-011 | Logical Architecture & Subsystem Boundaries | System Architecture | [11-LOGICAL-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/03-system-architecture/11-LOGICAL-ARCHITECTURE.md) |
| 12 | PFS-M1-DOC-012 | Module Catalog and Dependency Architecture | System Architecture | [12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/03-system-architecture/12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md) |
| 13 | PFS-M1-DOC-013 | PFS Core and Application Architecture (Rust) | System Architecture | [13-CORE-AND-APPLICATION-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/03-system-architecture/13-CORE-AND-APPLICATION-ARCHITECTURE.md) |
| 14 | PFS-M1-DOC-014 | Application Contracts, Commands, Queries & Events | System Architecture | [14-APPLICATION-CONTRACTS-AND-EVENTS.md](file:///C:/Users/OK259/rust/docs/M1-architecture/03-system-architecture/14-APPLICATION-CONTRACTS-AND-EVENTS.md) |
| 15 | PFS-M1-DOC-015 | Workflow Architecture & State Machines | Execution Architecture | [15-WORKFLOW-AND-STATE-MACHINES.md](file:///C:/Users/OK259/rust/docs/M1-architecture/04-execution-architecture/15-WORKFLOW-AND-STATE-MACHINES.md) |
| 16 | PFS-M1-DOC-016 | Agent Orchestration & Task Execution Architecture | Execution Architecture | [16-AGENT-ORCHESTRATION-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/04-execution-architecture/16-AGENT-ORCHESTRATION-ARCHITECTURE.md) |
| 17 | PFS-M1-DOC-017 | AI Provider Gateway and Tool Adapters | Execution Architecture | [17-AI-PROVIDER-AND-TOOL-ADAPTERS.md](file:///C:/Users/OK259/rust/docs/M1-architecture/04-execution-architecture/17-AI-PROVIDER-AND-TOOL-ADAPTERS.md) |
| 18 | PFS-M1-DOC-018 | Foundation Generator and Recovery Architecture | Execution Architecture | [18-GENERATION-AND-RECOVERY-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/04-execution-architecture/18-GENERATION-AND-RECOVERY-ARCHITECTURE.md) |
| 19 | PFS-M1-DOC-019 | Governance, Policy & Authorization Architecture | Trust and Quality | [19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/05-trust-and-quality/19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md) |
| 20 | PFS-M1-DOC-020 | Security Architecture & STRIDE Threat Model | Trust and Quality | [20-SECURITY-THREAT-MODEL.md](file:///C:/Users/OK259/rust/docs/M1-architecture/05-trust-and-quality/20-SECURITY-THREAT-MODEL.md) |
| 21 | PFS-M1-DOC-021 | Quality Engine, Gates & Evidence Architecture | Trust and Quality | [21-QUALITY-AND-EVIDENCE-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/05-trust-and-quality/21-QUALITY-AND-EVIDENCE-ARCHITECTURE.md) |
| 22 | PFS-M1-DOC-022 | Data Privacy, Classification & Supply Chain | Trust and Quality | [22-DATA-PRIVACY-AND-SUPPLY-CHAIN.md](file:///C:/Users/OK259/rust/docs/M1-architecture/05-trust-and-quality/22-DATA-PRIVACY-AND-SUPPLY-CHAIN.md) |
| 23 | PFS-M1-DOC-023 | Deployment Topology and Operations Architecture | Platform Operations | [23-DEPLOYMENT-AND-OPERATIONS-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/06-platform-operations/23-DEPLOYMENT-AND-OPERATIONS-ARCHITECTURE.md) |
| 24 | PFS-M1-DOC-024 | Interface Architecture: CLI, API & Web/Desktop | Platform Operations | [24-API-CLI-AND-USER-INTERFACE-ARCHITECTURE.md](file:///C:/Users/OK259/rust/docs/M1-architecture/06-platform-operations/24-API-CLI-AND-USER-INTERFACE-ARCHITECTURE.md) |
| 25 | PFS-M1-DOC-025 | Observability, Telemetry and System Reliability | Platform Operations | [25-OBSERVABILITY-AND-RELIABILITY.md](file:///C:/Users/OK259/rust/docs/M1-architecture/06-platform-operations/25-OBSERVABILITY-AND-RELIABILITY.md) |
| 26 | PFS-M1-DOC-026 | Implementation Blueprint, Crates & Backlog | Delivery | [26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md](file:///C:/Users/OK259/rust/docs/M1-architecture/07-delivery/26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md) |
| 27 | PFS-M1-DOC-027 | Milestone M1 Acceptance Criteria & Verification | Delivery | [27-M1-ACCEPTANCE-CRITERIA.md](file:///C:/Users/OK259/rust/docs/M1-architecture/07-delivery/27-M1-ACCEPTANCE-CRITERIA.md) |
| 28 | PFS-M1-DOC-028 | Independent Architecture Review & Assessment | Delivery | [28-M1-FINAL-ARCHITECTURE-REVIEW.md](file:///C:/Users/OK259/rust/docs/M1-architecture/07-delivery/28-M1-FINAL-ARCHITECTURE-REVIEW.md) |

---

## 4. Supporting Artifacts Registry

### 4.1. Architecture Decision Records (ADR Catalog)

Toàn bộ 20 quyết định kiến trúc chiến lược được lưu trữ tại `docs/M1-architecture/decisions/`:
- **ADR-001:** PFS System Topology (Modular Monolith with Out-of-Process Sidecars).
- **ADR-002:** Core Architectural Style (Clean Hexagonal Architecture with Ports & Adapters).
- **ADR-003:** Module Boundary and Strict Dependency Inversion Rules.
- **ADR-004:** Universal Domain Identity and ULID/UUIDv7 Specification.
- **ADR-005:** Multi-Tenancy, Hierarchy and Scope Isolation Model.
- **ADR-006:** Dynamic Capability Registry and Plugin Extension Model.
- **ADR-007:** Domain Persistence Strategy (Embedded SQLite / PostgreSQL Dual Driver via SQLx).
- **ADR-008:** Content-Addressed Artifact Storage and Merkle Versioning.
- **ADR-009:** Workflow State Engine and Deterministic Saga Orchestration.
- **ADR-010:** In-Memory / Broker-Agnostic Asynchronous Eventing Architecture.
- **ADR-011:** Multi-Agent Coordination Protocol and Conflict Arbitration.
- **ADR-012:** Provider-Agnostic LLM Gateway Contract and Model Switching.
- **ADR-013:** Tool Execution Gateway, WASM / Native Container Sandbox.
- **ADR-014:** Deterministic L0–L5 Authorization Enforcement Engine.
- **ADR-015:** Human-in-the-Loop Explicit Approval & Signature Workflow.
- **ADR-016:** Hierarchical Quality Gate Engine and Evidence Validation.
- **ADR-017:** Idempotent Foundation Generator with Staged Atomic Commit.
- **ADR-018:** Unified Business Semantics across CLI, REST API and Agent Tools.
- **ADR-019:** Multi-Platform Distribution, Packaging and Zero-Downtime Migration.
- **ADR-020:** Structured Telemetry, OpenTelemetry Tracing and Error Categorization.

### 4.2. Architecture Diagrams (16 Canonical Diagrams)

Các sơ đồ kiến trúc chuẩn hóa (Mermaid syntax) được lưu trữ tại `docs/M1-architecture/diagrams/`:
1. `DIA-001-system-context.mmd`: PFS System Context.
2. `DIA-002-capability-map.mmd`: PFS Product Capability Map.
3. `DIA-003-c4-container.mmd`: C4 Container Diagram.
4. `DIA-004-c4-component.mmd`: C4 Component Diagram (PFS Core Crates).
5. `DIA-005-dependency-graph.mmd`: Core Dependency & Crate Hierarchy.
6. `DIA-006-universal-domain-model.mmd`: Universal Domain Entity-Relationship Model.
7. `DIA-007-foundation-lifecycle.mmd`: 11-Stage Project Foundation Lifecycle.
8. `DIA-008-workflow-state-machine.mmd`: Foundation Workflow Execution State Machine.
9. `DIA-009-agent-task-sequence.mmd`: Multi-Agent Task Planning & Execution Sequence.
10. `DIA-010-governance-approval-sequence.mmd`: Authority & Approval Protocol Sequence.
11. `DIA-011-artifact-provenance-graph.mmd`: Artifact Provenance & Traceability Merkle DAG.
12. `DIA-012-generator-sequence.mmd`: Staged Foundation Generation & Recovery Sequence.
13. `DIA-013-security-trust-boundary.mmd`: Security Trust Boundaries & Attack Surfaces.
14. `DIA-014-deployment-topology.mmd`: Production Deployment Topology.
15. `DIA-015-data-flow-diagram.mmd`: End-to-End Data Flow (Intent to Foundation Package).
16. `DIA-016-failure-recovery-flow.mmd`: Failure Detection, Circuit Breaker & Compensation Flow.

---

## 5. Governance & Review Protocol

Tài liệu M1 này tuân thủ các nguyên tắc quản trị cao nhất:
1. **Trạng thái đề xuất:** Mọi tài liệu M1 ban đầu có trạng thái `Proposed — Ready for Owner Review`.
2. **Quyền nghiệm thu:** Chỉ duy nhất Project Owner mới có thẩm quyền chuyển trạng thái M1 sang `Accepted`. Tuyệt đối không tự phong quyền hoặc giả định phê duyệt.
3. **Traceability:** Mọi yêu cầu kỹ thuật của M1 đều truy vết trực tiếp về M0 Specification (`PFS-M0-SPEC-001..015`) và Project Owner Decisions (`PFS-M0-OWNER-DECISIONS-001`, `PFS-M0-OWNER-DECISIONS-002`).
4. **Validation Tooling:** Được kiểm tra tự động bằng `tools/validation/validate_m1.py` nhằm đảm bảo tính toàn vẹn 100% của tài liệu, liên kết, schema và logic phụ thuộc.
