# ADR-018 — Interface Integration: Single Business Semantics Across Interfaces

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-018 |
| Title | Interface Integration: Single Business Semantics Across Interfaces |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-29-INTG`, `pfs-cli`, `pfs-server` |
| Related Requirements | M1-OPS-003, M1-SYS-003 |
| Related Diagrams | DIA-003-c4-container.mmd |

---

## 1. Context & Problem Statement

PFS cung cấp nhiều phương thức giao tiếp khác nhau: Dòng lệnh CLI (`pfs`), Dịch vụ REST API (`pfsd`), Kênh WebSocket streaming, Giao diện Web Workspace và Công cụ AI Agent JSON-RPC. Trong nhiều hệ thống phần mềm, các giao diện này thường được phát triển độc lập, dẫn đến hiện tượng phân mảnh logic (Logic Drift):
- Một số quy tắc kiểm tra phân quyền chỉ có trên Web UI mà không có trên CLI.
- Các tham số đầu vào được chấp nhận trên API nhưng lại bị từ chối trên CLI.
- Tạo ra các lỗ hổng bảo mật do bỏ qua các cổng kiểm định chất lượng khi gọi từ script tự động.

Hệ thống đòi hỏi một kiến trúc giao diện thống nhất bảo đảm cùng một ngữ nghĩa nghiệp vụ.

## 2. Decision Drivers
- **Ngữ nghĩa Nghiệp vụ Thống nhất (Single Business Semantics):** Cùng một thao tác nghiệp vụ bắt buộc phải có cùng hành vi, quy tắc phân quyền, kiểm tra hợp lệ và kết quả lưu vết bất kể được gọi từ giao diện nào.
- **Tầng giao diện không chứa Business Logic:** Toàn bộ logic nghiệp vụ nằm gọn trong Application Services và Domain Core.
- **Tiêu chuẩn giao tiếp mở:** Tuân thủ OpenAPI 3.1 cho REST và JSON-RPC 2.0 cho Agent Tools.

## 3. Options Considered
- **Option A: Interface-Specific Logic (Logic riêng cho từng giao diện):**
  - CLI gọi thẳng vào Database; REST API có controller riêng; Web UI xử lý một phần logic trên frontend.
  - *Nhược điểm:* Nợ kỹ thuật nghiêm trọng; không thể kiểm soát tính nhất quán; vi phạm nguyên lý DRY.
- **Option B (Được chọn): Headless Application Service Layer với Adapter Wrappers:**
  - Toàn bộ nghiệp vụ được gói thành các `CommandHandlers` và `QueryHandlers` độc lập trong Crate `pfs-app`.
  - Các giao diện (CLI `pfs-cli`, REST Server `pfs-server`, Agent RPC) chỉ đóng vai trò là lớp vỏ phân tích cú pháp (Parsers) và tuần tự hóa dữ liệu (Serializers).

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Headless Application Service Layer với Adapter Wrappers**.
- CLI, API và Agent Tools đều chỉ là những khách hàng (Clients) tiêu thụ chung một tập hợp các Application Commands và Queries.
- Nếu một lệnh tạo dự án (`CmdInitializeProject`) yêu cầu thẩm quyền L2 và phải thỏa mãn Intent Schema, thì quy tắc này sẽ được thi hành giống hệt nhau khi người dùng gõ `pfs init`, khi gọi `POST /api/v1/projects`, hay khi AI Agent gửi yêu cầu qua JSON-RPC.

## 5. Consequences & Trade-offs
- *Tích cực:* Đảm bảo tính nhất quán 100%; bảo mật đồng đều trên mọi kênh giao tiếp; dễ dàng phát triển thêm giao diện mới mà không sợ phá vỡ logic cũ.
- *Thách thức:* Cần thiết kế các Data Transfer Objects (DTOs) trung gian chuẩn hóa cho toàn bộ các luồng tương tác.

## 6. Revisit Conditions

Nguyên tắc Single Business Semantics và kiến trúc Headless Application Service Layer sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi phát hiện sự khác biệt không thể khắc phục về yêu cầu giao tiếp tương tác thời gian thực giữa giao diện con người (Interactive CLI Wizards / GUI) và giao diện máy đọc (CI/CD JSON scripts / Agent RPC) mà không thể giải quyết thông qua Command Payload metadata, buộc phải tách riêng một số Command tối ưu hóa cho tương tác từng bước của con người.
2. Khi giao thức truyền thông thay đổi từ REST/JSON-RPC sang gRPC nhị phân tốc độ cao trên toàn bộ hệ thống.
