# PFS-M1-DOC-011 — Logical Architecture & Subsystem Boundaries

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-011 |
| Document Title | Logical Architecture and Subsystem Boundaries Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Hexagonal Architecture, Onion Architecture, Subsystem Decomposition |
| Related Decisions | ADR-001, ADR-002, ADR-003 |

---

## 1. Logical Architecture Design Principles

Kiến trúc logic của **Project Foundation System (PFS)** được xây dựng nhằm giải quyết bài toán cốt lõi: kết hợp sự linh hoạt của mô hình AI với sự chắc chắn, xác định và an toàn của hệ thống kỹ thuật phần mềm cốt lõi.

Kiến trúc logic tuân thủ nghiêm ngặt 5 nguyên tắc cấu trúc:
1. **Separation of Concerns (SoC):** Mỗi phân hệ logic (Subsystem) chỉ chịu trách nhiệm duy nhất cho một miền nghiệp vụ chuyên biệt.
2. **Strict Dependency Rule (Onion Principle):** Các phân hệ ở tầng trong (Domain Core) tuyệt đối không có kiến thức hoặc phụ thuộc vào các phân hệ ở tầng ngoài (Application, Infrastructure, UI).
3. **High Cohesion & Low Coupling:** Tối đa hóa tính gắn kết nội bộ module và tối thiểu hóa sự phụ thuộc chéo giữa các modules.
4. **Boundary by Contracts:** Giao tiếp xuyên ranh giới giữa các phân hệ logic bắt buộc phải thông qua **Trait Interfaces**, **Data Transfer Objects (DTOs)**, **Commands**, **Queries** hoặc **Typed Events** được định nghĩa bằng kiểu dữ liệu mạnh trong Rust.
5. **No Shared Mutable State:** Tuyệt đối không chia sẻ trạng thái có thể thay đổi (mutable state) giữa các phân hệ; toàn bộ tương tác đều qua lời gọi hàm bất đồng bộ hoặc thông điệp.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PFS Logical Subsystem Onion                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ INFRASTRUCTURE & ADAPTERS ]                                              │
│  ├── AI Provider Gateways (OpenAI, Anthropic, vLLM)                         │
│  ├── Persistence Drivers (SQLite, PostgreSQL via SQLx)                      │
│  ├── Filesystem CAS & Staging Storage                                       │
│  └── External Tool Sandbox (WASM / Isolated Subprocess)                     │
│       │                                                                     │
│       ▼ implements ports                                                    │
│  [ APPLICATION & ORCHESTRATION SERVICES ]                                   │
│  ├── Workflow Saga Coordinator                                              │
│  ├── Multi-Agent Task Planner & Router                                      │
│  ├── Governance & Approval Coordinator                                      │
│  └── Staged Foundation Generation Pipeline                                  │
│       │                                                                     │
│       ▼ coordinates                                                         │
│  [ DOMAIN CORE SERVICES & AGGREGATES ] (Pure Rust, Zero Ext Dependencies)   │
│  ├── Project & Capability Domain                                            │
│  ├── Requirement & Decision DAG Domain                                      │
│  ├── Governance, Policy & Authorization Domain (L0–L5)                      │
│  ├── Quality Gate & Evidence Domain                                         │
│  └── Artifact, Knowledge & Merkle DAG Domain                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Decomposition into Major Subsystems

Hệ thống PFS được phân rã logic thành 6 Phân hệ Lớn (Subsystems):

### 2.1. Project & Intent Subsystem (PIS)
- **Ranh giới trách nhiệm:** Tiếp nhận, chuẩn hóa và mô hình hóa Project Intent từ người dùng; quản lý cấu hình Project Profile; giải quyết danh mục Capabilities.
- **Ranh giới không đảm nhiệm:** Không thực thi workflow; không trực tiếp sinh tài liệu; không gọi LLM trực tiếp.
- **Thực thể chủ quản:** `Project`, `ProjectIntent`, `ProjectProfile`, `ProjectContext`, `Capability`, `CapabilityProfile`.

### 2.2. Requirements & Governance Subsystem (RGS)
- **Ranh giới trách nhiệm:** Xây dựng mạng lưới đồ thị có hướng (DAG) cho Requirements, Constraints, Assumptions, Risks; quản lý quyết định kiến trúc (ADRs); thực thi chính sách phân quyền L0–L5 và quản lý quy trình phê duyệt (Approval Workflows).
- **Ranh giới không đảm nhiệm:** Không trực tiếp tạo tệp tin trên ổ đĩa; không quản lý kết nối cơ sở dữ liệu.
- **Thực thể chủ quản:** `Requirement`, `Constraint`, `Assumption`, `Decision`, `Policy`, `Role`, `Authority`, `Approval`.

### 2.3. Workflow & Orchestration Subsystem (WOS)
- **Ranh giới trách nhiệm:** Điều phối việc chuyển đổi trạng thái qua 11 giai đoạn vòng đời; lập kế hoạch phân rã nhiệm vụ (Task Planning); định tuyến nhiệm vụ cho AI Agents; xử lý phục hồi khi gặp sự cố (Saga Compensation).
- **Ranh giới không đảm nhiệm:** Không chứa business logic của từng giai đoạn; chỉ quản lý trạng thái và luồng thực thi.
- **Thực thể chủ quản:** `FoundationStage`, `Workflow`, `WorkflowExecution`, `Task`, `ExecutionRecord`.

