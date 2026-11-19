# PFS-M1-DOC-003 — Global Architecture Requirements Specification

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-003 |
| Document Title | Global Architecture Requirements Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Parent Baseline | [requirement-registry.csv](file:///C:/Users/OK259/rust/docs/M0-foundation/registry/requirement-registry.csv), [PFS-M0-SPEC-014](file:///C:/Users/OK259/rust/docs/M0-foundation/14-M0-ACCEPTANCE-CRITERIA.md) |

---

## 1. Purpose and Namespace Architecture

Tài liệu này xác lập Danh mục Yêu cầu Kiến trúc Toàn cục (Global Architecture Requirement Registry) cho Milestone M1, thiết lập cầu nối truy vết hai chiều (Bidirectional Traceability) giữa các yêu cầu nền tảng của M0 và các giải pháp kiến trúc chi tiết của M1, chuẩn bị sẵn sàng cho việc kiểm thử và triển khai trong M2–M4.

### 1.1. Quy ước Namespace và Mã hóa Yêu cầu M1

Để bảo đảm tính duy nhất và không gây xung đột với 168 yêu cầu đã được xác lập tại M0 (`PFS-VIS`, `M0-PROD`, `M0-UNI`, `M0-MTH`, `M0-GOV`, `M0-AUT`, `M0-ART`, `M0-HYB`, `M0-SEC-AG`, `M0-QLT`, `M0-VER`, `M0-SC`, `M0-RDM`, `M0-REV`), Milestone M1 áp dụng quy ước namespace có cấu trúc tiền tố chuẩn `M1-` kết hợp với mã phân hệ nghiệp vụ:

| Namespace Phân hệ | Lĩnh vực chuyên môn | Dải số định danh | Tài liệu kiến trúc chủ quản |
|---|---|---|---|
| **M1-PROD** | Product & Capability Architecture | `M1-PROD-001` .. `M1-PROD-020` | `04-PFS-PRODUCT-ARCHITECTURE.md`, `06-CAPABILITY-ARCHITECTURE.md` |
| **M1-DOM** | Universal Domain Model & Lifecycle | `M1-DOM-001` .. `M1-DOM-025` | `07-UNIVERSAL-DOMAIN-MODEL.md`, `08-PROJECT-AND-FOUNDATION-LIFECYCLE.md` |
| **M1-SYS** | Logical & Core Module Architecture | `M1-SYS-001` .. `M1-SYS-025` | `11-LOGICAL-ARCHITECTURE.md`, `12-MODULE-AND-DEPENDENCY-ARCHITECTURE.md` |
| **M1-EXE** | Workflow, Agent & Generation Engine | `M1-EXE-001` .. `M1-EXE-025` | `15-WORKFLOW-AND-STATE-MACHINES.md`, `16-AGENT-ORCHESTRATION-ARCHITECTURE.md` |
| **M1-SEC** | Governance, Security & Supply Chain | `M1-SEC-001` .. `M1-SEC-025` | `19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md`, `20-SECURITY-THREAT-MODEL.md` |
| **M1-OPS** | Deployment, Operations & Reliability | `M1-OPS-001` .. `M1-OPS-020` | `23-DEPLOYMENT-AND-OPERATIONS-ARCHITECTURE.md`, `25-OBSERVABILITY-AND-RELIABILITY.md` |
| **M1-IMP** | Implementation Blueprint & Backlog | `M1-IMP-001` .. `M1-IMP-020` | `26-IMPLEMENTATION-BLUEPRINT-AND-BACKLOG.md`, `27-M1-ACCEPTANCE-CRITERIA.md` |

---

## 2. Core Architecture Requirements Catalog

Dưới đây là các yêu cầu kiến trúc mang tính sống còn được chuẩn hóa cho PFS Core:

### 2.1. Phân hệ Product & Capability (M1-PROD)

- **M1-PROD-001 (Universal Intake):** Hệ thống phải có khả năng tiếp nhận Project Intent dưới nhiều hình thức: câu lệnh vắn tắt, tài liệu mô tả thô, bộ câu hỏi cấu trúc hoặc phỏng vấn tương tác.
- **M1-PROD-002 (Domain Agnostic Core):** Lõi phân tích của PFS không được giả định rằng mọi dự án đều có source code, API hoặc database; hỗ trợ cấu hình đa miền thông qua Capability Profiles.
- **M1-PROD-003 (Dynamic Capability Registry):** Hệ thống phải cung cấp Capability Catalog có thể mở rộng động, hỗ trợ các trạng thái áp dụng: Required, Optional, Conditional, Not Applicable (kèm rationale) và Custom Extension.
- **M1-PROD-004 (Layered Separation):** Kiến trúc phải tách biệt tuyệt đối 4 tầng: Experience Layer, Application & Orchestration Layer, Domain Core Layer, Infrastructure & Adapter Layer. UI tuyệt đối không chứa business rules.

### 2.2. Phân hệ Universal Domain & Lifecycle (M1-DOM)

- **M1-DOM-001 (Entity Identity & Scope):** Mọi thực thể nghiệp vụ (Project, Requirement, Decision, Task, Artifact) phải có định danh toàn cầu duy nhất (ULID/UUIDv7), phân biệt rạch ròi giữa ID hệ thống, display name và đường dẫn lưu trữ.
- **M1-DOM-002 (11-Stage Workflow Preservation):** Kiến trúc bắt buộc phải hiện thực hóa đầy đủ vòng đời 11 giai đoạn kế thừa từ M0: `Initialize → Discover → Requirements → Architecture → Governance → Documentation → Agents → Quality → Bootstrap → Audit → Baseline`.
- **M1-DOM-003 (Bidirectional Traceability Linkage):** Hệ thống phải duy trì đường liên kết truy vết bất biến: `Intent → Requirement → Decision → Task → Artifact → Evidence → Quality Gate → Foundation Package`.
- **M1-DOM-004 (Immutable Artifact Provenance):** Mỗi Artifact Version phải lưu trữ đầy đủ thông tin nguồn gốc: ai tạo, công cụ/template nào, mô hình LLM nào, chính sách áp dụng, mã hash nội dung và quan hệ kế thừa (Derived-from).

### 2.3. Phân hệ System & Module Architecture (M1-SYS)

- **M1-SYS-001 (Rust Core Modular Monolith):** PFS Core phải được đóng gói theo mô hình Modular Monolith bằng Rust, phân rã thành các crate độc lập với ranh giới rõ ràng, không có cyclic dependency (ADR-001, ADR-003).
- **M1-SYS-002 (Dependency Inversion & Ports/Adapters):** Domain Core tuyệt đối không phụ thuộc vào hạ tầng bên ngoài, cơ sở dữ liệu cụ thể hay SDK của AI provider. Mọi phụ thuộc ngoại vi phải thông qua abstraction traits (ADR-002).
- **M1-SYS-003 (Unified Command/Query/Event Contracts):** Toàn bộ tương tác nghiệp vụ nội bộ phải tuân thủ nghiêm ngặt hợp đồng Command, Query và Typed Events. Query phải bảo đảm tính read-only đối với trạng thái nghiệp vụ.
- **M1-SYS-004 (Dual Persistence Backend):** Hệ thống phải hỗ trợ backend lưu trữ SQLite nhúng cho chế độ single-user/local CLI và PostgreSQL cho chế độ multi-user/team daemon thông qua abstraction layer SQLx (ADR-007).

### 2.4. Phân hệ Execution, Agent & Generation (M1-EXE)

- **M1-EXE-001 (Deterministic Workflow Engine):** Trạng thái workflow được điều phối bởi State Machine xác định trong Rust, bảo đảm tính khôi phục khi có sự cố, phát hiện thực thi trùng lặp và hỗ trợ saga compensation (ADR-009).
- **M1-EXE-002 (Provider-Agnostic LLM Gateway):** Kiến trúc phải có lớp Gateway trừu tượng hóa cho các AI Provider, hỗ trợ streaming, structured output (JSON Schema), token budgeting, circuit breaker và fallback tự động (ADR-012).
- **M1-EXE-003 (Isolated Tool Sandbox):** Mọi công cụ do Agent gọi (filesystem, shell, network) phải được thực thi trong môi trường Sandbox cách ly (WASM / Docker Container / Subprocess restricted), tuân thủ nghiêm ngặt allowlist (ADR-013).
- **M1-EXE-004 (Safe Idempotent Generation):** Quá trình sinh Foundation Package phải tuân thủ quy trình 4 bước: Staging → Dry-run Preview → Conflict Detection → Atomic Commit. Nghiêm cấm tự ý ghi đè file của người dùng khi chưa có sự xác nhận tường minh (ADR-017).

### 2.5. Phân hệ Governance, Security & Quality (M1-SEC)

- **M1-SEC-001 (L0–L5 Authorization Engine):** Thực thi mô hình phân quyền tối thiểu (Least Privilege) và deny-by-default: L0 (Read-only), L1 (Analyze/Propose), L2 (Draft Artifacts), L3 (Modify Files), L4 (Execute Approved Ops), L5 (Privileged/Destructive) (ADR-014).
- **M1-SEC-002 (Human-in-the-Loop Explicit Approval):** AI Agent tuyệt đối không có quyền tự phê duyệt các quyết định kiến trúc, thay đổi policy hoặc kích hoạt thao tác L4/L5; bắt buộc phải có chữ ký số/xác nhận của con người (ADR-015).
- **M1-SEC-003 (Data Classification & Secret Redaction):** Hệ thống phải phân loại dữ liệu theo 4 cấp độ (Public, Internal, Confidential, Restricted) và tự động làm sạch (redact) thông tin mật/secrets trước khi gửi sang bất kỳ AI Provider nào (INV-11).
- **M1-SEC-004 (Hierarchical Quality Gates):** Mỗi giai đoạn dự án phải được kiểm tra qua các Cổng chất lượng xác định; lỗi nghiêm trọng (Critical Finding) không được phép bù đắp bằng điểm trung bình; chặn chuyển giai đoạn nếu chưa có ngoại lệ hợp lệ (ADR-016).

### 2.6. Phân hệ Operations, Reliability & Delivery (M1-OPS & M1-IMP)

- **M1-OPS-001 (Zero-Downtime Migration & Versioning):** Hỗ trợ tương thích ngược cho dữ liệu dự án, schemas và foundation packages; có cơ chế database migration tự động và an toàn (ADR-019).
- **M1-OPS-002 (Unified Telemetry & Audit Trail):** Ghi nhật ký có cấu trúc (Structured Logging), chỉ số hiệu năng (Metrics) và phân tán dấu vết (Tracing) chuẩn OpenTelemetry; lưu vết kiểm toán bất biến (ADR-020).
- **M1-IMP-001 (Crate Architecture & Build Plan):** Mã nguồn PFS Core phải được phân rã thành tối thiểu 8 crates chính trong một Cargo Workspace, tuân thủ thứ tự xây dựng nghiêm ngặt từ rễ phụ thuộc lên đỉnh ứng dụng.
- **M1-IMP-002 (Executable Vertical Slice):** Cung cấp đặc tả kịch bản Vertical Slice đầu tiên: *Tạo lập Minimal Project Foundation từ Project Intent* để kiểm chứng toàn bộ luồng tích hợp từ Core đến CLI trong M2.

---

## 3. Bidirectional Traceability Framework

Mỗi yêu cầu trong Danh mục Yêu cầu Kiến trúc Toàn cục M1 được ánh xạ hai chiều theo mô hình liên kết:

$$\mathbf{M0\ Requirement} \iff \mathbf{M1\ Architecture\ Requirement} \iff \mathbf{ADR} \iff \mathbf{Module/Crate} \iff \mathbf{Contract/Schema} \iff \mathbf{Acceptance\ Criteria}$$

Toàn bộ dữ liệu chi tiết của 60+ yêu cầu kiến trúc M1 được biên soạn trong cơ sở dữ liệu `docs/M1-architecture/registry/m1-requirement-registry.csv` và ma trận đối soát `docs/M1-architecture/matrices/m1-traceability-matrix.csv`.
