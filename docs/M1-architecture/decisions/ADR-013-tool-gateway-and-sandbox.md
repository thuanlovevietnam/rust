# ADR-013 — Tool Gateway and Sandbox: Isolated WASM and Subprocess Jail Execution

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-013 |
| Title | Tool Gateway and Sandbox: Isolated WASM and Ephemeral Subprocess Jail Execution |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & Security Reviewer |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-17-TOL`, `pfs-infra` |
| Related Requirements | M1-EXE-003, M1-SEC-008, M0-AGT-007, M0-SEC-005 |
| Related Diagrams | DIA-013-security-trust-boundary.mmd |
| Invariant Reference | INV-06, INV-11 |
| Audit Remediation | Resolved finding FND-M1-04 (Evidence distinction: Target Policy vs Runtime Enforcement) and FND-M1-08 (Concrete Revisit Conditions) |

---

## 1. Context & Problem Statement

Để hỗ trợ việc thiết kế và thẩm định Foundation, các AI Agents cần sử dụng các công cụ ngoại vi: đọc tệp tài liệu, kiểm tra cú pháp schema (linting), định dạng tệp Markdown, hoặc chạy bài kiểm tra cú pháp mã nguồn.
- Nếu cho phép Agent thực thi các lệnh dòng lệnh (Shell Commands) trực tiếp trên máy chủ chủ quản mà không kiểm soát, một cuộc tấn công Prompt Injection có thể đánh lừa Agent thực thi mã độc (vd: `rm -rf /`, đánh cắp biến môi trường, tải mã độc từ internet).
- Ngay cả khi không bị tấn công, một công cụ bị treo hoặc ngốn cạn bộ nhớ RAM sẽ làm sập toàn bộ tiến trình PFS Core.
- Nguy cơ rò rỉ dữ liệu qua tool output: Nếu tool đọc dữ liệu nhạy cảm nhưng output không được gán nhãn phân loại phù hợp, dữ liệu có thể bị rò rỉ vào context chung.

Cần một cơ chế cổng kiểm soát công cụ (Tool Gateway) và môi trường thực thi cô lập an toàn (Sandbox).

---

## 2. Decision Drivers

- **Ngăn chặn triệt để mã độc & Path Traversal:** Agent không thể đọc/ghi ngoài thư mục dự án và không thể thực thi lệnh tùy ý.
- **Cách ly tài nguyên (Target Resource Limits):** Thiết lập chính sách ngưỡng tài nguyên: tối đa 5 giây CPU time, 128MB bộ nhớ RAM và không có kết nối mạng ngoại vi.
- **Kế thừa phân loại bảo mật (INV-11 & FND-M1-01):** Dữ liệu trả về từ công cụ tự động kế thừa mức phân loại bảo mật cao nhất của dữ liệu nguồn được đọc.
- **Ranh giới Bằng chứng Trung thực:** Phân biệt rõ chính sách thiết kế (Target Policy) trong M1 với việc kiểm chứng thực thi thực tế (Runtime Enforcement) trong M2/M3.

---

## 3. Options Considered

- **Option A: Direct Unrestricted Subprocess Execution:**
  - Chạy trực tiếp qua `std::process::Command` trên shell của máy chủ.
  - *Nhược điểm:* Thảm họa an ninh; mở toang cánh cửa cho Remote Code Execution (RCE) qua Prompt Injection.
- **Option B: Heavy Docker Container per Tool Execution:**
  - Khởi động một container Docker cho mỗi lần chạy công cụ.
  - *Nhược điểm:* Độ trễ khởi động quá lớn (1–3 giây/lệnh); phụ thuộc vào Docker Daemon chạy nền (không khả thi trên máy cá nhân nhẹ).
- **Option C (Được chọn): Hybrid Tool Gateway: WASM Sandbox kết hợp Ephemeral Subprocess Jail:**
  - Các công cụ xác thực, phân tích cú pháp và xử lý văn bản được đóng gói dưới dạng WebAssembly (WASM) chạy trực tiếp trong tiến trình qua thư viện `wasmtime` với độ trễ < 5ms.
  - Các công cụ nhị phân bắt buộc phải chạy ngoài (như rustfmt, git) được bao bọc trong một **Subprocess Jail** có giới hạn tài nguyên (Windows Job Objects trên Windows, `setrlimit`/namespaces trên Linux), đường dẫn được chuẩn hóa (`canonicalize()`), root hệ thống tệp chỉ đọc và ngắt kết nối mạng.

---

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Hybrid Tool Gateway (WASM Sandbox kết hợp Subprocess Jail)**.
- Áp dụng nguyên tắc **Tool Allowlist Deny-by-Default**: Chỉ những công cụ được định nghĩa rõ ràng trong Agent Profile mới được phép kích hoạt.
- Triệt tiêu hoàn toàn lỗ hổng Path Traversal: Kiểm tra nghiêm ngặt `path.canonicalize().starts_with(workspace_root)`. Mọi nỗ lực truy cập chứa `..` đều bị hủy bỏ ngay lập tức và ghi nhận vào nhật ký an ninh.
- Quản lý vòng đời thực thi bằng `tokio::time::timeout`; tự động cưỡng bức dừng (SIGKILL) nếu công cụ chạy quá 5.000ms.
- Phân định rõ ràng: Giới hạn 5s CPU và 128MB RAM là **Target Policy** được chuẩn hóa trong hợp đồng thiết kế M1 (`E2 — Specified`); việc đo kiểm thực tế trên CPU/RAM của tiến trình runtime sẽ được thực thi tại M2 và nghiệm thu tại M3 (`E4 — Executably Verified`).

---

## 5. Consequences & Trade-offs

### 5.1. Tích cực (Positive Consequences)
- An toàn an ninh tối đa, độ trễ thực thi cực thấp (< 5ms cho WASM), không phụ thuộc Docker daemon.
- Bảo vệ PFS Core không bị sập nguồn khi công cụ bên ngoài bị crash hoặc lặp vô tận.

### 5.2. Thách thức (Negative Consequences)
- Các công cụ phức tạp cần được biên dịch sang định dạng WASM hoặc viết wrapper kiểm soát chặt chẽ.
- Việc thực thi giới hạn bộ nhớ trên Windows đòi hỏi tạo Windows Job Objects qua Win32 API, phức tạp hơn so với `setrlimit` trên Linux.

---

## 6. Security & Operational Implications

- **Air-gapped Execution:** Không có quyền truy cập socket mạng (Network Egress Blocked) đối với toàn bộ các công cụ phân tích và đọc tệp.
- **Classification Inheritance:** Khi tool đọc một tệp tin có phân loại `Confidential` hoặc `Restricted`, giá trị trả về trong `ToolOutput` tự động mang nhãn phân loại tương ứng để Context Builder kiểm soát.

---

## 7. Dependencies & Compatibility

- **Phụ thuộc:** `wasmtime` runtime, `tokio::process`, Windows Job Objects (trên Windows) và POSIX syscalls (trên Linux).

---

## 8. Status & Owner Governance

- **Trạng thái:** `Proposed — Ready for Owner Review`.
- **Thẩm quyền phê duyệt:** Project Owner (Nguyễn Thế Thuận) — Bảo lưu cho quyết định OD-M1-01.
- **Bằng chứng kiến trúc:** `E2 — Specified` (Đặc tả chi tiết tại `docs/M1-architecture/04-execution-architecture/17-AI-PROVIDER-AND-TOOL-ADAPTERS.md` và `docs/M1-architecture/contracts/tool-contracts.json`).

---

## 9. Revisit Conditions

Kiến trúc Tool Gateway và Sandbox sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. **Lỗ hổng cách ly hệ điều hành:** Khi các bài kiểm thử bảo mật độc lập (Penetration Testing) trên Windows chứng minh được cơ chế Subprocess Jail có thể bị bypass qua các kỹ thuật Windows API đặc thù (như Named Pipe hijacking hoặc Token Duplication) mà không thể khắc phục được bằng Job Objects, đòi hỏi phải nâng cấp lên Micro-VM (như Firecracker hoặc WSL2 container).
2. **Nhu cầu tài nguyên vượt ngưỡng:** Khi các công cụ phân tích tĩnh hoặc linters của các dự án lớn (> 500.000 dòng code) yêu cầu vượt quá giới hạn 128MB RAM hoặc 5 giây CPU, gây lỗi Timeout/OOM trên > 20% các ca thực thi hợp lệ, đòi hỏi phải thiết lập cơ chế hạn ngạch động (Configurable Resource Quotas) được phê duyệt bởi Project Owner.
3. **Hiệu năng WASM:** Khi thời gian khởi tạo hoặc JIT compilation của module WASM trong `wasmtime` vượt quá 50ms, ảnh hưởng đến độ mượt mà của trải nghiệm tương tác dòng lệnh CLI.
