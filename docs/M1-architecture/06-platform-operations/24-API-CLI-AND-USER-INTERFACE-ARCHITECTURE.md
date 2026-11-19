# PFS-M1-DOC-024 — Interface Architecture: CLI, API and User Experience

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-024 |
| Document Title | Interface Architecture: CLI, REST API and User Interface Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Frontend/DX Lead |
| Classification | Internal |
| Reference Architecture | Headless Core, Single Business Semantics, OpenAPI 3.1, JSON-RPC 2.0 |
| Related Decisions | ADR-018 |

---

## 1. Single Business Semantics Principle

Theo quyết định kiến trúc **ADR-018**, **Project Foundation System (PFS)** áp dụng nguyên lý **Ngữ nghĩa Nghiệp vụ Thống nhất (Single Business Semantics)**:

> Cho dù một thao tác được kích hoạt từ Dòng lệnh CLI (`pfs`), từ Giao diện Web/Desktop, qua lời gọi REST API từ hệ thống CI/CD, hay thông qua giao diện công cụ JSON-RPC của một AI Agent, hành vi nghiệp vụ, quy tắc xác thực, cơ chế phân quyền L0–L5 và kết quả lưu vết kiểm toán bắt buộc phải **GIỐNG HẬU NHAU 100%**.

Tuyệt đối không cho phép tạo ra các "lối tắt bí mật" (backdoors) trên CLI hoặc API mà bỏ qua các bước kiểm tra của Policy Engine hay Quality Gates.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Unified Interface Gateway                          │
├─────────────────────┬─────────────────────┬─────────────────────────────────┤
│ Interface 1: CLI    │ Interface 2: API    │ Interface 3: Agent Tool RPC     │
│ Interactive / CI/CD │ REST / WebSockets   │ Headless IDE Integration        │
│ `pfs init`, `pfs gen│ /api/v1/projects    │ JSON-RPC over stdio / Unix sock │
└─────────────────────┴─────────────────────┴─────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                SHARED APPLICATION SERVICES & COMMAND PIPELINE               │
│  (Authentication -> Authorization L0-L5 -> Validation -> Core Aggregates)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Interface 1 — Command Line Interface (`pfs-cli`)

CLI là giao diện tương tác chủ lực dành cho các kỹ sư phần mềm, kiến trúc sư và hệ thống tự động hóa CI/CD:
- **Interactive Mode (Chế độ tương tác cho con người):** Cung cấp các biểu mẫu dòng lệnh trực quan (CLI Wizards bằng thư viện `dialoguer` / `inquire`), thanh tiến trình thời gian thực, bảng hiển thị màu sắc và cây sơ đồ ASCII.
- **Machine-Readable Mode (Chế độ tự động hóa cho scripts & CI):** Khi truyền cờ `--json` hoặc `--non-interactive`, CLI tắt toàn bộ màu sắc và hộp thoại; trả về kết quả thuần túy dưới dạng JSON có cấu trúc kèm theo **Mã thoát xác định (Deterministic Exit Codes)**:
  - `0`: Thành công hoàn hảo (Success).
  - `1`: Lỗi tham số đầu vào hoặc cấu hình không hợp lệ (Bad Request).
  - `2`: Vi phạm phân quyền hoặc thiếu thẩm quyền phê duyệt (Unauthorized / Forbidden).
  - `3`: Cổng chất lượng bị chặn do phát hiện lỗi nghiêm trọng (Quality Gate Blocked).
  - `4`: Phát hiện xung đột tệp tin khi sinh Foundation (File Conflict).
  - `5`: Lỗi hệ thống nội bộ hoặc sự cố nhà cung cấp AI (Internal Server / Provider Error).

---

## 3. Interface 2 — REST API & Real-time Streaming (`pfs-server`)

Khi chạy ở chế độ Daemon, PFS cung cấp hệ thống API hiện đại xây dựng trên nền tảng framework `axum` của Rust:
- **Chuẩn hóa OpenAPI 3.1:** Toàn bộ API contracts được sinh tự động từ mã nguồn Rust thông qua crate `utoipa`, lưu trữ tại `docs/M1-architecture/contracts/pfs-openapi.json`.
- **API Versioning:** Định tuyến URL chuẩn `/api/v1/...` để bảo đảm tính tương thích lâu dài.
- **Các nhóm Endpoints cốt lõi:**
  - `/api/v1/projects`: Khởi tạo, cập nhật thông tin và quản lý vòng đời dự án.
  - `/api/v1/requirements`: Tra cứu và thao tác đồ thị DAG yêu cầu.
  - `/api/v1/decisions`: Quản trị hồ sơ các quyết định kiến trúc ADRs.
  - `/api/v1/workflow`: Điều khiển chuyển đổi trạng thái 11 giai đoạn, truy vấn guards.
  - `/api/v1/generator`: Kích hoạt dry-run preview và commit gói Foundation.
  - `/api/v1/quality`: Truy xuất kết quả đánh giá cổng chất lượng và bằng chứng.
  - `/api/v1/audit`: Truy vấn sổ cái kiểm toán bất biến.
- **Server-Sent Events (SSE) & WebSocket Streaming:** Cung cấp kênh truyền tin hai chiều cho phép đẩy trực tiếp từng token do LLM sinh ra về giao diện người dùng theo thời gian thực (Real-time Token Streaming) và cập nhật tiến độ thực thi của Workflow.

---

## 4. Interface 3 — Headless Agent Tool Interface (JSON-RPC)

Để tích hợp liền mạch với các AI IDEs thế hệ mới (Cursor, Windsurf, Claude Code, GitHub Copilot Workspace):
- PFS cung cấp chế độ **Headless Agent Server** giao tiếp qua chuẩn **JSON-RPC 2.0** trên luồng Standard I/O (`stdio`) hoặc Unix Domain Socket (`.pfs/agent.sock`).
- IDEs và các Agent bên ngoài có thể gọi các công cụ của PFS như một Extension chuẩn (Model Context Protocol - MCP compatible):
  ```json
  {"jsonrpc": "2.0", "method": "pfs.query.get_requirements", "params": {"project_id": "prj_01..."}, "id": 1}
  ```
- Toàn bộ kết quả trả về đều tuân thủ đúng định dạng JSON Schema, cho phép Agent tự động phân tích cú pháp mà không cần bóc tách văn bản thô.

---

## 5. Standardized Error Response Contract

Mọi phản hồi lỗi từ API hoặc CLI JSON output đều tuân thủ chuẩn RFC 7807 (Problem Details for HTTP APIs):

```json
{
  "type": "https://pfs.dev/errors/quality-gate-blocked",
  "title": "Quality Gate Blocked by Critical Finding",
  "status": 422,
  "detail": "Giai đoạn STG-04-ARCH không thể hoàn tất do phát hiện 1 lỗi Critical về chu trình phụ thuộc.",
  "instance": "/api/v1/projects/prj_alpha/stages/STG-04-ARCH/approve",
  "correlation_id": "corr_01HQZ9G8K5E7B9A3F1M4R2V0W8",
  "timestamp": "2026-11-17T13:20:00Z",
  "invalid_params": [
    {"name": "dependency_graph", "reason": "Phát hiện chu trình phụ thuộc giữa crate_a và crate_b"}
  ],
  "remediation_guidance": "Sử dụng Trait Inversion để phá vỡ chu trình trước khi gửi lại phiếu duyệt."
}
```
