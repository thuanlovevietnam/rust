# PFS-M1-DOC-023 — Deployment Topology and Operations Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-023 |
| Document Title | Deployment Topology and Operations Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & SRE Lead |
| Classification | Internal |
| Reference Architecture | Modular Monolith, Multi-Topology Deployment, 12-Factor App |
| Related Diagrams | DIA-014-deployment-topology.mmd |
| Related Decisions | ADR-001, ADR-007, ADR-019 |

---

## 1. Deployment Topology Strategy & Rationale

Theo quyết định kiến trúc chiến lược **ADR-001**, **Project Foundation System (PFS)** bác bỏ xu hướng lạm dụng vi dịch vụ phân tán (Microservices Over-engineering) trong giai đoạn khởi nguyên. Thay vào đó, PFS áp dụng mô hình **Modular Monolith với Sidecar Độc lập Tùy chọn (Modular Monolith with Optional Out-of-Process Sidecars)**.

Mô hình này mang lại 4 lợi ích vượt trội:
1. **Zero-Configuration Local Developer Experience:** Toàn bộ hệ thống có thể đóng gói thành duy nhất một tệp nhị phân độc lập (`pfs` binary) chạy trực tiếp trên máy trạm của lập trình viên mà không cần cài đặt Docker hay máy chủ database phức tạp.
2. **Sub-millisecond Inter-Module Latency:** Giao tiếp giữa các module diễn ra trực tiếp qua lời gọi hàm nội bộ (In-memory function calls), giảm thiểu độ trễ mạng và chi phí tuần tự hóa JSON.
3. **Seamless Multi-Topology Scaling:** Cùng một mã nguồn Rust có thể triển khai linh hoạt ở 3 hình thái cấu hình khác nhau mà không phải thay đổi logic nghiệp vụ.
4. **Operational Simplicity:** Giảm thiểu tối đa chi phí vận hành máy chủ, giám sát và gỡ lỗi phân tán.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Three Deployment Topologies of PFS                     │
├─────────────────────┬─────────────────────┬─────────────────────────────────┤
│ Mode 1: Local CLI   │ Mode 2: Team Daemon │ Mode 3: Enterprise Cloud        │
│ Single User / Local │ Small Team / LAN    │ Scalable Enterprise Cluster     │
│ - 1 Static Binary   │ - Background Daemon │ - Multi-replica PFS Pods        │
│ - Embedded SQLite   │ - Dual DB (SQLite/PG│ - Cloud Managed PostgreSQL (RDS)│
│ - Local Disk CAS    │ - Local Shared CAS  │ - S3-compatible CAS (MinIO/AWS) │
│ - In-Process Engine │ - REST & WebSockets │ - OIDC / SSO Authentication     │
└─────────────────────┴─────────────────────┴─────────────────────────────────┘
```

---

## 2. The Three Canonical Deployment Topologies

### 2.1. Topology 1 — Local Developer CLI Mode (`pfs`)
- **Đối tượng:** Lập trình viên đơn lẻ, nhà nghiên cứu, người dùng cá nhân muốn tạo Foundation nhanh chóng trên máy tính xách tay.
- **Thành phần:** Duy nhất 1 file thực thi nhị phân (`pfs` hoặc `pfs.exe`), kích thước ~25MB.
- **Cơ sở dữ liệu:** SQLite nhúng trực tiếp trong tiến trình (`.pfs/state.db`), kích hoạt chế độ WAL (Write-Ahead Logging).
- **Lưu trữ tạo tác (CAS):** Thư mục cục bộ `.pfs/cas/objects/`.
- **Thực thi công cụ:** Tiến trình con (Subprocess jail) trên máy trạm.
- **Tài nguyên tối thiểu:** 1 CPU Core, 128MB RAM, 100MB ổ đĩa.

### 2.2. Topology 2 — Team Daemon Mode (`pfsd`)
- **Đối tượng:** Đội ngũ phát triển từ 5 đến 30 người làm việc trong cùng mạng nội bộ hoặc máy chủ chia sẻ của công ty.
- **Thành phần:** Tiến trình Daemon chạy nền `pfsd` lắng nghe cổng HTTP/WebSocket (mặc định: `0.0.0.0:8080`), kết hợp CLI client `pfs` và Web UI.
- **Cơ sở dữ liệu:** PostgreSQL 16+ hoặc SQLite chia sẻ trên máy chủ tệp tin tốc độ cao.
- **Lưu trữ tạo tác:** Network File System (NFS / SMB) hoặc máy chủ MinIO cục bộ.
- **Xác thực:** API Keys cục bộ hoặc Local User Accounts.

### 2.3. Topology 3 — Enterprise Cloud Cluster Mode
- **Đối tượng:** Doanh nghiệp quy mô lớn với hàng trăm kỹ sư và hàng ngàn dự án đồng thời.
- **Thành phần:** Các container Pods `pfsd` không trạng thái (Stateless Pods) chạy trên Kubernetes, đứng sau Application Load Balancer.
- **Cơ sở dữ liệu:** PostgreSQL Cluster có High Availability (vd: Amazon Aurora, Cloud SQL) với Connection Pooling qua `PgBouncer`.
- **Lưu trữ tạo tác:** AWS S3 / Google Cloud Storage với mã hóa dữ liệu tĩnh (AES-256).
- **Thực thi công cụ:** Cụm Sandbox Worker chuyên biệt chạy WebAssembly hoặc gVisor containers cách ly.
- **Xác thực:** Tích hợp Enterprise Identity Provider qua OpenID Connect (OIDC / OAuth 2.0).

---

## 3. Operational Lifecycle & Zero-Downtime Migration

Quy trình vận hành và khởi động hệ thống tuân thủ 6 giai đoạn xác định:
1. **Preflight Environment Validation:** Kiểm tra biến môi trường, kết nối cơ sở dữ liệu, quyền ghi đĩa và phiên bản công cụ.
2. **Deterministic Schema Migration:** Tự động thực thi các script migration cơ sở dữ liệu thông qua `sqlx::migrate!()`. Áp dụng chiến lược **Expand-and-Contract** để bảo đảm tính tương thích ngược, cho phép cập nhật hệ thống mà không phải dừng dịch vụ (Zero-Downtime Migration).
3. **Integrity Hash Check:** Kiểm tra mã băm của các mẫu template hệ thống và tệp cấu hình cốt lõi.
4. **Service Health & Readiness Probes:**
   - `GET /health/liveness`: Trả về HTTP 200 nếu tiến trình Rust đang hoạt động bình thường.
   - `GET /health/readiness`: Trả về HTTP 200 nếu kết nối Database, Storage và AI Gateway đều sẵn sàng tiếp nhận yêu cầu.
5. **Graceful Shutdown Protocol:** Khi nhận tín hiệu `SIGTERM` / `SIGINT`:
   - Ngừng tiếp nhận các Command mới.
   - Chờ tối đa 30 giây để các tác vụ Agent đang chạy hoàn thành bước hiện tại hoặc lưu Checkpoint an toàn.
   - Đóng các kết nối cơ sở dữ liệu và ngắt kênh I/O an toàn.
6. **Disaster Recovery & Backup Policy:** Hỗ trợ lệnh sao lưu nguyên tử `pfs admin backup --output backup.tar.zst` đóng gói toàn bộ metadata database và blob store trong trạng thái đóng băng nhất quán.
