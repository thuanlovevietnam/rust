# PFS-M1-DOC-026 — Implementation Blueprint, Crates Breakdown and Backlog

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-026 |
| Document Title | Implementation Blueprint, Crates Breakdown and Backlog Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.1.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Engineering Lead |
| Classification | Internal |
| Target Implementation Stack | Rust (Edition 2021 / 2024 Stable, Cargo Workspace) |
| Target Milestones | M2 (Agent System & Vertical Slice), M3 (Quality Gates), M4 (Generator Automation & Production) |
| Related Decisions | ADR-001, ADR-002, ADR-003, ADR-007, ADR-012, ADR-013, ADR-014, ADR-017 |
| Invariant Reference | INV-01, INV-02, INV-03, INV-06, INV-08 |
| Audit Remediation | Resolved finding FND-M1-05 (Journal-Based Commit), FND-M1-06 (M2 Minimal vs M4 Full Generator), and M2 Work Packages Readiness |

---

## 1. Executive Implementation Blueprint Purpose

Tài liệu này là **Deliverable Trọng yếu Nhất (Primary Implementation Deliverable)** của Milestone M1. Mục tiêu duy nhất của tài liệu này là cung cấp một bản thiết kế thi công (Implementation Blueprint) hoàn chỉnh, mạch lạc và tường minh đến mức các kỹ sư phần mềm cao cấp hoặc các **AI Coding Agents** có thể bắt đầu xây dựng mã nguồn thực tế của **PFS Core (Rust)** trong Milestone M2–M4 mà không phải tự suy đoán bất kỳ nguyên tắc kiến trúc hoặc quy tắc ranh giới nào.

> [!CRITICAL]
> **Tuyên bố Ranh giới Hiện thực:** Milestone M1 hoàn thành trọn vẹn việc thiết kế kiến trúc, hợp đồng giao tiếp, mô hình dữ liệu, tiêu chí nghiệm thu và lộ trình xây dựng. Tài liệu này KHÔNG tuyên bố rằng mã nguồn runtime của PFS Core đã được biên dịch hoặc thực thi trong thực tế (điều này được phân bổ thực hiện trong Milestones M2, M3 và M4 theo đúng chỉ thị M0 và Roadmaps).

---

## 2. Cargo Workspace Architecture & Crate Dependency Order

Mã nguồn PFS Core được tổ chức thành một Cargo Workspace chuẩn hóa gồm 10 Crates. Thứ tự biên dịch và triển khai tuân thủ nghiêm ngặt đồ thị phụ thuộc từ dưới lên (Bottom-up Dependency Order):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Cargo Workspace Build & Dependency Order                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Layer 1 (Rễ độc lập):  pfs-core (Zero external I/O, Pure Domain Entities)  │
│                                │                                            │
│  Layer 2 (Lõi chính sách):     ├──> pfs-governance (L0–L5 Engine, Grants)   │
│                                ├──> pfs-workflow (11-Stage State Machine)   │
│                                └──> pfs-quality (Quality Gates, Merkle DAG) │
│                                │                                            │
│  Layer 3 (Ứng dụng điều phối): ├──> pfs-app (CQRS Handlers, Saga Execution) │
│                                ├──> pfs-agent (Task Planner & Router)       │
│                                └──> pfs-generator (Staged CAS Generator)    │
│                                │                                            │
│  Layer 4 (Hạ tầng thích ứng):  └──> pfs-infra (SQLx, AI Gateway, Sandbox)   │
│                                │                                            │
│  Layer 5 (Nhị phân đầu cuối):  ├──> pfs-cli (Command Line Interface Binary) │
│                                └──> pfs-server (Local Daemon & REST Server) │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Lộ trình Triển khai qua các Milestone (Milestone Mapping)
- **Milestone M1 (Hiện tại):** Hoàn tất toàn bộ Tài liệu Kiến trúc, Contracts, Schemas, ADRs, Bản thiết kế thi công và Bộ kiểm tra tự động.
- **Milestone M2 (Universal Agent System & Vertical Slice):** Triển khai các crates:
  - `pfs-core`: Các aggregates cốt lõi (`Project`, `Intent`, `Requirement`, `Decision`, `Artifact`).
  - `pfs-governance`: Policy Engine L0–L5, Deny-by-default, Ed25519 signature checks.
  - `pfs-agent`: Agent Task Planner, Router và Context Builder (tích hợp PEP/PDP).
  - `pfs-infra`: Provider Gateway (OpenAI, local vLLM) và SQLite persistence qua SQLx.
  - `pfs-cli`: Giao diện dòng lệnh cơ bản cho kịch bản Vertical Slice.
  - **`pfs-generator` (Minimal Generator Foundation):** Đóng gói bộ sinh tối thiểu phục vụ kịch bản First Vertical Slice (staging, conflict detection cơ bản, safe apply cấp file).
