# PFS-M1-DOC-017 — AI Provider Gateway and Tool Adapters

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-017 |
| Document Title | AI Provider Gateway and Tool Adapters Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Hexagonal Ports & Adapters, Gateway Pattern, Sandbox Isolation |
| Related Decisions | ADR-012, ADR-013 |
| Invariant Reference | INV-05, INV-06, INV-11 |

---

## 1. Provider Independence & Gateway Architecture

Theo bất biến kiến trúc **INV-05**, **PFS Core hoàn toàn độc lập với bất kỳ nhà cung cấp mô hình AI cụ thể nào**. PFS không bao giờ phụ thuộc trực tiếp vào các SDK độc quyền của OpenAI, Anthropic, Google hay Meta. Toàn bộ các tương tác giao tiếp với mô hình trí tuệ nhân tạo đều được cô lập và chuẩn hóa thông qua **AI Provider Gateway** (thuộc Crate `pfs-infra`).

Kiến trúc Gateway cung cấp 5 năng lực cốt lõi:
1. **Dynamic Model Switching:** Cho phép người dùng hoặc hệ thống chuyển đổi linh hoạt giữa các nhà cung cấp mô hình (ví dụ: chuyển từ OpenAI GPT-4o sang Anthropic Claude 3.7 Sonnet hoặc vLLM chạy offline trên máy chủ nội bộ) chỉ bằng một thay đổi cấu hình mà không phải sửa đổi mã nguồn.
2. **Standardized Tool Calling & Structured Outputs:** Ép buộc các mô hình trả về dữ liệu đúng định dạng JSON Schema mong muốn thông qua cơ chế *Constrained Decoding* hoặc *Function Calling Standardization*.
3. **Resilience & Failover:** Tích hợp Circuit Breaker, Exponential Backoff và cơ chế tự động chuyển vùng dự phòng khi nhà cung cấp chính gặp sự cố.
4. **Token Usage & Cost Governance:** Đo lường chính xác số lượng token đầu vào (prompt) và đầu ra (completion), tính toán chi phí tài chính thời gian thực và tự động khóa tác vụ khi vượt ngân sách cho phép.
5. **Data Minimization & Zero Retention:** Cấu hình các cờ không lưu trữ dữ liệu (Zero Data Retention) phía nhà cung cấp để bảo vệ bí mật kinh doanh của dự án.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI Provider Gateway Model                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ PFS Core / Agent Orchestrator ]                                          │
│       │ calls Universal Provider Trait                                      │
│       ▼                                                                     │
│  [ AI Provider Gateway (pfs-infra) ]                                        │
│  ├── Dynamic Router & Model Selection Engine                                │
│  ├── Token Budgeter & Financial Cost Calculator                             │
│  ├── Circuit Breaker & Rate Limiter (Token Bucket)                          │
│  └── Secret Redaction & Sanitization Filter                                 │
│       │                                                                     │
│       ├──> [ OpenAI Adapter ]      ──> api.openai.com                       │
│       ├──> [ Anthropic Adapter ]   ──> api.anthropic.com                    │
│       ├──> [ Google Gemini Adapter]──> generativelanguage.googleapis.com    │
│       └──> [ Local vLLM/Ollama Adp]──> http://localhost:8000/v1             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Standardized LLM Request & Response Contracts

Tất cả các lời gọi từ Core đều sử dụng cấu trúc dữ liệu chuẩn hóa độc lập với nhà cung cấp:

```rust
// Định nghĩa Universal LLM Request trong pfs-infra
pub struct UniversalLLMRequest {
    pub model_alias: String,             // Vd: "fast-reasoner", "deep-architect"
    pub system_prompt: String,           // Hướng dẫn hệ thống đã qua kiểm duyệt
    pub user_messages: Vec<ChatMessage>, // Lịch sử hội thoại có cấu trúc
    pub tools_schema: Option<Vec<ToolDefinition>>, // Danh sách công cụ cho phép
    pub response_schema: Option<serde_json::Value>, // Bắt buộc định dạng JSON
    pub temperature: f32,                // Nhiệt độ ngẫu nhiên (mặc định: 0.1)
    pub max_tokens: u32,                 // Giới hạn token đầu ra
    pub timeout_duration: Duration,      // Thời hạn tối đa cho cuộc gọi
}

// Định nghĩa Universal LLM Response trong pfs-infra
pub struct UniversalLLMResponse {
    pub content: String,
    pub tool_calls: Vec<ToolCallRequest>,
    pub token_usage: TokenUsageMetrics,
    pub finish_reason: FinishReason,     // Stop, ToolCalls, LengthExceeded
    pub latency_ms: u64,
    pub provider_used: String,
    pub raw_fingerprint: String,
}
```

