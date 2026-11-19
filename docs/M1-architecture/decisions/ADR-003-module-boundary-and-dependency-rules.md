# ADR-003 — Module Boundary and Strict Dependency Inversion Rules

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-003 |
| Title | Module Boundary and Strict Dependency Inversion Rules |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | All Modules (MOD-01..29) |
| Related Requirements | M1-SYS-001, M1-SYS-002 |
| Related Diagrams | DIA-005-dependency-graph.mmd |

---

## 1. Context & Problem Statement

Trong các dự án phát triển phần mềm dài hạn với quy mô 29 modules chuyên môn, rủi ro lớn nhất làm suy thoái kiến trúc là hiện tượng "vết dầu loang phụ thuộc" (Dependency Creep) và phụ thuộc chu trình (Cyclic Dependencies). Khi Module A phụ thuộc Module B, và Module B gọi ngược lại Module A qua một hàm tiện ích, cấu trúc hệ thống sẽ bị khóa chặt thành một khối không thể tách rời hoặc kiểm thử độc lập.

Cần xác lập các quy tắc bất biến về ranh giới module và hướng phụ thuộc được tự động hóa kiểm tra trong quy trình tích hợp liên tục (CI).

## 2. Decision Drivers
- **Zero Circular Dependencies:** Cấm tuyệt đối 100% các chu trình phụ thuộc ở mọi cấp độ (Crate, Module, Trait).
- **Phân định quyền sở hữu dữ liệu:** Mỗi bảng dữ liệu và tài nguyên hệ thống chỉ thuộc về duy nhất một module chủ quản.
- **Tự động hóa kiểm soát:** Sử dụng công cụ kiểm tra tự động phát hiện vi phạm kiến trúc ngay khi biên dịch.

## 3. Options Considered
- **Option A: Quy ước Bằng Miệng (Informal Guidelines):**
  - Viết tài liệu hướng dẫn và trông chờ lập trình viên tự giác tuân thủ.
  - *Nhược điểm:* Chắc chắn thất bại khi có nhiều người hoặc nhiều AI coding agents cùng tham gia đóng góp mã nguồn.
- **Option B (Được chọn): Kiểm soát Bằng Cấu trúc Crate và Thuật toán Đồ thị Không Chu trình (DAG Enforcement):**
  - Phân tách Cargo Workspace thành các crates độc lập có thứ tự phân tầng rõ ràng (Core -> Governance/Workflow -> App -> Infra -> CLI/Server).
  - Trình biên dịch `rustc` tự động từ chối biên dịch nếu có cyclic dependency giữa các Crates.
  - Tích hợp công cụ `tools/validation/validate_m1.py` chạy thuật toán Tarjan/DFS để quét ma trận phụ thuộc nội bộ giữa 29 modules.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Kiểm soát Bằng Cấu trúc Crate và DAG Enforcement**.
- Đồ thị phụ thuộc toàn cục bắt buộc phải là một **Directed Acyclic Graph (DAG)**.
- Khi hai module cùng tầng cần tương tác hai chiều, việc giao tiếp bắt buộc phải được đảo ngược (Inverted) thông qua một Trait Interface hoặc phát sinh một **Domain Event** bất đồng bộ qua Event Bus, triệt tiêu hoàn toàn sự phụ thuộc trực tiếp.

## 5. Consequences & Trade-offs
- *Tích cực:* Đồ thị phụ thuộc trong sạch, thời gian biên dịch song song tối ưu, dễ dàng cô lập lỗi và tái cấu trúc mã nguồn.
- *Thách thức:* Đòi hỏi đội ngũ phát triển phải thiết kế giao diện Traits cẩn thận trước khi viết code triển khai.

## 6. Revisit Conditions

Quy tắc ranh giới module và cấu trúc DAG sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi phát hiện số lượng module tăng vượt quá 40 modules hoặc độ sâu của đồ thị phụ thuộc (DAG depth) vượt quá 8 tầng, dẫn đến tình trạng suy giảm tốc độ giải quyết kiểu dữ liệu trong rustc compiler hoặc gây phân mảnh logic nghiệp vụ quá mức, đòi hỏi phải hợp nhất một số module có độ gắn kết cao (high cohesion) thành aggregate module lớn hơn.
2. Khi việc sử dụng Domain Event cho tương tác giữa các module làm tăng độ phức tạp của transaction tracing và phân tích sự cố vượt ngưỡng chấp nhận của đội ngũ vận hành.
