# ADR-007 — Domain Persistence Strategy: SQLite and PostgreSQL Dual Driver via SQLx

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-007 |
| Title | Domain Persistence Strategy: SQLite and PostgreSQL Dual Driver via SQLx |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `pfs-infra`, `pfs-core`, `MOD-01..29` |
| Related Requirements | M1-SYS-004, M1-OPS-001 |
| Related Diagrams | DIA-004-c4-component.mmd, DIA-014-deployment-topology.mmd |

---

## 1. Context & Problem Statement

PFS cần lưu trữ các thực thể có cấu trúc phức tạp: đồ thị quan hệ requirements (DAG), lịch sử chuyển đổi trạng thái workflow, bản ghi phân quyền L0–L5 và nhật ký kiểm toán bất biến.
- Nếu chỉ hỗ trợ PostgreSQL: Người dùng cá nhân khi chạy lệnh CLI trên máy tính xách tay sẽ gặp rào cản lớn vì phải cài đặt và duy trì máy chủ PostgreSQL, phá vỡ mục tiêu "Zero-Configuration Developer Experience".
- Nếu chỉ hỗ trợ SQLite: Hệ thống không thể phục vụ các doanh nghiệp lớn với hàng trăm người dùng đồng thời, do SQLite bị giới hạn về xử lý ghi đồng thời (Single-writer lock).

Hệ thống đòi hỏi một giải pháp lưu trữ kép (Dual Persistence Strategy) thống nhất.

## 2. Decision Drivers
- **Hỗ trợ chạy Offline/Local không cần cài đặt:** SQLite nhúng trực tiếp trong file nhị phân.
- **Hỗ trợ quy mô doanh nghiệp:** PostgreSQL cho môi trường máy chủ tập trung có tính sẵn sàng cao.
- **Mã nguồn thuần Rust và an toàn truy vấn (Compile-time Checked SQL):** Ngăn ngừa triệt để lỗi cú pháp SQL và SQL Injection ngay từ khi biên dịch.

## 3. Options Considered
- **Option A: Traditional Heavy ORM (Diesel / SeaORM):**
  - Sử dụng ORM đầy đủ để che giấu cơ sở dữ liệu.
  - *Nhược điểm:* Thời gian biên dịch rất chậm; trừu tượng hóa quá mức gây khó khăn khi cần viết các truy vấn đệ quy phức tạp trên đồ thị DAG (Recursive CTEs).
- **Option B: Pure Key-Value Embedded Store (RocksDB / Sled):**
  - Lưu trữ dạng key-value thô.
  - *Nhược điểm:* Thiếu các tính năng giao dịch ACID quan hệ, không hỗ trợ truy vấn lọc phân trang linh hoạt và khóa quan hệ toàn vẹn.
- **Option C (Được chọn): Thư viện SQLx Bất đồng bộ với Cấu trúc Repository Trait Chuẩn hóa:**
  - Định nghĩa các `RepositoryTrait` trong tầng Domain/Application.
  - Crate `pfs-infra` hiện thực hóa 2 drivers: `SqliteRepository` (Local CLI) và `PostgresRepository` (Enterprise Server) sử dụng chung các câu lệnh SQL chuẩn ANSI tương thích cao.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Thư viện SQLx với Trình điều khiển Kép SQLite / PostgreSQL**.
- Cho phép người dùng chuyển đổi giữa SQLite và PostgreSQL chỉ bằng việc thay đổi chuỗi kết nối:
  - `DATABASE_URL=sqlite://.pfs/state.db` (Chế độ Local CLI)
  - `DATABASE_URL=postgres://user:pass@host/pfs` (Chế độ Server Daemon)
- Áp dụng các bảng dữ liệu chuẩn hóa, tận dụng tính năng đệ quy `WITH RECURSIVE` của SQL để duyệt đồ thị yêu cầu và phả hệ artifacts với hiệu năng cao trên cả hai hệ quản trị.
- Tự động chạy migration thông qua `sqlx::migrate!()` lúc khởi động hệ thống.

## 5. Consequences & Trade-offs
- *Tích cực:* Thỏa mãn 100% nhu cầu của cả người dùng cá nhân lẫn doanh nghiệp; truy vấn SQL được kiểm tra kiểu dữ liệu tĩnh an toàn.
- *Thách thức:* Cần viết các câu lệnh SQL tuân thủ chuẩn tương thích chung giữa SQLite và PostgreSQL (tránh dùng các hàm đặc thù chỉ có trên một hệ quản trị).

## 6. Revisit Conditions

Kiến trúc lưu trữ Dual Persistence qua SQLx (SQLite/PostgreSQL) sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi việc duy trì tập câu lệnh SQL tương thích kép (SQLite dialect vs PostgreSQL dialect) làm tăng chi phí phát triển và kiểm thử vượt quá 30% công sức của nhóm Backend, hoặc khi xuất hiện yêu cầu phân tích đồ thị phức tạp đòi hỏi các tính năng chuyên biệt của cơ sở dữ liệu đồ thị (Graph Database như Neo4j / Apache AGE) mà câu lệnh SQL đệ quy (Recursive CTEs) không đáp ứng được SLA truy vấn (< 100ms trên đồ thị > 100.000 nodes).
2. Khi SQLite gặp hiện tượng tắc nghẽn ghi đồng thời (database table lock contention) nghiêm trọng ở chế độ Daemon đa luồng trên máy trạm cá nhân ngay cả khi đã kích hoạt Write-Ahead Logging (WAL mode), buộc phải tách riêng storage engine cho audit ledger hoặc event outbox.