- **Milestone M3 (Validation & Quality Gates):** Triển khai các crates: `pfs-workflow` (FSM 11 giai đoạn), `pfs-quality` (Quality Gates, Cycle Detection trên DAG, Evidence Ledger).
- **Milestone M4 (Full Generator Automation & Production):** Hoàn thiện **Full Generator Engine** (13-stage Journal-Based Commit & Recovery, multi-artifact planning, 3-way merge, crash recovery), hoàn thiện `pfs-server` (REST API Daemon theo OpenAPI 3.1) và đóng gói bản phát hành v1.0.0.

---

## 3. The First Vertical Slice: "Minimal Foundation from Intent"

Để kiểm chứng toàn bộ chuỗi kiến trúc ngay từ bước đầu triển khai trong M2, PFS thiết kế kịch bản **Vertical Slice Đầu tiên (End-to-End Vertical Slice)**:

**"Tiếp nhận một câu Project Intent ngắn gọn từ dòng lệnh CLI và sinh ra một Minimal Project Foundation Package có cấu trúc, được kiểm định chất lượng và lưu vết kiểm toán đầy đủ."**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                End-to-End First Vertical Slice Execution Flow               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. User runs: `pfs init --intent "Xây dựng hệ thống lưu trữ phân tán Rust"`│
│ 2. CLI parse command -> Send CmdInitializeProject to Application Layer     │
│ 3. Policy Engine validates: Actor has L2 authority -> Allowed              │
│ 4. Intent Service creates Project Aggregate (Stage: STG-01-INIT)           │
│ 5. Agent Orchestrator calls AI Provider Gateway (Fast Model) to parse scope │
│ 6. Core resolves Capability Profile (SoftwareProduct Profile selected)     │
│ 7. Requirements Engine generates 5 core functional requirements into DAG   │
│ 8. Governance Engine records initial Architecture Decision (ADR-001)       │
│ 9. Minimal Generator stages minimal directory tree in .pfs/staging/         │
│ 10. Quality Engine runs Schema Validator & SHA-256 Checksum (Pass)          │
│ 11. Interactive Dry-run Diff is displayed to User in Terminal              │
│ 12. User confirms (L3 sign-off) -> Safe File Apply to workspace directory   │
│ 13. Audit Ledger commits cryptographic record sealed with Ed25519 signature │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Các Crates và Modules tham gia Vertical Slice
- `pfs-cli`: Xử lý tương tác dòng lệnh và hiển thị giao diện terminal wizard (`MOD-29-INTG`).
- `pfs-core`: Khởi tạo các thực thể `Project`, `Requirement`, `Decision`, `Artifact` (`MOD-01..09`).
- `pfs-governance`: Kiểm tra quyền hạn L2 của người dùng và ghi nhận chữ ký số (`MOD-10`, `MOD-11`).
- `pfs-infra`: Gửi prompt phân tích intent sang mô hình AI qua Provider Gateway (`MOD-16-GWY`).
- `pfs-generator`: Phân hệ Minimal Generator sinh cấu trúc thư mục, tệp `README.md`, `specs/`, và `.pfs-manifest.json` (`MOD-22-GEN`).
- `pfs-quality`: Kiểm tra tính toàn vẹn của mã băm SHA-256 đối với các tệp tin vừa sinh (`MOD-23`, `MOD-24`).

---

## 4. Implementation Backlog Items (BL-01 to BL-07)

Dưới đây là danh mục các hạng mục công việc thực thi cụ thể:

### BL-01: Khởi tạo Cargo Workspace và Crate `pfs-core`
- **Mô tả:** Thiết lập cấu trúc workspace, định nghĩa các kiểu thực thể bất biến: `ProjectId`, `ULID`, `ProjectIntent`, `ProjectProfile`, `FoundationStage`.
- **Milestone:** M2 | **Priority:** Critical | **Module:** `MOD-03-PRJ`, `MOD-01-IAM`.
- **Preconditions:** M1 Architecture Baseline được duyệt.
- **Definition of Done:** Crate biên dịch không cảnh báo (`cargo check`), 100% unit tests vượt qua cho việc khởi tạo và xác thực thuộc tính của các aggregates.

