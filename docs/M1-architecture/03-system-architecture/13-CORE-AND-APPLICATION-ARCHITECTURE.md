# PFS-M1-DOC-013 — PFS Core and Application Architecture (Rust)

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-013 |
| Document Title | PFS Core and Application Architecture Specification (Rust) |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Programming Language | Rust (Edition 2021 / 2024 Stable) |
| Related Decisions | ADR-001, ADR-002, ADR-003, ADR-007 |
| Invariant Reference | INV-02, INV-03, INV-06 |

---

## 1. Rust Architecture Strategy & Rationale

Theo bất biến kiến trúc cốt lõi **INV-03**, **PFS Core Engine** được hiện thực hóa 100% bằng ngôn ngữ lập trình **Rust**. Việc lựa chọn Rust không đơn thuần là một quyết định công nghệ mà là sự bảo đảm kỹ thuật cho các thuộc tính sống còn của hệ thống:
1. **Memory Safety Without Garbage Collection:** Loại bỏ hoàn toàn các lỗ hổng bảo mật về bộ nhớ (Null pointer dereference, Buffer overflow, Use-after-free) mà không phải chịu độ trễ ngắt quãng do thu gom rác (GC pauses).
2. **Fearless Concurrency & Thread Safety:** Hệ thống kiểu dữ liệu (`Send` và `Sync`) bảo đảm an toàn dữ liệu tuyệt đối khi hàng chục AI Agents và luồng xử lý chạy song song.
3. **Zero-Cost Abstractions:** Các Trait contracts và State Machine được tối ưu hóa ở thời điểm biên dịch (compile-time), mang lại tốc độ thực thi xác định (Deterministic Execution) ở mức microsecond.
4. **Strong Domain Modeling:** Sử dụng triệt để hệ thống Type System phong phú của Rust (Enums with Data, Newtype pattern, Typestate pattern) để biến các trạng thái không hợp lệ thành lỗi biên dịch (Make Invalid States Unrepresentable).

---

## 2. Cargo Workspace & Crate Decomposition

PFS Core được tổ chức dưới dạng một **Cargo Workspace** phân cấp gồm 10 Crates chuyên biệt, phản ánh chính xác ranh giới của các phân hệ logic:

```
crates/
├── pfs-core/               # [TẦNG LÕI] Domain Models, Value Objects, Aggregates, Invariants (Pure Rust)
├── pfs-governance/         # [TẦNG LÕI] L0–L5 Policy Engine, Authority Grants, Decision Evaluation
├── pfs-workflow/           # [TẦNG LÕI] 11-Stage State Machine, Transition Guards, FSM Logic
├── pfs-quality/            # [TẦNG LÕI] Quality Gate Manifest, Evidence Verification, DAG Validator
├── pfs-app/                # [TẦNG ỨNG DỤNG] Application Services, CQRS Handlers, Saga Orchestrator
├── pfs-agent/              # [TẦNG ỨNG DỤNG] Agent Task Planner, Router, Context Window Injector
├── pfs-generator/          # [TẦNG ỨNG DỤNG] Staged Idempotent Generator, CAS Storage, Conflict Engine
├── pfs-infra/              # [TẦNG HẠ TẦNG] Database (SQLx), AI Gateway, Tool Sandbox, Observability
├── pfs-cli/                # [TẦNG GIAO DIỆN] CLI Binary (clap), Interactive Wizards, Progress Render
└── pfs-server/             # [TẦNG GIAO DIỆN] Daemon Process (axum), REST Endpoints, WebSocket Streams
```

### 2.1. Ma trận phân quyền phụ thuộc giữa các Crates

| Crate | Vai trò phân tầng | Các Crates được phép phụ thuộc | Crates BỊ CẤM phụ thuộc |
|---|---|---|---|
| `pfs-core` | Domain Core (Pure) | *Không phụ thuộc Crate nào khác trong workspace* | `pfs-app`, `pfs-infra`, `pfs-cli`, `pfs-server` |
| `pfs-governance` | Domain Core | `pfs-core` | `pfs-infra`, `pfs-cli`, `pfs-server` |
| `pfs-workflow` | Domain Core | `pfs-core`, `pfs-governance` | `pfs-infra`, `pfs-cli`, `pfs-server` |
| `pfs-quality` | Domain Core | `pfs-core`, `pfs-governance` | `pfs-infra`, `pfs-cli`, `pfs-server` |
| `pfs-app` | Application Service | `pfs-core`, `pfs-governance`, `pfs-workflow`, `pfs-quality` | `pfs-cli`, `pfs-server` |
| `pfs-agent` | Application Service | `pfs-core`, `pfs-app` | `pfs-cli`, `pfs-server` |
| `pfs-generator` | Application Service | `pfs-core`, `pfs-app`, `pfs-quality` | `pfs-cli`, `pfs-server` |
| `pfs-infra` | Infrastructure Adapters | `pfs-core`, `pfs-governance`, `pfs-app` | `pfs-cli`, `pfs-server` |
| `pfs-cli` | Presentation (Binary) | `pfs-core`, `pfs-app`, `pfs-infra` | *Là nhị phân đầu cuối* |
| `pfs-server` | Presentation (Binary) | `pfs-core`, `pfs-app`, `pfs-infra` | *Là nhị phân đầu cuối* |

