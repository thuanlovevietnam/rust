# ADR-005 — Project Hierarchy and Scope: Multi-Tenancy & Scope Isolation Model

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-005 |
| Title | Project Hierarchy and Scope: Multi-Tenancy & Scope Isolation Model |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-02-ORG`, `MOD-03-PRJ`, `MOD-18-CTX` |
| Related Requirements | M1-DOM-001, M1-SEC-005 |
| Related Diagrams | DIA-006-universal-domain-model.mmd, DIA-013-security-trust-boundary.mmd |

---

## 1. Context & Problem Statement

PFS được thiết kế để phục vụ từ một nhà phát triển độc lập cho đến các tập đoàn công nghệ lớn với hàng ngàn dự án cùng hoạt động. Trong môi trường dùng chung tài nguyên (Multi-Tenant & Multi-Project):
- Một dự án độc lập (Standalone Project) không được phép nhìn thấy hoặc truy cập dữ liệu của một dự án khác nếu không được chia sẻ tường minh.
- Các tập đoàn cần quản lý danh mục đầu tư (Portfolio) bao gồm Dự án Cha (Parent Project) và các Dự án Con (Subprojects) với khả năng kế thừa tri thức chung nhưng vẫn bảo đảm cô lập quyền hạn.
- Sự rò rỉ dữ liệu qua lại giữa các dự án (Cross-Project Leakage) thông qua bộ nhớ đệm hoặc ngữ cảnh AI là rủi ro an ninh nghiêm trọng.

## 2. Decision Drivers
- **Cách ly phạm vi nghiêm ngặt (Strict Scope Isolation):** Ngăn chặn 100% việc truy cập trái phép giữa các tổ chức (Tenants) và giữa các dự án (Projects).
- **Phân cấp linh hoạt (Hierarchical Flexibility):** Hỗ trợ dự án độc lập, cấu trúc cha-con (Subprojects) và danh mục dự án (Portfolios).
- **Chia sẻ tri thức có kiểm soát:** Cho phép chia sẻ các Templates và Best Practices dùng chung ở cấp độ Organization mà không làm lộ dữ liệu kinh doanh của từng dự án.

## 3. Options Considered
- **Option A: Physical Database-Per-Tenant / Database-Per-Project:**
  - Mỗi dự án hoặc tổ chức có một tệp SQLite hoặc một database PostgreSQL riêng biệt.
  - *Ưu điểm:* Cách ly vật lý tuyệt đối.
  - *Nhược điểm:* Quá tải tài nguyên khi có hàng ngàn dự án; không thể thực hiện truy vấn tổng hợp trên danh mục đầu tư (Portfolio View).
- **Option B (Được chọn): Logical Multi-Tenancy with Hierarchical Scope Envelope:**
  - Sử dụng cơ sở dữ liệu chung với ranh giới phân cấp logic 3 tầng: `Organization` (Root Tenant) -> `Workspace` (Resource Boundary) -> `Project` (Execution Unit).
  - Mọi thực thể trong hệ thống đều bắt buộc gắn nhãn `tenant_id`, `workspace_id` và `project_id`.
  - Áp dụng Row-Level Security (RLS) trên PostgreSQL và Scoped Query Filters trên SQLite.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Logical Multi-Tenancy with Hierarchical Scope Envelope**.
- Hệ thống áp dụng cấu trúc định danh phạm vi chuẩn:
  `pfs:<entity_type>:<workspace_id>:<project_id>:<ulid>`
- Mọi câu lệnh Command và Query khi đi qua Application Layer đều tự động được bao bọc trong một `SecurityScopeContext`. Nếu chủ thể phát lệnh không sở hữu quyền truy cập vào `project_id` đích, hệ thống lập tức từ chối ở tầng phân quyền trước khi chạm vào cơ sở dữ liệu.
- Đối với quan hệ Cha-Con: Dự án con kế thừa các quy định quản trị và templates của dự án cha, nhưng dữ liệu artifacts và secrets của dự án con được bảo vệ độc lập.

## 5. Consequences & Trade-offs
- *Tích cực:* Tiết kiệm tài nguyên tối đa, dễ dàng quản lý tập trung, hỗ trợ cả môi trường máy trạm lẫn đám mây doanh nghiệp.
- *Thách thức:* Mọi câu lệnh SQL đều bắt buộc phải có điều kiện lọc theo Scope Context, đòi hỏi kiểm tra tự động để ngăn ngừa lập trình viên quên mệnh đề `WHERE project_id = ...`.

## 6. Revisit Conditions
Tái đánh giá kiến trúc Database-Per-Tenant vật lý chỉ khi: Khách hàng thuộc khối Ngân hàng / Quốc phòng yêu cầu chứng chỉ cách ly phần cứng và khóa mã hóa dữ liệu độc lập (BYOK) theo luật định.
