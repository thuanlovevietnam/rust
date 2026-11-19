# PFS-M1-DOC-014 — Application Contracts, Commands, Queries and Events

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-014 |
| Document Title | Application Contracts, Commands, Queries and Events Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Architecture Pattern | Command Query Responsibility Segregation (CQRS), Event-Driven Architecture |
| Related Decisions | ADR-010, ADR-014, ADR-018 |

---

## 1. Unified Interaction Contracts Philosophy

Trong **Project Foundation System (PFS)**, mọi tương tác với hệ thống—cho dù xuất phát từ giao diện người dùng Web, dòng lệnh CLI, lời gọi API từ bên ngoài hay một AI Agent tự hành—đều bắt buộc phải tuân thủ **Một Ngữ nghĩa Nghiệp vụ Thống nhất (Single Business Semantics)**.

Hệ thống áp dụng mô hình **CQRS (Command Query Responsibility Segregation)**:
- **Command:** Biểu đạt ý định thay đổi trạng thái hệ thống; bắt buộc phải có thẩm quyền L2–L5, được thực thi trong một ranh giới giao dịch và phát sinh Domain Events.
- **Query:** Biểu đạt yêu cầu đọc dữ liệu; bắt buộc mang tính **Read-Only tuyệt đối** đối với trạng thái nghiệp vụ, hỗ trợ phân trang, lọc và sắp xếp.
- **Events:** Ghi nhận sự kiện nghiệp vụ đã xảy ra trong quá khứ một cách bất biến, phục vụ đồng bộ hóa bất đồng bộ, kiểm toán và giám sát.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CQRS Application Contracts                         │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ COMMAND PIPELINE (State-Changing)    │ QUERY PIPELINE (Read-Only)           │
│ 1. Identity & L0–L5 Authorization    │ 1. Identity & Scope Authorization    │
│ 2. Schema Validation (Input DTO)     │ 2. Filter, Pagination & Sort Params  │
│ 3. Preconditions & State Machine     │ 3. Read Replica / Read-Optimized View│
│ 4. Transactional Execution in Core   │ 4. Deterministic Output Schema       │
│ 5. Emit Domain Events & Audit Log    │ 5. Zero Side Effects on Business State│
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Command Contracts Architecture

Mỗi Command trong PFS được định nghĩa bằng một cấu trúc hợp đồng chuẩn mực (được ánh xạ thành Rust Structs và JSON Schema):

### 2.1. Cấu trúc Hợp đồng Command Chuẩn
1. `command_id`: Định danh duy nhất của lệnh (ULID).
2. `command_type`: Tên lệnh định danh dạng URN (vd: `cmd.project.initialize`, `cmd.governance.approve_decision`).
3. `actor_principal`: Danh tính chủ thể phát lệnh (User ID / Agent Profile ID).
4. `required_authority`: Mức phân quyền tối thiểu theo mô hình L0–L5 (vd: `L3_ModifyFiles`, `L5_Privileged`).
5. `project_scope`: Định danh dự án chịu tác động (Project Scope Isolation).
6. `idempotency_key`: Khóa chống trùng lặp do client gửi lên.
7. `payload`: Dữ liệu đầu vào đã qua kiểm định JSON Schema.
8. `preconditions`: Biểu thức logic điều kiện tiên quyết bắt buộc thỏa mãn.
9. `transaction_boundary`: Phạm vi giao dịch nguyên tử (Atomic / Saga).
10. `emitted_events`: Danh mục các sự kiện nghiệp vụ được phát sinh khi thành công.

### 2.2. Danh mục các Commands Cốt lõi
- `CmdInitializeProject`: Khởi tạo dự án và tiếp nhận Project Intent ban đầu (Authority: L2/L3).
- `CmdSpecifyRequirement`: Thêm mới hoặc cập nhật một yêu cầu vào DAG (Authority: L2).
- `CmdRecordDecision`: Đề xuất hoặc ban hành một Quyết định kiến trúc ADR (Authority: L3/L4).
- `CmdApproveStage`: Phê duyệt chuyển đổi giai đoạn trong Foundation Workflow (Authority: L3/L4/L5).
- `CmdGenerateFoundation`: Kích hoạt tiến trình sinh Foundation Package ra Staging (Authority: L3).
- `CmdCommitFoundation`: Áp dụng Foundation Package đã sinh vào thư mục làm việc (Authority: L4/L5).
- `CmdRevokeAuthority`: Thu hồi quyền hạn của một Agent hoặc người dùng (Authority: L5).

---

## 3. Query Contracts Architecture

Mọi Query trong PFS đều bảo đảm tính an toàn tuyệt đối và tính xác định:

