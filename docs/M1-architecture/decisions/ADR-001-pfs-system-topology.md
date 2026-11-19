# ADR-001 — PFS System Topology: Modular Monolith with Optional Sidecars

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-001 |
| Title | PFS System Topology: Modular Monolith with Optional Sidecars |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | All Modules (MOD-01..29) |
| Related Requirements | M1-SYS-001, M1-OPS-001 |
| Related Diagrams | DIA-003-c4-container.mmd, DIA-014-deployment-topology.mmd |

---

## 1. Context & Problem Statement

Hệ thống Project Foundation System (PFS) cần một kiến trúc cấu trúc hệ thống (System Topology) có thể đáp ứng hai nhu cầu dường như trái ngược nhau:
1. **Trải nghiệm lập trình viên cá nhân (DX):** Cần một công cụ dòng lệnh (CLI) cực kỳ gọn nhẹ, không yêu cầu cài đặt Docker, cơ sở dữ liệu hay hạ tầng đám mây phức tạp; có thể chạy độc lập trên máy tính cá nhân trong vài giây.
2. **Khả năng mở rộng cho doanh nghiệp (Enterprise):** Có khả năng chạy như một dịch vụ nền (Daemon) phục vụ nhiều người dùng đồng thời, kết nối với hạ tầng lưu trữ đám mây và cô lập an toàn các công cụ thực thi mã độc.

Nếu chọn kiến trúc Vi dịch vụ (Microservices), hệ thống sẽ gánh chịu độ phức tạp vận hành quá lớn, độ trễ mạng trong giao tiếp nội bộ và chi phí phát triển ban đầu khổng lồ. Nếu chọn Monolith truyền thống không phân rã, hệ thống sẽ gặp rủi ro ranh giới bị xóa nhòa, khó bảo trì và không thể cô lập các công cụ ngoại vi có tính rủi ro cao.

## 2. Decision Drivers
- **Chi phí vận hành & Triển khai:** Cực kỳ tối giản cho người dùng cá nhân (Single static binary).
- **Độ trễ nội bộ:** Tối ưu hóa ở mức sub-millisecond cho các tương tác giữa Workflow, Domain và Policy.
- **Ranh giới module rõ ràng:** Bảo đảm tính độc lập giữa các phân hệ để có thể tách thành dịch vụ riêng trong tương lai nếu thực sự cần thiết.
- **Cô lập an toàn (Security Sandboxing):** Công cụ ngoại vi phải có khả năng chạy trong môi trường tiến trình riêng biệt để tránh làm sập tiến trình chính.

## 3. Options Considered

### Option A: Phân tán Vi dịch vụ Đầy đủ (Full Distributed Microservices)
- Tách riêng từng phân hệ (Workflow Service, Policy Service, Generator Service, Agent Service) thành các containers riêng biệt giao tiếp qua gRPC / Kafka.
- *Ưu điểm:* Khả năng mở rộng độc lập từng dịch vụ.
- *Nhược điểm:* Quá tải vận hành, không thể phân phối dưới dạng single CLI binary cho lập trình viên cá nhân, phát sinh bài toán phân tán dữ liệu phức tạp.

### Option B: Khối Thống nhất Không Phân rã (Monolithic Spaghetti)
- Gom toàn bộ mã nguồn vào một ứng dụng duy nhất, chia sẻ trạng thái tự do trên bộ nhớ.
- *Ưu điểm:* Phát triển nhanh ở giai đoạn đầu.
- *Nhược điểm:* Nợ kỹ thuật nghiêm trọng, xóa nhòa ranh giới nghiệp vụ, rủi ro một công cụ bị lỗi làm sập toàn bộ hệ thống.

### Option C (Được chọn): Modular Monolith kết hợp Out-of-Process Sidecars
- Toàn bộ 29 phân hệ nghiệp vụ được tổ chức thành các Crate Rust độc lập trong một Cargo Workspace, biên dịch thành một nhị phân thống nhất (`pfs` / `pfsd`).
- Riêng môi trường thực thi công cụ nguy hiểm (Tool Execution Sandbox) được thiết kế theo mô hình Sidecar (chạy trên tiến trình hoặc container cô lập riêng biệt).

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Modular Monolith kết hợp Out-of-Process Sidecars**.
- PFS Core được biên dịch thành một nhị phân Rust duy nhất, mang lại hiệu năng tối đa và sự tiện lợi tuyệt đối khi triển khai trên máy trạm cá nhân.
- Các ranh giới phân hệ được bảo vệ bằng quy tắc kiểu dữ liệu tĩnh của Rust (Visibility `pub(crate)` và `traits`), ngăn chặn việc xâm phạm ranh giới.
- Môi trường Sandbox ngoại vi chạy dưới dạng tiến trình con biệt lập hoặc WebAssembly runtime, loại bỏ nguy cơ làm gián đoạn tiến trình Core.

## 5. Consequences & Trade-offs
- *Tích cực:* Dễ triển khai, kiểm thử nhanh, độ trễ bằng 0 giữa các phân hệ, hỗ trợ cả 3 topologies (Local CLI, Team Daemon, Enterprise Cloud).
- *Thách thức:* Đòi hỏi kỷ luật cao trong việc quản lý đồ thị phụ thuộc giữa các Crates để tránh biến thành một Monolith rối rắm.

## 6. Revisit Conditions

Kiến trúc Modular Monolith kết hợp Out-of-Process Sidecars sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi số lượng kỹ sư đóng góp đồng thời vượt quá 50 người dẫn đến tình trạng tắc nghẽn biên dịch Cargo Workspace (thời gian build > 15 phút) và xung đột mã nguồn liên tục giữa các nhóm phát triển độc lập.
2. Khi một phân hệ cụ thể (ví dụ: Agent Sandbox Worker hoặc Provider Gateway) yêu cầu quy mô tài nguyên phần cứng chuyên dụng (cụm máy chủ GPU/TPU với lưu lượng > 10.000 requests/giây) đòi hỏi phải tách riêng thành microservice độc lập có chu kỳ scale tự động riêng biệt.