### 2.1. Chuẩn hóa mã lỗi nhà cung cấp (Universal Error Mapping)
Mọi mã lỗi HTTP (401, 429, 500, 503) hoặc lỗi kết nối từ các nhà cung cấp bên ngoài được ánh xạ thống nhất thành Enum `UniversalProviderError`:
- `AuthenticationFailed`: API key không hợp lệ hoặc đã hết hạn.
- `RateLimitExceeded`: Bị giới hạn tần suất gọi; kích hoạt Exponential Backoff kèm Jitter.
- `QuotaExhausted`: Hết hạn ngạch tài khoản; kích hoạt chuyển sang Secondary Fallback Provider.
- `ContextWindowExceeded`: Ngữ cảnh quá dài; thông báo cho Context Builder thực hiện thu gọn.
- `ProviderUnavailable`: Máy chủ nhà cung cấp bị sập (503); kích hoạt Circuit Breaker trong 60 giây.
- `StructuredOutputViolation`: Mô hình trả về kết quả không khớp JSON Schema; tự động retry kèm thông báo lỗi chi tiết cho mô hình sửa đổi.

---

## 3. Tool Gateway & Sandbox Execution Architecture

Để ngăn chặn triệt để nguy cơ **Agent Chiếm quyền Điều khiển (Confused Deputy / Agent Hijacking)** hoặc thực thi mã độc trên máy chủ, mọi công cụ ngoại vi mà Agent yêu cầu gọi đều phải đi qua **Tool Gateway** và được thực thi trong môi trường **Sandbox Cách ly Tuyệt đối**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Tool Gateway & Sandbox Security Pipeline                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ Agent Tool Call Request ]                                                │
│        │                                                                    │
│  1. Tool Allowlist Check: Công cụ có nằm trong danh mục được phép không?   │
│        │ Pass                                                               │
│  2. L0–L5 Permission Check: Agent có đủ thẩm quyền để gọi công cụ này?      │
│        │ Pass                                                               │
│  3. Input Sanitization: Kiểm tra Path Traversal (../), SQL Injection, Shell │
│        │ Pass                                                               │
│  4. Sandbox Isolation Execution:                                            │
│     ├── Option A: WebAssembly (WASM) Sandbox via Wasmtime                   │
│     └── Option B: Ephemeral Subprocess Jail (chroot, read-only root, no net)│
│        │ Execution Completed                                                │
│  5. Output Verification: Đối soát kích thước kết quả và kiểm tra an toàn   │
│        │                                                                    │
│  [ Return Clean Tool Output to Agent ]                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Các cơ chế cách ly an ninh trong Sandbox (Sandbox Security Controls)
1. **Filesystem Virtualization & Path Traversal Defense:**
   - Mọi đường dẫn tệp tin do Agent yêu cầu (ví dụ: `read_file`, `write_file`) bắt buộc phải được chuẩn hóa thông qua hàm `canonicalize()`.
   - Hệ thống kiểm tra xem đường dẫn đích có nằm hoàn toàn bên trong thư mục làm việc được ủy quyền của dự án (`workspace_root`) hay không.
   - Nếu phát hiện chứa ký tự `..` hoặc đường dẫn tuyệt đối trỏ ra ngoài phạm vi (như `/etc/passwd` hoặc `C:\Windows`), lệnh lập tức bị chặn đứng và ghi nhận vi phạm an ninh nghiêm trọng (Security Finding).
2. **Network Isolation (Air-gapped by Default):**
   - Môi trường Sandbox bị ngắt hoàn toàn kết nối mạng Internet mặc định. Agent không thể gửi yêu cầu HTTP ra bên ngoài trừ khi công cụ đó được cấu hình tường minh và người dùng phê duyệt quyền truy cập mạng.
3. **Resource Quotas (Giới hạn tài nguyên thực thi):**
   - **CPU Time Limit:** Tối đa 5.000ms cho mỗi lần gọi công cụ.
   - **RAM Limit:** Tối đa 128MB bộ nhớ vật lý cho mỗi phiên thực thi công cụ.
   - **Output Size Limit:** Kết quả đầu ra bị giới hạn tối đa 1MB để tránh làm tràn bộ nhớ và cửa sổ ngữ cảnh.
