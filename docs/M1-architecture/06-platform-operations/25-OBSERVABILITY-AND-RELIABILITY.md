# PFS-M1-DOC-025 — Observability, Telemetry and System Reliability

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-025 |
| Document Title | Observability, Telemetry and System Reliability Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & SRE Lead |
| Classification | Internal |
| Reference Architecture | OpenTelemetry (OTel), Site Reliability Engineering (SRE), Chaos Engineering |
| Related Decisions | ADR-020, ADR-012 |
| Invariant Reference | INV-10, INV-12 |

---

## 1. Observability Architectural Strategy

Trong một hệ thống lai kết hợp giữa logic xác định và trí tuệ nhân tạo có tính xác suất, tính năng quan sát (Observability) không đơn thuần là in ra các dòng log văn bản. Khả năng giám sát sâu là điều kiện sống còn để phát hiện sai lệch mô hình, kiểm soát chi phí token, điều tra nguyên nhân gốc rễ (Root Cause Analysis) và phục vụ kiểm toán thanh tra an ninh.

PFS tích hợp chuẩn công nghiệp **OpenTelemetry (OTel)** xuyên suốt toàn bộ các tầng kiến trúc, dựa trên 3 trụ cột (Pillars of Observability):
1. **Distributed Tracing (Dấu vết Phân tán):** Mỗi Command hoặc User Interaction được gán một `Correlation ID` bất biến. Dấu vết này được lan truyền (propagated) qua toàn bộ các tiến trình nội bộ, các tác vụ của Agent và các cuộc gọi API ra LLM bên ngoài.
2. **Structured JSON Metrics (Chỉ số Định lượng):** Đo lường thời gian thực về độ trễ xử lý (Latency P50, P95, P99), số lượng token tiêu thụ, chi phí tài chính tích lũy và tỷ lệ lỗi của từng model.
3. **Append-Only Cryptographic Audit Logging (Nhật ký Kiểm toán Mật mã):** Toàn bộ các sự kiện thay đổi trạng thái, quyết định quản trị và phân quyền đều được ghi nhận vào nhật ký kiểm toán bất biến có niêm phong chữ ký số Ed25519.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       OpenTelemetry Telemetry Pipeline                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ PFS Engine Instrumented with tracing crate ]                            │
│        │                                                                    │
│        ├── Traces: Span context with Correlation ID, Agent ID, Task ID      │
│        ├── Metrics: Counter (Tokens, Requests), Histogram (Latencies)       │
│        └── Logs: Structured JSON (Level, Target, Fields, Stacktrace)        │
│        │                                                                    │
│        ▼ exported via OpenTelemetry Protocol (OTLP / gRPC)                  │
│  [ OpenTelemetry Collector / Prometheus / Grafana Loki / Jaeger / Datadog ] │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Reliability Engineering & Fault Tolerance Patterns

Để duy trì tính ổn định liên tục của hệ thống ngay cả khi các dịch vụ đám mây bên ngoài gặp sự cố, PFS Core triển khai 5 mẫu thiết kế chống chịu lỗi (Fault-Tolerance Patterns):

### 2.1. Circuit Breaker Pattern (Bộ ngắt mạch tự động)
- **Mục đích:** Bảo vệ hệ thống khỏi việc tiếp tục gửi yêu cầu vào một nhà cung cấp AI đang bị sập (ví dụ: OpenAI trả về lỗi 503 liên tục), tránh lãng phí thời gian chờ đợi và nghẽn tài nguyên.
- **Vận hành:**
  - `Closed (Bình thường):` Toàn bộ yêu cầu được chuyển tiếp bình thường. Nếu tỷ lệ lỗi vượt quá 50% trong 10 yêu cầu gần nhất, chuyển sang `Open`.
  - `Open (Ngắt mạch):` Chặn đứng toàn bộ yêu cầu gửi đến nhà cung cấp này trong 60 giây; tự động kích hoạt **Secondary Fallback Adapter** (ví dụ: chuyển sang Anthropic hoặc local vLLM).
  - `Half-Open (Thử nghiệm):` Sau 60 giây, cho phép 2 yêu cầu thử nghiệm đi qua. Nếu thành công, đóng mạch (`Closed`); nếu thất bại, tiếp tục mở mạch (`Open`) thêm 120 giây.

