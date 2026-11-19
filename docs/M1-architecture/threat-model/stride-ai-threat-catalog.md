# PFS STRIDE-AI Threat Catalog & Attack Surface Analysis

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-SEC-CAT-001 |
| Title | STRIDE-AI Threat Catalog & Attack Surface Analysis |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Authority | Security Reviewer & Principal Systems Architect |
| Target Reviewer | Project Owner |

---

## 1. STRIDE-AI Threat Taxonomy

Hệ thống phân tích mô hình đe dọa STRIDE-AI của PFS bao quát 6 danh mục tấn công truyền thống kết hợp với các hình thức tấn công mới xuất hiện của trí tuệ nhân tạo:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           STRIDE-AI Threat Taxonomy                         │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ S - Spoofing        │ Mạo danh chủ thể, mạo danh Agent, chữ ký số giả mạo   │
│ T - Tampering       │ Prompt Injection, sửa đổi mã nguồn CAS, sửa template  │
│ R - Repudiation     │ Chối bỏ hành vi phê duyệt, thao túng audit ledger     │
│ I - Info Disclosure │ Rò rỉ dữ liệu qua prompt LLM, cross-project leakage   │
│ D - Denial of Serv. │ Bão token (DoS), tấn công vòng lặp vô tận của Agent   │
│ E - Elevation Priv. │ Leo thang quyền L1 lên L4, Confused Deputy bypass     │
└─────────────────────┴───────────────────────────────────────────────────────┘
```

## 2. Threat Catalog & Mapping to Controls

Bảng dưới đây tổng hợp 19 mối đe dọa được quản lý trong `docs/M1-architecture/matrices/threat-control-test-matrix.csv`:

1. **THR-01 (Direct Prompt Injection):** Kẻ tấn công chèn chỉ thị độc hại vào Project Intent. Kiểm soát: Tách biệt System Prompt, sử dụng XML boundary delimiters, xác thực đầu ra bằng JSON Schema.
2. **THR-02 (Indirect Prompt Injection):** Văn bản ẩn trong tài liệu nạp vào. Kiểm soát: Sanitizer làm sạch tài liệu thô, vô hiệu hóa tự động thực thi.
3. **THR-03 (Agent Confused Deputy):** Agent bị lừa gọi công cụ ngoài thẩm quyền. Kiểm soát: Tool Allowlist, kiểm tra L0–L5 tại ranh giới công cụ.
4. **THR-04 (Privilege Escalation):** Chủ thể quyền thấp cố tình gửi Command quyền cao. Kiểm soát: Policy Enforcement Point, Deny-by-default, Ed25519 signature verification.
5. **THR-05 (Cross-Project Leakage):** Rò rỉ dữ liệu giữa các dự án. Kiểm soát: Scope Isolation theo `project_id`, dọn sạch bộ nhớ phiên Agent sau mỗi task.
6. **THR-06 (Cross-Tenant Leakage):** Rò rỉ dữ liệu giữa các tổ chức. Kiểm soát: Row-Level Security theo `org_id`, kiểm tra Tenant Token.
7. **THR-07 (Secret Leakage to LLM):** Lộ API keys/passwords sang AI Provider. Kiểm soát: Secret Redaction Filter (Entropy & Regex) quét 100% dữ liệu trước khi gửi.
8. **THR-08 (Tool Abuse):** Agent lạm dụng lệnh để tấn công hệ thống khác. Kiểm soát: Ngắt mạng Sandbox mặc định (Air-gapped), giới hạn tài nguyên 5s/128MB.
9. **THR-09 (Unauthorized File Access):** Agent đọc file ngoài thư mục dự án. Kiểm soát: Filesystem Virtualization, kiểm tra `starts_with(workspace_root)`.
10. **THR-10 (Path Traversal Attack):** Đầu vào chứa `../`. Kiểm soát: Loại bỏ `..`, chuẩn hóa bằng `canonicalize()`.
11. **THR-11 (Unsafe File Overwrite):** Ghi đè file có sẵn của người dùng. Kiểm soát: Ownership Manifest, so sánh SHA-256, hiển thị Interactive Diff Preview.
12. **THR-12 (Malicious Template Injection):** Chèn mã độc vào template. Kiểm soát: Không dùng template engine có code execution, chỉ dùng pure string interpolation.
13. **THR-13 (Malicious Extension):** Plugin bên ngoài chứa trojan. Kiểm soát: Bắt buộc Code Signing Certificate, chạy trong WASM Sandbox.
14. **THR-14 (Supply-Chain Compromise):** Crate Rust bị nhiễm mã độc. Kiểm soát: Khóa Cargo.lock, quét tự động `cargo-audit` và `cargo-deny`.
15. **THR-15 (Artifact Tampering):** Chỉnh sửa lén lút file đã duyệt. Kiểm soát: Content-Addressed Storage (CAS) đối soát Merkle Root Hash trong Sổ cái.
16. **THR-16 (Replay Attack):** Gửi lại Command đã ký trong quá khứ. Kiểm soát: Bắt buộc `nonce`, `timestamp` hiệu lực 300s, `idempotency_key`.
17. **THR-17 (Duplicate Execution):** Gửi yêu cầu lặp nhiều lần. Kiểm soát: Lưu Idempotency Key trong giao dịch DB, từ chối thực thi kép.
18. **THR-18 (Unauthorized Approval):** Giả mạo chữ ký phê duyệt Owner. Kiểm soát: Kiểm tra chữ ký số Ed25519 với Public Key lưu trong Enclave an toàn.
19. **THR-19 (Provider-Side Exposure):** AI Provider dùng dữ liệu để train model. Kiểm soát: Cấu hình Zero Data Retention & Do-Not-Train header.
