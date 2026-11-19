# ADR-009 — Workflow State and Execution Model: Hierarchical FSM and Saga Orchestrator

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-009 |
| Title | Workflow State and Execution Model: Hierarchical FSM and Saga Orchestrator |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-12-WKF`, `MOD-13-TSK`, `MOD-15-ORC` |
| Related Requirements | M1-EXE-001, M1-DOM-002 |
| Related Diagrams | DIA-007-foundation-lifecycle.mmd, DIA-008-workflow-state-machine.mmd |

---

## 1. Context & Problem Statement

Quy trình tạo lập Project Foundation là một tiến trình kéo dài (Long-Running Process) bao gồm 11 giai đoạn vĩ mô, hàng trăm nhiệm vụ vi mô của các AI Agents và các bước kiểm định chất lượng, phê duyệt con người. Trong quá trình này:
- Hệ thống có thể bị sập đột ngột (Power loss, OS crash) khi một tác vụ đang chạy dở dang.
- Một số bước có tác động ngoại vi (như gọi LLM tốn phí hoặc ghi tệp vào đĩa) có thể thành công nhưng bước tiếp theo bị lỗi.
- Cần ngăn ngừa tình trạng thực thi trùng lặp (Duplicate Execution) và bảo đảm khả năng khôi phục (Recovery) hoặc bồi hoàn (Compensation).

## 2. Decision Drivers
- **Tính xác định (Determinism):** Mọi trạng thái và bước chuyển đổi phải được kiểm soát bằng quy tắc logic chặt chẽ; không có trạng thái "mơ hồ".
- **Khả năng chịu lỗi và Phục hồi (Crash Resilience):** Khi khởi động lại sau sự cố, hệ thống phải tự động phục hồi về điểm kiểm tra an toàn (Checkpoint) gần nhất mà không làm hỏng dữ liệu.
- **Hỗ trợ con người tham gia (Human-in-the-Loop):** Khả năng tạm dừng an toàn để chờ quyết định phê duyệt và tiếp tục chạy khi có tín hiệu.

## 3. Options Considered
- **Option A: Simple Scripted Pipeline (Linear Bash / Python Runner):**
  - Thực thi tuần tự từ đầu đến cuối dạng pipeline.
  - *Nhược điểm:* Không thể tạm dừng chờ duyệt; nếu đứt gãy giữa chừng thì phải chạy lại từ đầu; không có cơ chế bồi hoàn.
- **Option B: Heavy Distributed Workflow Engine (Temporal / Camunda):**
  - Cài đặt thêm cụm máy chủ Temporal/Camunda bên ngoài.
  - *Nhược điểm:* Quá cồng kềnh; phá vỡ mục tiêu đóng gói Single Binary độc lập cho người dùng cá nhân.
- **Option C (Được chọn): Hierarchical Finite State Machine (HFSM) kết hợp Embedded Saga Orchestrator trong Rust:**
  - Lập trình State Machine phân cấp trực tiếp bằng Rust Core: Tầng 1 (11 Macro Stages) -> Tầng 2 (Stage Execution FSM) -> Tầng 3 (Micro Task Saga).
  - Sử dụng Write-Ahead Saga Log lưu trong SQLite/PostgreSQL để quản lý các bước bồi hoàn (Compensating Actions).

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Hierarchical FSM kết hợp Embedded Saga Orchestrator**.
- Quản lý trạng thái 12 bước chuẩn xác định: `Draft -> Ready -> Running -> InReview -> Approved -> Completed` (kèm các trạng thái lỗi `Failed`, `Blocked`, `Suspended`).
- Mọi thao tác dài hạn đều được điều phối theo mẫu Saga Pattern: Nếu gặp sự cố ở bước N, hệ thống tự động gọi các hàm bồi hoàn từ bước N-1 ngược về bước 1 để dọn dẹp tài nguyên tạm (Staging files) và giải phóng Task Leases.
- Phân biệt tuyệt đối giữa trạng thái kỹ thuật `Completed` và trạng thái quản trị `Approved`.

## 5. Consequences & Trade-offs
- *Tích cực:* Hệ thống cực kỳ bền bỉ (Crash-proof), không phụ thuộc dịch vụ ngoài, kiểm soát trạng thái thời gian thực chính xác 100%.
- *Thách thức:* Đòi hỏi phải định nghĩa rõ ràng hàm bồi hoàn (Compensate function) cho từng loại Task.

## 6. Revisit Conditions

Mô hình FSM 11 giai đoạn và Saga Engine sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi quy trình làm việc đòi hỏi phân nhánh song song động phức tạp (Dynamic Directed Workflow DAG) với hàng trăm tác vụ bất đồng bộ phụ thuộc lẫn nhau mà mô hình FSM phân cấp (Hierarchical State Machine) không thể biểu diễn một cách mạch lạc mà không tạo ra sự bùng nổ số lượng trạng thái (State Explosion > 50 trạng thái phụ).
2. Khi hệ thống được triển khai trên cụm phân tán nhiều máy chủ (Distributed Multi-Node Cluster) yêu cầu cơ chế đồng thuận phân tán (Raft / Paxos) thay cho embedded local saga persistence.