---

## 3. Aggregate Roots & Transaction Boundaries

Để bảo đảm tính nhất quán dữ liệu (Data Consistency) và tránh xung đột khóa bản ghi trong môi trường đa luồng:

```rust
// Định nghĩa Aggregate Root chuẩn trong pfs-core
pub trait AggregateRoot {
    type Id: Clone + PartialEq + Eq + std::hash::Hash;
    
    fn id(&self) -> &Self::Id;
    fn version(&self) -> u64;
    fn uncommitted_events(&self) -> &[DomainEvent];
    fn clear_uncommitted_events(&mut self);
}

// Ví dụ: ProjectAggregate quản lý ranh giới giao dịch của Dự án
pub struct ProjectAggregate {
    id: ProjectId,
    version: u64, // Dùng cho Optimistic Concurrency Control (OCC)
    intent: ProjectIntent,
    profile: ProjectProfile,
    current_stage: FoundationStage,
    uncommitted_events: Vec<DomainEvent>,
}
```

### 3.1. Cơ chế kiểm soát đồng thời lạc quan (Optimistic Concurrency Control - OCC)
Khi cập nhật bất kỳ Aggregate nào (Project, Requirement DAG, Workflow State):
1. Ứng dụng đọc thực thể kèm phiên bản hiện tại (`version = N`).
2. Thực thi quy tắc nghiệp vụ nội bộ trên bộ nhớ (In-memory verification).
3. Ghi dữ liệu vào cơ sở dữ liệu với điều kiện:
   $$\mathbf{UPDATE\ table\ SET\ ...,\ version = N+1\ WHERE\ id = :id\ AND\ version = N}$$
4. Nếu số dòng ảnh hưởng bằng 0 (do luồng khác đã cập nhật trước), hệ thống phát sinh lỗi `ConcurrencyConflictError` và kích hoạt chiến lược Retry tự động sau khi nạp lại trạng thái mới nhất.

---

## 4. Concurrency Model & Async Runtime (Tokio)

PFS Core sử dụng **Tokio Runtime (Multi-Threaded Work-Stealing Scheduler)** làm nền tảng xử lý bất đồng bộ:
- **I/O-Bound Tasks (AI API Calls, DB Queries, Network Streaming):** Chạy trên luồng bất đồng bộ của Tokio, sử dụng `tokio::spawn` với kênh giao tiếp thông điệp `tokio::sync::mpsc`.
- **CPU-Bound Tasks (DAG Cycle Detection, Merkle Hash Calculation, WASM Sandboxing):** Tuyệt đối không chặn luồng async của Tokio; được cách ly sang thread pool chuyên biệt thông qua `tokio::task::spawn_blocking` hoặc thư viện tính toán song song `rayon`.
- **Graceful Shutdown & Task Cancellation:** Sử dụng `tokio_util::sync::CancellationToken` để truyền tín hiệu dừng tới toàn bộ các tiến trình con và tác vụ Agent khi người dùng hủy bỏ hoặc khi nhận tín hiệu `SIGINT` / `SIGTERM`.

---

## 5. Standardized Error Handling Strategy

Hệ thống phân tách triệt để cách xử lý lỗi giữa Tầng Lõi (Domain) và Tầng Biên (Application Boundary):

1. **Domain & Internal Errors (`thiserror`):**
   Mọi Crate tầng lõi bắt buộc phải định nghĩa lỗi bằng các Enum có kiểu dữ liệu mạnh thông qua macro `thiserror`. Tuyệt đối không dùng kiểu chuỗi tự do (Stringly-typed errors) trong Domain Core.
   ```rust
   #[derive(thiserror::Error, Debug)]
   pub enum GovernanceError {
       #[error("Thẩm quyền không hợp lệ: chủ thể {principal} không có quyền {required:?}")]
       PermissionDenied { principal: String, required: AuthorityLevel },
       
       #[error("Quyết định {decision_id} đang ở trạng thái {current:?}, không thể phê duyệt")]
       InvalidDecisionState { decision_id: String, current: DecisionStatus },
       
       #[error("Xung đột quyền lợi: Người duyệt không được trùng với người khởi tạo (SoD violation)")]
       SeparationOfDutiesViolation,
   }
   ```
2. **Application Boundary & CLI Errors (`anyhow` / Structured DTO):**
   Tại ranh giới tầng ngoài cùng (CLI output, REST API response), các lỗi nội bộ được chuyển đổi thành cấu trúc phản hồi chuẩn hóa kèm theo Correlation ID để dễ dàng tra cứu trong hệ thống viễn trắc (OpenTelemetry).