### BL-02: Hiện thực hóa Policy Engine và Mô hình Phân quyền L0–L5 (`pfs-governance`)
- **Mô tả:** Viết mã nguồn kiểm soát thẩm quyền theo nguyên tắc Deny-by-default, kiểm tra SoD, kiểm tra Data Classification (FND-M1-01) và xác thực chữ ký số Ed25519.
- **Milestone:** M2 | **Priority:** Critical | **Module:** `MOD-11-POL`, `MOD-10-GOV`.
- **Definition of Done:** Toàn bộ các kịch bản kiểm thử phân quyền (L0 đến L5) chạy thành công; các thao tác vượt quyền hoặc gửi dữ liệu Restricted ra ngoại vi bị chặn đứng 100%.

### BL-03: Hiện thực hóa AI Provider Gateway Adapter (`pfs-infra`)
- **Mô tả:** Viết adapter kết nối OpenAI và local vLLM/Ollama, hỗ trợ structured output (JSON Schema), streaming, đo lường token và chốt chặn an ninh chặn dữ liệu Restricted.
- **Milestone:** M2 | **Priority:** High | **Module:** `MOD-16-GWY`.
- **Definition of Done:** Thực hiện thành công cuộc gọi sinh cấu trúc qua mock server và máy chủ thực tế; tự động retry khi gặp lỗi 429; từ chối dispatch dữ liệu Restricted ra ngoài.

### BL-04: Hiện thực hóa Động cơ Máy trạng thái Workflow 11 Giai đoạn (`pfs-workflow`)
- **Mô tả:** Lập trình State Machine điều phối vòng đời dự án, cài đặt các hàm Transition Guards và Saga Transaction Journal.
- **Milestone:** M3 | **Priority:** High | **Module:** `MOD-12-WKF`.
- **Definition of Done:** Máy trạng thái vượt qua bài kiểm thử chuyển đổi hợp lệ và bài kiểm thử từ chối chuyển đổi khi vi phạm guard.

### BL-05: Hiện thực hóa Quality Engine và Kiểm định Truy vết Đồ thị (`pfs-quality`)
- **Mô tả:** Lập trình thuật toán phát hiện chu trình (Cycle Detection bằng DFS/Tarjan) trên đồ thị Requirements DAG và kiểm tra bằng chứng Quality Gates.
- **Milestone:** M3 | **Priority:** High | **Module:** `MOD-23-QLT`, `MOD-08-REQ`.
- **Definition of Done:** Phát hiện chính xác 100% các chu trình phụ thuộc giả lập trong test suite; khóa gate khi có lỗi Critical.

### BL-06: Hiện thực hóa Journal-Based Staged Commit & Recovery Engine (`pfs-generator`)
- **Mô tả:** Lập trình cơ chế lưu trữ Content-Addressed Storage, bộ sinh staged file, phát hiện xung đột mã băm và quy trình commit an toàn kèm Write-Ahead Journal.
- **Milestone:** M2 (Minimal Foundation) / M4 (Full Engine) | **Priority:** Critical | **Module:** `MOD-22-GEN`, `MOD-20-ART`.
- **Definition of Done:** Quá trình sinh Foundation bảo toàn 100% tệp tin người dùng; hoàn tác sạch sẽ khi có lệnh hủy bỏ.

### BL-07: Hiện thực hóa Giao diện Dòng lệnh CLI (`pfs-cli`)
- **Mô tả:** Xây dựng nhị phân dòng lệnh tích hợp bộ phân tích tham số `clap`, các wizard tương tác và cờ đầu ra `--json` cho CI/CD.
- **Milestone:** M2–M4 | **Priority:** High | **Module:** `MOD-29-INTG`.
- **Definition of Done:** CLI chạy độc lập, hỗ trợ đầy đủ các lệnh `init`, `plan`, `gate`, `generate`, `verify`.

---

## 5. Milestone M2 Work Packages (WP-M2-01 to WP-M2-06) & Readiness Assessment

Để chuẩn bị đầy đủ cho việc khởi động Milestone M2 ngay khi Project Owner phê duyệt M1, toàn bộ 6 gói công việc (Work Packages) được chuẩn hóa:

