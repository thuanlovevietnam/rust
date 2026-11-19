# ADR-004 — Universal Domain Identity: ULID and UUIDv7 Specification

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-004 |
| Title | Universal Domain Identity: ULID and UUIDv7 Specification |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `pfs-core`, `MOD-01-IAM` to `MOD-29-INTG` |
| Related Requirements | M1-DOM-001 |
| Related Diagrams | DIA-006-universal-domain-model.mmd |

---

## 1. Context & Problem Statement

Trong một hệ thống quản lý dự án đa miền (Universal Project Model) với hàng ngàn thực thể (Projects, Requirements, Decisions, Tasks, Artifacts, Evidence, Audit Logs), việc lựa chọn chuẩn định danh (Identity Strategy) ảnh hưởng trực tiếp đến hiệu năng cơ sở dữ liệu, khả năng phân tán dữ liệu và trải nghiệm tra cứu của người dùng:
- Số nguyên tự tăng (Auto-incrementing Integer IDs) làm lộ quy mô hệ thống, dễ bị tấn công duyệt tuần tự (Enumeration attack) và gây xung đột nghiêm trọng khi phân tán hoặc đồng bộ hóa đa máy trạm.
- UUIDv4 truyền thống (Random UUID) giải quyết được tính duy nhất nhưng lại phân bố ngẫu nhiên hoàn toàn, dẫn đến hiện tượng phân mảnh chỉ mục cơ sở dữ liệu (B-Tree Index Fragmentation) làm suy giảm hiệu năng nghiêm trọng khi dữ liệu lớn.
- Đường dẫn tệp tin (File Path) hoặc Tên hiển thị (Display Name) thường xuyên bị người dùng đổi tên trong vòng đời dự án, không thể dùng làm định danh khóa chính bất biến.

## 2. Decision Drivers
- **Tính duy nhất toàn cầu (Global Uniqueness):** Khả năng sinh ID độc lập trên máy trạm của client mà không cần kết nối máy chủ tập trung (No ID collision).
- **Tính sắp xếp theo thời gian (Lexicographical Time-Sortability):** Khóa chính được sắp xếp theo thời gian tạo lập, tối ưu hóa tối đa hiệu năng lập chỉ mục B-Tree và phân trang (Cursor Pagination).
- **Định dạng ngắn gọn, thân thiện (URL-safe & Human-readable):** Dễ dàng truyền tải qua URL, dòng lệnh CLI và thông điệp JSON mà không bị lỗi mã hóa.

## 3. Options Considered
- **Option A: UUIDv4 (Random UUID):** 128-bit hoàn toàn ngẫu nhiên.
  - *Nhược điểm:* Phân mảnh chỉ mục B-Tree, không sắp xếp được theo thời gian tạo.
- **Option B: Auto-incrementing BigInt / Snowflake IDs:**
  - *Nhược điểm:* Đòi hỏi máy chủ phối hợp tập trung để tránh trùng lặp; không phù hợp với chế độ Local CLI offline.
- **Option C (Được chọn): ULID (Universally Unique Lexicographically Sortable Identifier) / UUIDv7:**
  - 128-bit bao gồm 48-bit timestamp (độ chính xác mili-giây) + 80-bit ngẫu nhiên mật mã (Crockford's Base32).
  - Định dạng chuỗi 26 ký tự thân thiện: `01HQZ9G8K5E7B9A3F1M4R2V0W8`.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: ULID (kết hợp ánh xạ tương đương UUIDv7)** làm định danh chuẩn cho toàn bộ thực thể trong PFS Core.
- Mọi bản ghi được tạo ra đều tự động mang theo mốc thời gian (Timestamp) mà không cần thêm trường `created_at` riêng biệt khi lập chỉ mục.
- Hiệu năng ghi cơ sở dữ liệu (Insert Throughput) đạt tốc độ tối đa vì các bản ghi mới luôn được chèn tuần tự vào cuối cây chỉ mục B-Tree (Clustered Index), triệt tiêu hiện tượng Page Split.
- Tách bạch tuyệt đối 3 khái niệm: **Entity Identity (ULID bất biến)** $\neq$ **Display Name (có thể đổi)** $\neq$ **File Path (vị trí lưu trữ logic)**.

## 5. Consequences & Trade-offs
- *Tích cực:* Hiệu năng DB vượt trội, an toàn phân tán, thân thiện với URL và dòng lệnh CLI.
- *Thách thức:* Người dùng thông thường cần làm quen với chuỗi ký tự Base32 thay vì các con số nguyên đơn giản 1, 2, 3.

## 6. Revisit Conditions

Chiến lược định danh ULID/UUIDv7 sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi xuất hiện yêu cầu tích hợp bắt buộc với các hệ thống di sản của khách hàng doanh nghiệp hoặc tiêu chuẩn ngành chỉ chấp nhận định dạng định danh cố định khác (ví dụ: chuỗi định danh phân cấp OID của viễn thông hoặc UUIDv4 ngẫu nhiên thuần túy) mà không thể giải quyết thông qua adapter mapping ở tầng Presentation.
2. Khi tần suất sinh thực thể đồng thời trong một node vượt quá 100.000 IDs/mili-giây dẫn đến rủi ro tràn bit ngẫu nhiên trong cùng millisecond timestamp.