### 2.2. Rate Limiting & Token Bucket Algorithm
- Áp dụng thuật toán Token Bucket tại lớp Gateway để kiểm soát tốc độ gửi yêu cầu lên các dịch vụ AI bên ngoài, ngăn ngừa việc vi phạm giới hạn tần suất (HTTP 429 Rate Limit Exceeded) và điều hòa lưu lượng trong giờ cao điểm.

### 2.3. Exponential Backoff with Jitter
- Khi gặp lỗi mạng tạm thời hoặc mã lỗi 429, hệ thống tự động thử lại (Retry) với thời gian chờ tăng theo cấp số nhân kết hợp độ trễ ngẫu nhiên (Full Jitter) để tránh hiện tượng bão yêu cầu (Thundering Herd Problem):
  $$T_{\text{wait}} = \text{random}(0, \min(T_{\text{max}}, T_{\text{base}} \times 2^{\text{attempt}}))$$

### 2.4. Crash Recovery & Transaction Journaling
- Mọi thao tác ghi tệp tin của Generator đều được ghi trước vào Transaction Journal (`.pfs/journal.log`). Khi tiến trình khởi động lại sau sự cố mất điện hoặc sập máy tính, Recovery Engine đọc nhật ký và tự động dọn dẹp các tệp tin tạm mồ côi trong Staging Directory.

---

## 3. Comprehensive Version Compatibility Matrix

Theo bất biến kiến trúc **INV-10**, PFS phân định rạch ròi 9 miền phiên bản (Version Domains) độc lập nhằm bảo đảm tính tương thích lâu dài và không làm gián đoạn các dự án đã tồn tại:

| Miền Phiên bản | Chuẩn định dạng | Quy tắc Tương thích & Quản lý Thay đổi |
|---|---|---|
| **1. PFS Core Binary** | SemVer 2.0.0 (vd: `1.0.0`) | Tuân thủ SemVer nghiêm ngặt. Thay đổi Major yêu cầu chạy script migration dữ liệu tự động. |
| **2. Universal Domain Model** | Schema URI (vd: `dom.v1`) | Tương thích ngược; thuộc tính mới bổ sung bắt buộc phải là Optional hoặc có giá trị mặc định. |
| **3. API Contracts** | URL Path (`/api/v1`) | Duy trì API v1 tối thiểu 12 tháng sau khi công bố API v2. Có cảnh báo `Deprecation` header. |
| **4. Artifact Schemas** | JSON Schema Draft 2020-12 | Cung cấp JSON Schema migration transforms để nâng cấp metadata của các artifacts cũ. |
| **5. Generator Templates** | SemVer (vd: `tpl-rust-v1.2`) | Khóa phiên bản (Pinning) trong Project Profile; dự án cũ tiếp tục dùng template cũ trừ khi chủ động nâng cấp. |
| **6. Agent Profiles** | SemVer (vd: `agt-c4-v2.0`) | Thay đổi system prompt hoặc tool schema lớn làm tăng Major version của Agent Profile. |
| **7. Governance Policies** | Hash Digest / SemVer | Mọi quyết định phê duyệt đều lưu mã băm của Policy có hiệu lực tại thời điểm ký; không áp dụng hồi tố. |
| **8. Provider Adapters** | SemVer (vd: `adp-openai-v1`) | Cập nhật adapter khi nhà cung cấp nâng cấp API; không làm thay đổi Universal Provider Trait của Core. |
| **9. Foundation Package** | SemVer (vd: `pkg-v1.0.0`) | Niêm phong bằng chữ ký số bất biến; một khi đã Baseline thì không bao giờ bị ghi đè. |