### WP-M2-01: Cargo Workspace & `pfs-core`
- **Mục tiêu:** Thiết lập cấu trúc Cargo Workspace 10 Crates và xây dựng Pure Domain Core (`pfs-core`).
- **Phạm vi:** Định nghĩa kiểu thực thể cốt lõi, value objects, ULID generation, Aggregates (`Project`, `Intent`, `Requirement`, `Decision`, `Artifact`).
- **Non-goals:** Không thực hiện bất kỳ lời gọi I/O (Disk/Network/DB) nào trong `pfs-core`.
- **Đầu vào:** `07-UNIVERSAL-DOMAIN-MODEL.md`, `project-schema.json`, `intent-schema.json`.
- **Đầu ra:** Crate `pfs-core` biên dịch sạch sẽ, 100% unit tests đạt.
- **Phụ thuộc:** Không phụ thuộc crate nào (Level 1 Root).
- **Yêu cầu & AC:** M0-MOD-001, M0-MOD-004, AC-M1-05, AC-M1-06.
- **Kiểm thử:** Unit tests cho aggregate invariants, ULID ordering, SemVer parsing.
- **Trạng thái Sẵn sàng:** **READY**.

### WP-M2-02: Policy Engine & L0–L5 Authorization (`pfs-governance`)
- **Mục tiêu:** Hiện thực hóa Policy Decision Point (PDP) và mô hình phân quyền 6 cấp L0–L5.
- **Phạm vi:** Đánh giá Deny-by-default, SoD enforcement, kiểm tra Classification Tier (FND-M1-01), xác thực chữ ký Ed25519.
- **Non-goals:** Không tích hợp LDAP hay SSO doanh nghiệp phức tạp trong M2.
- **Đầu vào:** `19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md`, `ADR-014`, `ADR-015`.
- **Đầu ra:** Crate `pfs-governance` cung cấp hàm `evaluate_policy()`.
- **Phụ thuộc:** `pfs-core`.
- **Yêu cầu & AC:** M0-GOV-001, M0-AUT-001, AC-M1-22, FND-M1-01.
- **Kiểm thử:** Security test suite cho 100 kịch bản phân quyền và kiểm tra chữ ký số giả mạo.
- **Trạng thái Sẵn sàng:** **READY** (Sau khi hoàn tất đặc tả FND-M1-01).

### WP-M2-03: Provider Gateway & AI Integration (`pfs-infra`)
- **Mục tiêu:** Xây dựng adapter kết nối AI Provider với tính năng Constrained Decoding và chốt chặn an ninh.
- **Phạm vi:** OpenAI adapter, Anthropic adapter, Local vLLM/Ollama adapter, Token budgeting, cờ Do-Not-Train / ZDR, chốt chặn từ chối gửi dữ liệu Restricted ra External Cloud.
- **Non-goals:** Không huấn luyện mô hình (Fine-tuning) trong M2.
- **Đầu vào:** `17-AI-PROVIDER-AND-TOOL-ADAPTERS.md`, `ADR-012`, `provider-contracts.json`.
- **Đầu ra:** Module `MOD-16-GWY` trong `pfs-infra` hiện thực hóa Trait `AIProviderPort`.
- **Phụ thuộc:** `pfs-core`, `pfs-governance` (kiểm tra phân loại dữ liệu).
- **Yêu cầu & AC:** M0-AGT-006, M0-SEC-004, AC-M1-20, FND-M1-01.
- **Kiểm thử:** Mock server tests cho HTTP streaming, structured output validation, và chặn dispatch dữ liệu Restricted.
- **Trạng thái Sẵn sàng:** **CONDITIONALLY READY** (Sẵn sàng triển khai sau khi hoàn tất thiết kế chốt chặn FND-M1-01; bị chặn nếu gửi dữ liệu chưa phân loại).

### WP-M2-04: Agent Task Planner & Router (`pfs-agent`)
- **Mục tiêu:** Xây dựng bộ lập kế hoạch phân rã nhiệm vụ và định tuyến tác vụ cho AI Agents.
- **Phạm vi:** Phân rã Project Intent thành DAG nhiệm vụ, Context Builder (tích hợp PEP), quản lý Task Lease và ghi nhận Disagreement Record.
- **Non-goals:** Không hỗ trợ multi-agent swarm tự trị hoàn toàn không có giám sát.
- **Đầu vào:** `16-AGENT-ORCHESTRATION-ARCHITECTURE.md`, `ADR-011`, `ADR-013`.
- **Đầu ra:** Crate `pfs-agent` điều phối các tác vụ phân tích và sinh đề xuất.
- **Phụ thuộc:** `pfs-core`, `pfs-governance`, `pfs-infra` (Provider Gateway).
- **Yêu cầu & AC:** M0-AGT-001, M0-AGT-004, AC-M1-19.
- **Kiểm thử:** Integration test cho kịch bản phân tích intent và lập kế hoạch DAG 5 bước.
- **Trạng thái Sẵn sàng:** **READY**.