### 2.4. Agent & Tooling Subsystem (ATS)
- **Ranh giới trách nhiệm:** Quản lý hồ sơ Agent Profiles; điều phối giao tiếp với các AI Providers qua lớp Gateway; thực thi công cụ trong môi trường Sandbox cô lập; giám sát chi phí token và giới hạn tỷ lệ (Rate Limiting).
- **Ranh giới không đảm nhiệm:** Không tự ý đưa ra quyết định kiến trúc; không được tự nâng quyền L0–L2 lên L3+.
- **Thực thể chủ quản:** `Agent`, `AgentProfile`, `ProviderAdapter`, `ToolContract`, `SandboxSession`.

### 2.5. Artifact & Generation Subsystem (AGS)
- **Ranh giới trách nhiệm:** Quản lý kho tạo tác Content-Addressed Storage (CAS); duy trì cây phả hệ Merkle DAG; thực thi quy trình sinh Foundation 4 bước an toàn (Staging → Dry-run Preview → Conflict Detection → Atomic Commit).
- **Ranh giới không đảm nhiệm:** Không phê duyệt chất lượng; không tự quyết định ghi đè tệp tin khi có xung đột.
- **Thực thể chủ quản:** `Artifact`, `ArtifactVersion`, `Template`, `TemplateVersion`, `GenerationPlan`, `OwnershipManifest`.

### 2.6. Quality & Verification Subsystem (QVS)
- **Ranh giới trách nhiệm:** Quản lý các Cổng chất lượng (Quality Gates); thu thập và xác thực bằng chứng (Evidence Validation); ghi nhận các phát hiện (Findings, Defects, Risks); kiểm tra tính toàn vẹn của chuỗi truy vết hai chiều.
- **Ranh giới không đảm nhiệm:** Không cấp quyền ngoại lệ (Waivers) nếu thiếu chữ ký số của thẩm quyền con người.
- **Thực thể chủ quản:** `QualityGate`, `Evidence`, `Finding`, `ExceptionWaiver`, `AuditLedger`.

---

## 3. Subsystem Interaction and Coupling Analysis

Để bảo đảm tính ổn định và khả năng bảo trì lâu dài, mức độ phụ thuộc giữa các phân hệ được thiết kế theo các chỉ số đo lường kiến trúc chuẩn:
- **Afferent Coupling ($C_a$):** Số lượng phân hệ bên ngoài phụ thuộc vào phân hệ hiện tại.
- **Efferent Coupling ($C_e$):** Số lượng phân hệ bên ngoài mà phân hệ hiện tại phụ thuộc vào.
- **Instability Metric ($I = \frac{C_e}{C_a + C_e}$):** Giá trị từ 0 (Hoàn toàn Ổn định) đến 1 (Rất Linh hoạt/Dễ biến động).

| Phân hệ logic | $C_a$ (Được phụ thuộc) | $C_e$ (Phụ thuộc ngoài) | Độ mất ổn định ($I$) | Đánh giá kiến trúc |
|---|---|---|---|---|
| **Domain Core (RGS, PIS)** | Cao (5) | Thấp (0) | $0.00$ (Maximally Stable) | Lõi ổn định tuyệt đối; không đổi khi công nghệ ngoài đổi. |
| **Artifact & Storage (AGS)** | Trung bình (3) | Thấp (1) | $0.25$ (Stable) | Ổn định cao; chỉ phụ thuộc vào Core Domain. |
| **Quality & Audit (QVS)** | Trung bình (3) | Thấp (1) | $0.25$ (Stable) | Ổn định cao; kiểm định dựa trên các thực thể Core. |
| **Workflow Engine (WOS)** | Trung bình (2) | Trung bình (3) | $0.60$ (Balanced) | Đóng vai trò nhạc trưởng điều phối các phân hệ khác. |
| **Agent & Providers (ATS)** | Thấp (1) | Cao (4) | $0.80$ (Flexible) | Rất linh hoạt; dễ dàng thay thế adapter các model AI mới. |
| **Experience Layer (UI/CLI)** | Thấp (0) | Cao (5) | $1.00$ (Maximally Volatile) | Linh hoạt tuyệt đối; thay đổi giao diện không ảnh hưởng Core. |

---

## 4. Boundary Protection & Anti-Corruption Layers (ACL)

Để ngăn chặn việc các khái niệm kỹ thuật của các bên thứ ba (như cấu trúc JSON đặc thù của OpenAI, định dạng bảng của PostgreSQL, hoặc cấu trúc tệp của hệ điều hành) làm ô nhiễm mô hình nghiệp vụ:
1. **AI Provider Anti-Corruption Layer:** Mọi cấu trúc dữ liệu trả về từ OpenAI (JSON response, tool calls) được chuyển đổi ngay lập tức thành `UniversalAgentResponse` chuẩn của PFS trước khi đi vào Core Engine.
2. **Storage Anti-Corruption Layer:** Các kiểu dữ liệu cơ sở dữ liệu (`sqlx::Row`, `sqlite3_stmt`) được bao bọc trong `RepositoryTrait` và ánh xạ thành Pure Rust Domain Structs.
3. **Filesystem Anti-Corruption Layer:** Mọi thao tác đường dẫn tệp tin đều được chuẩn hóa thành `NormalizedPathUri` (sử dụng dấu `/` chuẩn, loại bỏ các ký tự điều khiển và ngăn chặn triệt để lỗ hổng Path Traversal `../`).