### 3.1. Cấu trúc Hợp đồng Query Chuẩn
1. `query_id`: Định danh duy nhất của truy vấn.
2. `query_type`: Tên truy vấn định danh (vd: `query.requirement.get_dag`, `query.artifact.get_provenance`).
3. `actor_principal`: Danh tính chủ thể truy vấn.
4. `required_authority`: Thẩm quyền đọc tối thiểu (mặc định: `L0_ReadOnly`).
5. `filters`: Tiêu chí lọc dữ liệu có cấu trúc.
6. `pagination`: Tham số phân trang chuẩn: `limit` (tối đa 100), `offset` hoặc `cursor` (ULID).
7. `sorting`: Danh sách các trường sắp xếp kèm hướng (`ASC` / `DESC`).
8. `consistency`: `StrongConsistency` (đọc từ Primary DB) hoặc `EventualConsistency` (đọc từ Read Views).

### 3.2. Danh mục các Queries Cốt lõi
- `QueryGetProjectOverview`: Lấy thông tin tổng hợp về dự án, tiến độ workflow và rủi ro.
- `QueryListRequirements`: Liệt kê yêu cầu theo phân loại, độ ưu tiên hoặc trạng thái kiểm chứng.
- `QueryGetTraceabilityMatrix`: Xuất ma trận truy vết hai chiều từ Intent đến Artifacts.
- `QueryGetDryRunDiff`: Xem trước các thay đổi tệp tin (File Diff) trước khi commit Foundation.
- `QueryGetAuditTrail`: Truy xuất sổ cái kiểm toán bất biến theo khoảng thời gian và chủ thể.

---

## 4. Event Contracts Architecture

PFS phân định rõ ràng 4 loại sự kiện (Events) với các mục đích chuyên biệt:

```
                                  EVENT TAXONOMY
    ┌──────────────────────────────┬──────────────────────────────┐
    │     1. DOMAIN EVENTS         │    2. INTEGRATION EVENTS     │
    ├──────────────────────────────┼──────────────────────────────┤
    │ Xảy ra bên trong Domain Core │ Truyền tin tới các phân hệ   │
    │ Bắt buộc lưu cùng giao dịch  │ ngoài hoặc webhooks bên ngoài│
    │ Vd: RequirementAdded         │ Vd: StageApprovedWebhook     │
    ├──────────────────────────────┼──────────────────────────────┤
    │     3. AUDIT EVENTS          │    4. EXECUTION EVENTS       │
    ├──────────────────────────────┼──────────────────────────────┤
    │ Phục vụ thanh tra pháp lý    │ Giám sát tiến độ chi tiết    │
    │ Bất biến, niêm phong chữ ký  │ Streaming token, CPU usage   │
    │ Vd: AuthorityRevokedRecord   │ Vd: AgentTokenConsumedEvent  │
    └──────────────────────────────┴──────────────────────────────┘
```

### 4.1. Cấu trúc Phong bì Sự kiện Chuẩn hóa (Universal Event Envelope)
```json
{
  "event_id": "01HQZ9G8K5E7B9A3F1M4R2V0W8",
  "event_type": "pfs.domain.stage_transitioned",
  "schema_version": "1.0.0",
  "aggregate_id": "pfs:project:ws_corp:prj_alpha",
  "timestamp": "2026-11-17T13:20:00Z",
  "correlation_id": "corr_01HQZ9A1B2C3D4E5F6G7H8J9K0",
  "causation_id": "cmd_01HQZ99876543210FEDCBA9876",
  "producer": "pfs-workflow-engine",
  "payload": {
    "from_stage": "STG-03-REQS",
    "to_stage": "STG-04-ARCH",
    "transition_reason": "Requirements Baseline Approved by Owner",
    "approver_principal": "user_owner_nguyen_the_thuan"
  }
}
```

---

## 5. Standardized Adapter Contracts (Ports & Adapters)

Mọi phụ thuộc vào công nghệ ngoại vi đều được trừu tượng hóa bằng các Rust Traits:

### 5.1. AI Provider Gateway Port (`AIProviderPort`)
```rust
#[async_trait::async_trait]
pub trait AIProviderPort: Send + Sync {
    async fn generate_completion(
        &self,
        request: UniversalLLMRequest,
    ) -> Result<UniversalLLMResponse, ProviderError>;

    async fn stream_completion(
        &self,
        request: UniversalLLMRequest,
    ) -> Result<Pin<Box<dyn Stream<Item = Result<LLMStreamChunk, ProviderError>> + Send>>, ProviderError>;
}
```

### 5.2. Tool Sandbox Port (`ToolExecutionPort`)
```rust
#[async_trait::async_trait]
pub trait ToolExecutionPort: Send + Sync {
    async fn execute_tool(
        &self,
        tool_name: &str,
        arguments: serde_json::Value,
        sandbox_policy: SandboxPolicy,
    ) -> Result<ToolExecutionResult, SandboxError>;
}
```

### 5.3. Content-Addressed Storage Port (`StoragePort`)
```rust
#[async_trait::async_trait]
pub trait StoragePort: Send + Sync {
    async fn put_blob(&self, data: &[u8]) -> Result<ContentHash, StorageError>;
    async fn get_blob(&self, hash: &ContentHash) -> Result<Vec<u8>, StorageError>;
    async fn exists(&self, hash: &ContentHash) -> Result<bool, StorageError>;
}
```