### WP-M2-05: Local CLI & First Vertical Slice (`pfs-cli` & Minimal `pfs-generator`)
- **Mục tiêu:** Hiện thực hóa kịch bản First Vertical Slice xuyên suốt từ dòng lệnh đến khi sinh file an toàn.
- **Phạm vi:** Lệnh `pfs init`, wizard tương tác terminal, Minimal Generator Foundation sinh `README.md`, `specs/`, `.pfs-manifest.json`, dry-run diff, safe file apply.
- **Non-goals:** Không bao gồm Full Generator M4 (không có template nesting phức tạp, không có 3-way merge).
- **Đầu vào:** `24-API-CLI-AND-USER-INTERFACE-ARCHITECTURE.md`, `18-GENERATION-AND-RECOVERY-ARCHITECTURE.md`.
- **Đầu ra:** Nhị phân `pfs` có thể chạy trên máy trạm thực tế.
- **Phụ thuộc:** `pfs-core`, `pfs-governance`, `pfs-agent`, `pfs-infra`.
- **Yêu cầu & AC:** M0-PRD-001, AC-M1-36, FND-M1-06.
- **Kiểm thử:** End-to-end integration test chạy lệnh `pfs init` và kiểm tra tệp tin sinh ra trên thư mục tạm.
- **Trạng thái Sẵn sàng:** **READY**.

### WP-M2-06: Database Persistence via SQLx (`pfs-infra`)
- **Mục tiêu:** Hiện thực hóa lớp lưu trữ dữ liệu bền vững bằng SQLite trên máy trạm cá nhân.
- **Phạm vi:** Cài đặt `SqliteRepository` cho các aggregates cốt lõi, chạy migration `sqlx::migrate!()`, cấu hình WAL mode.
- **Non-goals:** Không bắt buộc hoàn thiện 100% PostgreSQL production cluster trong M2 (PostgreSQL được kiểm thử song song trong M3/M4).
- **Đầu vào:** `ADR-007`, `13-CORE-AND-APPLICATION-ARCHITECTURE.md`.
- **Đầu ra:** Module persistence trong `pfs-infra`.
- **Phụ thuộc:** `pfs-core`.
- **Yêu cầu & AC:** M0-ART-002, AC-M1-07.
- **Kiểm thử:** SQL migration tests, CRUD tests, transaction rollback tests trên SQLite in-memory & file.
- **Trạng thái Sẵn sàng:** **READY**.

---

## 6. Tổng hợp Trạng thái Sẵn sàng Milestone M2 (Readiness Verdict)

| Work Package ID | Tên gói công việc | Mức độ Sẵn sàng | Rào cản còn lại (Blockers) | Kế hoạch hành động |
|---|---|---|---|---|
| `WP-M2-01` | Cargo Workspace & `pfs-core` | **READY** | Không | Bắt đầu thi công ngay khi M1 được duyệt |
| `WP-M2-02` | Policy Engine & L0–L5 | **READY** | Không | Tích hợp đặc tả FND-M1-01 vào test suite |
| `WP-M2-03` | Provider Gateway & AI Integration | **CONDITIONALLY READY** | Yêu cầu hoàn thành chốt chặn dữ liệu Restricted | Triển khai mock adapter trước khi nối mạng |
| `WP-M2-04` | Agent Task Planner & Router | **READY** | Phụ thuộc WP-M2-01, 02, 03 | Xây dựng theo thứ tự dependency DAG |
| `WP-M2-05` | Local CLI & First Vertical Slice | **READY** | Phụ thuộc các WP trên | Là tiêu chí nghiệm thu chính của M2 |
| `WP-M2-06` | Database Persistence via SQLx | **READY** | Không | Viết migration script cho SQLite |

**KẾT LUẬN SẴN SÀNG:** Toàn bộ bản thiết kế thi công M2 đã hoàn tất và mạch lạc. Milestone M2 đạt trạng thái **SẴN SÀNG KHỞI ĐỘNG CÓ ĐIỀU KIỆN (CONDITIONALLY READY — PENDING M1 OWNER ACCEPTANCE)**.
