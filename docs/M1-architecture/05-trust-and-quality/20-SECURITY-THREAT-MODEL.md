# PFS-M1-DOC-020 — Security Architecture & STRIDE-AI Threat Model

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-020 |
| Document Title | Security Architecture and STRIDE-AI Threat Model Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.1.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Security Reviewer |
| Classification | Internal |
| Reference Framework | STRIDE-AI, OWASP Top 10 for LLM Applications, NIST SP 800-218 (SSDF) |
| Related Diagrams | DIA-013-security-trust-boundary.mmd |
| Related Decisions | ADR-012, ADR-013, ADR-014 |
| Parent Baseline | [PFS-M0-SPEC-009](file:///C:/Users/OK259/rust/docs/M0-foundation/09-AGENT-SECURITY-MODEL.md), [PFS-M0-SPEC-012](file:///C:/Users/OK259/rust/docs/M0-foundation/12-SECURITY-AND-SUPPLY-CHAIN.md) |
| Invariant Reference | INV-06, INV-11, INV-12 |
| Audit Remediation | Resolved finding FND-M1-01 (Metadata Boundary Enforcement, Fail-Secure Dispatch) |

---

## 1. Security Architecture Principles

Kiến trúc an ninh của **Project Foundation System (PFS)** được thiết kế dựa trên triết lý **Security-by-Design** và **Zero Trust**. Trong một hệ thống kết hợp giữa phần mềm xác định và trí tuệ nhân tạo, nguy cơ an ninh không chỉ đến từ các cuộc tấn công mạng truyền thống (như SQL Injection, Buffer Overflow) mà còn đến từ các bề mặt tấn công mới xuất hiện do AI (Prompt Injection, Data Poisoning, Confused Deputy, Hallucination-driven Exploits).

Hệ thống bảo đảm 4 trụ cột an ninh cốt lõi:
1. **Zero Trust Architecture:** Mọi yêu cầu truy cập, cho dù xuất phát từ mạng nội bộ, tiến trình máy trạm hay từ một AI Agent đã được xác thực, đều phải được kiểm tra tính hợp lệ và thẩm quyền tại thời điểm thực thi.
2. **Deterministic Security Boundary:** An ninh hệ thống không bao giờ được đặt niềm tin vào "lời hứa" hoặc "hướng dẫn trong prompt" của LLM. Mọi ranh giới kiểm soát an ninh bắt buộc phải được thi hành bằng mã nguồn xác định trong Rust Core.
3. **Defense-in-Depth (Phòng thủ đa tầng):** Áp dụng nhiều lớp bảo vệ độc lập: phân loại dữ liệu -> PEP/PDP context filtering -> lọc bí mật regex/entropy -> phân quyền L0–L5 -> cô lập sandbox -> mã băm toàn vẹn CAS -> kiểm toán bất biến.
4. **Comprehensive Threat-Control-Test Traceability:** Mọi mối đe dọa an ninh đều phải được liên kết trực tiếp với biện pháp kiểm soát, module chịu trách nhiệm, bài kiểm thử và bằng chứng kiểm chứng.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STRIDE-AI Threat Model & Defense-in-Depth                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Layer 1: Metadata Classification & Context PEP/PDP (Strict Deny Restricted)│
│  Layer 2: Input Sanitization & Secret Redaction (Entropy & Regex patterns)  │
│  Layer 3: Identity & L0–L5 Authorization (Deny-by-default, SoD enforcement) │
│  Layer 4: Ephemeral Sandbox Isolation (WASM / Jail, path canonicalization)  │
│  Layer 5: CAS Integrity Verification (SHA-256 Merkle DAG, tampering detect) │
│  Layer 6: Append-Only Cryptographic Audit Ledger (Ed25519 signatures)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Trust Boundaries and Attack Surfaces

PFS xác lập 4 ranh giới tin cậy (Trust Boundaries) được thể hiện tại sơ đồ `DIA-013-security-trust-boundary.mmd`:
- **TB-1 (User to PFS Boundary):** Giao thức CLI/HTTP. Bề mặt tấn công: Tham số độc hại, Path Traversal qua đường dẫn tệp tin, DoS bằng gói tin khổng lồ.
- **TB-2 (Application to Domain Core Boundary):** Lời gọi hàm nội bộ Rust. Bề mặt tấn công: Giả mạo danh tính chủ thể, leo thang đặc quyền từ L1 lên L4.
- **TB-3 (PFS Core to External AI Boundary):** Giao thức HTTPS TLS 1.3. Bề mặt tấn công: Direct & Indirect Prompt Injection, rò rỉ dữ liệu nhạy cảm sang máy chủ bên thứ ba, vi phạm điều khoản lưu trữ nhà cung cấp.
- **TB-4 (PFS Core to Tool Execution Sandbox):** Giao thức gRPC / IPC / WASM Memory Boundary. Bề mặt tấn công: Thoát khỏi sandbox (Sandbox escape), lạm dụng công cụ (Tool abuse), ghi đè tệp tin hệ thống.

---

## 3. Comprehensive Analysis of 19 Security Threats

Dưới đây là bảng phân tích toàn diện 19 mối đe dọa an ninh bắt buộc theo yêu cầu M1 (kèm trạng thái bằng chứng M1 và kế hoạch triển khai M2–M4):

| Threat ID | Tên mối đe dọa (Threat Scenario) | Phân loại STRIDE-AI | Đường tấn công (Attack Path) | Biện pháp kiểm soát kiến trúc (Controls) | Module phụ trách | Bằng chứng M1 & Verification Plan |
|---|---|---|---|---|---|---|
| **THR-01** | **Direct Prompt Injection** | Tampering / Elevation | Người dùng chèn chỉ thị độc hại vào Project Intent để ép Agent bỏ qua quy tắc quản trị. | Tách biệt rạch ròi giữa System Prompt bất biến và User Context; sử dụng XML boundary delimiters; kiểm tra kết quả bằng JSON Schema xác định. | `MOD-18-CTX`, `MOD-16-GWY` | `E2 — Specified` (Test contract: `test_direct_prompt_injection_blocked` in M2 WP-M2-03) |
| **THR-02** | **Indirect Prompt Injection** | Tampering / Information Disclosure | Tài liệu đầu vào của dự án (PDF/Markdown) chứa văn bản ẩn đánh lừa Agent trích xuất dữ liệu bí mật. | Bộ lọc Context Sanitizer trích xuất văn bản thô, làm sạch thẻ lệnh; vô hiệu hóa khả năng thực thi code tự động từ ngữ cảnh. | `MOD-18-CTX` | `E2 — Specified` (Test contract: `test_indirect_injection_payload_ignored` in M2 WP-M2-04) |
| **THR-03** | **Agent Confused Deputy** | Elevation of Privilege | Agent bị thao túng để gọi các công cụ hợp lệ nhưng với tham số độc hại (ví dụ: yêu cầu đọc file nhạy cảm). | Áp đặt Tool Allowlist nghiêm ngặt; kiểm tra thẩm quyền L0–L5 trước mỗi lời gọi công cụ; con người duyệt thao tác ghi đè. | `MOD-17-TOL`, `MOD-11-POL` | `E2 — Specified` (Test contract: `test_confused_deputy_tool_blocked` in M2 WP-M2-02) |
| **THR-04** | **Privilege Escalation** | Elevation of Privilege | Agent hoặc người dùng có quyền L1/L2 cố gắng kích hoạt các Commands yêu cầu quyền L3–L5. | Policy Engine kiểm tra Token thẩm quyền tại ranh giới Command; Deny-by-default; xác minh chữ ký Ed25519 cho quyền L5. | `MOD-11-POL`, `MOD-01-IAM` | `E2 — Specified` (Test contract: `test_privilege_escalation_denied` in M2 WP-M2-02) |
| **THR-05** | **Cross-Project Leakage** | Information Disclosure | Dữ liệu nhạy cảm của Dự án A bị rò rỉ sang Dự án B thông qua bộ nhớ đệm (Cache) hoặc Ngữ cảnh Agent. | Cách ly phạm vi tuyệt đối (Scope Isolation by `project_id`); cô lập phiên làm việc của Agent; xóa sạch bộ nhớ tạm sau mỗi task. | `MOD-03-PRJ`, `MOD-18-CTX` | `E2 — Specified` (Test contract: `test_cross_project_isolation` in M2 WP-M2-01) |
| **THR-06** | **Cross-Tenant Leakage** | Information Disclosure | Người dùng của Tổ chức (Org) X truy cập trái phép tài nguyên của Tổ chức Y trong môi trường multi-tenant. | Phân vùng logic cơ sở dữ liệu dựa trên `org_id` (Row-Level Security / SQLx scoping); kiểm tra tính hợp lệ của Tenant Token. | `MOD-02-ORG`, `MOD-01-IAM` | `E2 — Specified` (Test contract: `test_cross_tenant_access_forbidden` in M2 WP-M2-06) |
| **THR-07** | **Restricted / Secret Leakage to LLM** | Information Disclosure | Dữ liệu Restricted hoặc secrets/API keys bị gửi ra AI Provider bên ngoài. | **Dual Control:** (1) Metadata-based PEP/PDP enforcement chặn đứng dữ liệu `Restricted`/Unclassified; (2) Secret Redaction pipeline (regex & entropy). | `MOD-18-CTX`, `MOD-16-GWY`, `MOD-22-DATA` | `E2 — Specified` (Test contract: `SEC-TEST-01`, `SEC-TEST-06` in M2 WP-M2-03) |
| **THR-08** | **Tool Abuse** | Elevation / Tampering | Agent lạm dụng công cụ thực thi dòng lệnh để đào coin hoặc tấn công DoS các dịch vụ khác. | Ngắt toàn bộ kết nối mạng trong Sandbox (Air-gapped); chỉ cho phép các công cụ nội kiểm định (Linters, Validators). | `MOD-17-TOL` | `E2 — Specified` (Test contract: `test_tool_network_access_blocked` in M2 WP-M2-04) |
| **THR-09** | **Unauthorized File Access** | Information Disclosure | Agent cố tình đọc các tệp tin ngoài thư mục dự án (ví dụ: `/etc/shadow`, `C:\Windows\System32`). | Filesystem Virtualization; chuẩn hóa đường dẫn bằng `canonicalize()`; từ chối nếu không nằm trong `workspace_root`. | `MOD-17-TOL`, `MOD-20-ART` | `E2 — Specified` (Test contract: `test_unauthorized_path_access_denied` in M2 WP-M2-05) |
| **THR-10** | **Path Traversal Attack** | Tampering / Information Disclosure | Đầu vào chứa các chuỗi `../` hoặc `..\` để thoát khỏi thư mục chỉ định. | Kiểm tra tiền xử lý loại bỏ toàn bộ `..`; kiểm tra độ dài đường dẫn; bắt buộc sử dụng `Path::starts_with(root)`. | `MOD-20-ART`, `MOD-22-GEN` | `E2 — Specified` (Test contract: `test_path_traversal_detection` in M2 WP-M2-05) |
| **THR-11** | **Unsafe File Overwrite** | Tampering / Repudiation | Generator vô tình hoặc cố ý ghi đè lên các tệp tin mã nguồn có sẵn của người dùng làm mất dữ liệu. | Kiểm tra Ownership Manifest; so sánh mã băm SHA-256; tạm dừng tiến trình và hiển thị Interactive Diff Preview khi xung đột. | `MOD-22-GEN` | `E2 — Specified` (Test contract: `test_safe_overwrite_conflict_halt` in M2 WP-M2-05) |
| **THR-12** | **Malicious Template Injection** | Tampering | Mẫu template bị chèn mã độc (vd: Jinja code execution) để thực thi lệnh tùy ý khi render. | Không sử dụng template engine cho phép thực thi code tùy ý; chỉ dùng pure string interpolation hoặc logic-less mustache. | `MOD-21-TPL`, `MOD-22-GEN` | `E2 — Specified` (Test contract: `test_template_arbitrary_code_rejected` in M4) |
| **THR-13** | **Malicious Plugin Extension** | Tampering / Elevation | Tiện ích mở rộng do bên thứ ba cung cấp chứa trojan hoặc đánh cắp dữ liệu dự án. | Bắt buộc kiểm tra chữ ký số của Extension Provider; chạy tiện ích mở rộng trong môi trường cô lập WebAssembly (WASM). | `MOD-06-CAP`, `MOD-17-TOL` | `E2 — Specified` (Test contract: `test_unsigned_extension_rejected` in M3) |
| **THR-14** | **Supply-Chain Compromise** | Tampering | Các thư viện crate phụ thuộc trong Rust bị nhiễm mã độc hoặc có lỗ hổng bảo mật đã biết. | Khóa phiên bản `Cargo.lock`; kiểm tra lỗ hổng tự động định kỳ bằng `cargo-audit` và `cargo-deny`; cấm dependency chưa kiểm duyệt. | `pfs-infra`, `pfs-core` | `E3 — Statically Validated` (Security policy defined; CI static check in M2) |
| **THR-15** | **Artifact Tampering** | Tampering | Kẻ tấn công sửa đổi nội dung tệp tin đã được phê duyệt trực tiếp trên đĩa cứng. | Áp dụng Content-Addressed Storage (CAS); kiểm tra đối chiếu mã băm SHA-256 đối với Merkle Root Hash trong Sổ cái. | `MOD-20-ART`, `MOD-24-EVI` | `E2 — Specified` (Test contract: `test_tampered_artifact_detected` in M3) |
| **THR-16** | **Replay Attack** | Repudiation / Elevation | Kẻ tấn công chặn bắt và gửi lại một Command hợp lệ đã được ký trong quá khứ. | Mỗi Command bắt buộc phải có `nonce`, `timestamp` (hiệu lực trong 300s) và `idempotency_key` duy nhất. | `MOD-01-IAM`, `MOD-29-INTG` | `E2 — Specified` (Test contract: `test_replayed_command_rejected` in M2 WP-M2-02) |
| **THR-17** | **Duplicate Execution** | Denial of Service | Yêu cầu sinh Foundation bị gửi lặp lại nhiều lần do lỗi mạng hoặc người dùng click liên tục. | Lưu trữ trạng thái `IdempotencyKey` trong cơ sở dữ liệu giao dịch; từ chối thực thi kép và trả về kết quả đang chạy. | `MOD-12-WKF`, `MOD-22-GEN` | `E2 — Specified` (Test contract: `test_duplicate_execution_deduped` in M2 WP-M2-05) |
| **THR-18** | **Unauthorized Approval** | Repudiation / Elevation | AI Agent hoặc người dùng mạo danh chữ ký của Project Owner để thông qua Milestone Baseline. | Xác thực chữ ký số mã hóa Ed25519 bằng Public Key của Project Owner được lưu trữ an toàn trong Secure Enclave. | `MOD-10-GOV`, `MOD-19-AUTH`| `E2 — Specified` (Test contract: `test_forged_approval_signature_denied` in M2 WP-M2-02) |
| **THR-19** | **Provider-Side Exposure** | Information Disclosure | Dữ liệu gửi sang OpenAI/Anthropic bị các nhà cung cấp sử dụng để huấn luyện mô hình công cộng. | Kích hoạt cờ cấu hình Do-Not-Train / Zero-Retention thông qua Enterprise Agreement Header (`opt-out: true`). | `MOD-16-GWY` | `E2 — Specified` (Test contract: `test_provider_zero_retention_flag` in M2 WP-M2-03) |

---

## 4. Threat-Control-Test Bidirectional Traceability

Mọi mối đe dọa trong danh mục trên đều được kết nối hai chiều thành ma trận:
$$\mathbf{Threat} \longleftrightarrow \mathbf{Attack\ Path} \longleftrightarrow \mathbf{Security\ Control} \longleftrightarrow \mathbf{Module} \longleftrightarrow \mathbf{Requirement} \longleftrightarrow \mathbf{Verification\ Plan} \longleftrightarrow \mathbf{Evidence\ Level}$$

Ma trận chi tiết được cập nhật đồng bộ tại `docs/M1-architecture/matrices/threat-control-test-matrix.csv` và được kiểm định tự động bởi `tools/validation/validate_m1.py`.
