# ADR-020 — Observability and Reliability: OpenTelemetry Tracing & Circuit Breaker

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-020 |
| Title | Observability and Reliability: OpenTelemetry Tracing and Circuit Breaker |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & SRE Lead |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-27-AUD`, `MOD-16-GWY`, `pfs-infra` |
| Related Requirements | M1-OPS-002, M1-EXE-002 |
| Related Diagrams | DIA-016-failure-recovery-flow.mmd |
| Invariant Reference | INV-12 |

---

## 1. Context & Problem Statement

Trong một hệ thống lai phức tạp nơi các quyết định kiến trúc được suy luận bởi AI và điều phối bởi động cơ xác định, việc phát hiện lỗi, điều tra sự cố và kiểm soát chất lượng đòi hỏi khả năng quan sát chuyên sâu:
- Nếu chỉ dùng các câu lệnh in log văn bản thô (printf-style logging), khi có sự cố xảy ra giữa hàng trăm luồng của các Agents, kỹ sư sẽ hoàn toàn mất phương hướng và không thể tái hiện lại ngữ cảnh.
- Khi một dịch vụ AI bên ngoài bị chập chờn, việc tiếp tục dội hàng ngàn yêu cầu vào sẽ gây tắc nghẽn toàn bộ hàng đợi của hệ thống và làm cạn kiệt tài nguyên kết nối mạng.

Cần một kiến trúc viễn trắc phân tán chuẩn công nghiệp (OpenTelemetry) kết hợp mẫu thiết kế ngắt mạch tự động (Circuit Breaker).

## 2. Decision Drivers
- **Chuẩn hóa công nghiệp mở (OpenTelemetry Native):** Khả năng xuất dữ liệu viễn trắc (Traces, Metrics, Logs) ra bất kỳ nền tảng giám sát nào (Prometheus, Jaeger, Grafana Loki, Datadog) mà không bị phụ thuộc công nghệ độc quyền.
- **Dấu vết liên kết bất biến (End-to-End Correlation ID):** Mọi tác vụ đều có thể truy vết xuyên suốt từ cú click chuột của người dùng đến từng token của LLM.
- **Chống chịu lỗi chủ động (Resilience by Design):** Tự động phát hiện và ngắt mạch khi dịch vụ ngoài bị lỗi, bảo vệ tài nguyên hệ thống.

## 3. Options Considered
- **Option A: Proprietary Custom Log Format:**
  - Tự định nghĩa định dạng log riêng ghi ra tệp văn bản.
  - *Nhược điểm:* Khó tích hợp với các công cụ phân tích tập trung của doanh nghiệp; không hỗ trợ distributed context propagation.
- **Option B (Được chọn): Tích hợp OpenTelemetry SDK với Rust Crate `tracing` & Circuit Breaker Pattern:**
  - Sử dụng hệ sinh thái `tracing` và `opentelemetry` chuẩn hóa của Rust.
  - Mọi tầng ứng dụng đều được gắn các Spans viễn trắc mang đầy đủ ngữ cảnh (`project_id`, `actor_id`, `correlation_id`).
  - Lớp AI Gateway và Tool Gateway được bảo vệ bằng máy trạng thái ngắt mạch (Circuit Breaker: Closed -> Open -> Half-Open).

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: OpenTelemetry SDK kết hợp Circuit Breaker Pattern**.
- Khi một yêu cầu đi vào hệ thống, một `Correlation ID` duy nhất được khởi tạo và lan truyền xuyên suốt toàn bộ các luồng Tokio bất đồng bộ.
- Dữ liệu viễn trắc được xuất ra định dạng JSON có cấu trúc trên máy trạm hoặc gửi trực tiếp qua giao thức OTLP/gRPC tới OpenTelemetry Collector trên môi trường máy chủ.
- Circuit Breaker tự động kích hoạt khi tỷ lệ lỗi của một AI Provider vượt quá 50% trong 10 yêu cầu gần nhất, chuyển hướng tức thì sang nhà cung cấp dự phòng mà không làm gián đoạn trải nghiệm người dùng.

## 5. Consequences & Trade-offs
- *Tích cực:* Khả năng giám sát và gỡ lỗi đẳng cấp doanh nghiệp; bảo vệ hệ thống trước sự cố đám mây; minh bạch 100% về chi phí token.
- *Thách thức:* Cần phân bổ tài nguyên bộ nhớ đệm (buffer) cho bộ thu thập viễn trắc để tránh làm ảnh hưởng đến hiệu năng xử lý chính.

## 6. Revisit Conditions

Kiến trúc Quan sát và Độ tin cậy (Observability & Reliability) sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi chi phí tài nguyên (CPU/RAM/Network overhead) phục vụ việc thu thập và xuất viễn trắc OpenTelemetry vượt quá 5% tổng tài nguyên tiêu thụ của tiến trình Core trên máy trạm cá nhân, đòi hỏi phải kích hoạt cơ chế Adaptive Sampling hoặc tắt bớt span traces ở môi trường Local CLI.
2. Khi cơ chế Circuit Breaker cục bộ trong bộ nhớ không đồng bộ được trạng thái lỗi giữa nhiều tiến trình Daemon chạy song song trong cụm Kubernetes doanh nghiệp, đòi hỏi phải chuyển sang sử dụng Circuit Breaker phân tán dựa trên Redis hoặc Envoy Service Mesh.
