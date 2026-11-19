# ADR-010 — Event and Messaging Strategy: In-Memory and Broker-Agnostic Eventing

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-010 |
| Title | Event and Messaging Strategy: In-Memory and Broker-Agnostic Eventing |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-26-EVT`, `pfs-core`, `pfs-app` |
| Related Requirements | M1-SYS-003, M1-EXE-001 |
| Related Diagrams | DIA-005-dependency-graph.mmd |

---

## 1. Context & Problem Statement

Trong kiến trúc Modular Monolith, các modules cần giao tiếp và thông báo cho nhau khi có sự kiện nghiệp vụ xảy ra (ví dụ: khi một Requirement được thêm mới, Quality Engine cần tính toán lại ma trận phủ; khi một Stage được phê duyệt, Workflow Engine cần khởi động Stage kế tiếp).
- Nếu các module gọi trực tiếp hàm của nhau, hệ thống sẽ rơi vào cái bẫy phụ thuộc chặt (Tight Coupling) và dễ dẫn đến chu trình phụ thuộc.
- Nếu tích hợp ngay một Message Broker phân tán phức tạp (như Apache Kafka hoặc RabbitMQ), hệ thống sẽ không thể chạy độc lập trên máy trạm cá nhân của người dùng.

Cần một chiến lược truyền thông điệp (Event & Messaging Strategy) linh hoạt, hỗ trợ cả môi trường in-memory lẫn distributed.

## 2. Decision Drivers
- **Phụ thuộc lỏng (Loose Coupling):** Các module lắng nghe sự kiện mà không cần biết chủ thể phát sinh sự kiện là ai.
- **Không phụ thuộc Broker ngoài ở chế độ Local:** Chạy hoàn toàn trên bộ nhớ với kênh truyền `tokio::sync::broadcast` hoặc `mpsc`.
- **Đảm bảo tính nhất quán (Transactional Outbox Pattern):** Ngăn ngừa việc dữ liệu đã lưu vào database nhưng sự kiện bị mất do sập máy tính.

## 3. Options Considered
- **Option A: External Message Broker Mandatory (Kafka / NATS):**
  - Bắt buộc cài đặt Kafka/NATS cho mọi trường hợp.
  - *Nhược điểm:* Phá vỡ trải nghiệm Zero-Config Local CLI; tiêu tốn hàng trăm MB RAM vô ích trên máy trạm cá nhân.
- **Option B: Synchronous In-Memory Observer Pattern:**
  - Gọi callback đồng bộ trực tiếp trong cùng luồng.
  - *Nhược điểm:* Một listener bị lỗi hoặc chạy chậm sẽ làm nghẽn toàn bộ giao dịch chính; không có khả năng thử lại (Retry).
- **Option C (Được chọn): In-Memory Event Bus kết hợp Transactional Outbox Pattern:**
  - Sử dụng kênh truyền thông điệp bất đồng bộ trong tiến trình của Tokio (`EventBusPort`).
  - Đối với các sự kiện quan trọng cần bảo đảm không mất mát (Domain & Audit Events), hệ thống ghi vào bảng `outbox_events` trong cùng một giao dịch cơ sở dữ liệu với nghiệp vụ chính (Transactional Outbox). Tiến trình nền (Worker) sẽ đọc và phát lại an toàn.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: In-Memory Event Bus kết hợp Transactional Outbox Pattern**.
- Cung cấp tính năng gửi/nhận sự kiện bất đồng bộ cực nhanh trên máy trạm mà không cần cài thêm bất kỳ phần mềm nào.
- Đảm bảo tính nhất quán tối cao: Dữ liệu nghiệp vụ và sự kiện luôn được ghi thành công cùng nhau hoặc cùng bị hủy bỏ (Rollback).
- Khi triển khai trên môi trường đám mây doanh nghiệp (Enterprise Mode), Adapter Outbox Worker có thể dễ dàng chuyển tiếp các sự kiện từ bảng `outbox_events` sang Kafka hoặc AWS EventBridge mà không cần sửa mã nguồn Core.

## 5. Consequences & Trade-offs
- *Tích cực:* Hệ thống hoàn toàn phi tập trung ở local, mở rộng không giới hạn ở cloud; bảo đảm At-Least-Once Delivery.
- *Thách thức:* Người nhận sự kiện (Event Consumers) bắt buộc phải thiết kế có tính Idempotent (chống xử lý trùng lặp).

## 6. Revisit Conditions

Chiến lược sự kiện Broker-Agnostic kết hợp Transactional Outbox sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi lưu lượng phát sinh sự kiện nội bộ vượt quá 50.000 sự kiện/giây khiến bảng outbox_events trong RDBMS trở thành điểm nghẽn ghi (write bottleneck) và độ trễ polling của outbox relay vượt quá SLA 100ms.
2. Khi xuất hiện yêu cầu nghiệp vụ bắt buộc bảo đảm thứ tự tuần tự tuyệt đối toàn cầu (Global Strict Total Ordering) xuyên suốt hàng triệu sự kiện phân tán mà cơ chế sequence number cục bộ theo từng aggregate không đáp ứng được.
