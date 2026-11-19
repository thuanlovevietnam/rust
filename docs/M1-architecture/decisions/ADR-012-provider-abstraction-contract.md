# ADR-012 — Provider Abstraction Contract: Agnostic LLM Gateway with Constrained Decoding

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-012 |
| Title | Provider Abstraction Contract: Agnostic LLM Gateway with Constrained Decoding and Boundary Protection |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-16-GWY`, `pfs-infra` |
| Related Requirements | M1-EXE-002, M1-PROD-004, M0-AGT-006, M0-SEC-004 |
| Related Diagrams | DIA-004-c4-component.mmd, DIA-013-security-trust-boundary.mmd |
| Invariant Reference | INV-05, INV-11 |
| Audit Remediation | Resolved finding FND-M1-01 (Boundary Enforcement at Provider Gateway) and FND-M1-08 (Concrete Revisit Conditions) |

---

## 1. Context & Problem Statement

Thị trường các mô hình ngôn ngữ lớn (LLMs) biến động rất nhanh: OpenAI, Anthropic, Google, DeepSeek và các mô hình mã nguồn mở nội bộ (Meta Llama qua vLLM/Ollama) liên tục cạnh tranh về giá cả, độ trễ và năng lực suy luận.
- Nếu hệ thống gắn chặt mã nguồn vào định dạng API của OpenAI, khi OpenAI sập mạng hoặc thay đổi chính sách giá, PFS sẽ bị tê liệt hoàn toàn (Vendor Lock-in).
- Các mô hình AI có xu hướng trả về văn bản tự do kèm lời dẫn dắt (chatter), gây lỗi phân tích cú pháp nghiêm trọng cho các hệ thống phần mềm xác định.
- Nguy cơ rò rỉ dữ liệu nhạy cảm: Nếu không có chốt chặn kiểm tra metadata phân loại tại Gateway, dữ liệu cấp Tier 4 (Restricted) hoặc dữ liệu chưa được phân loại (Unclassified) có thể bị gửi nhầm sang các nhà cung cấp đám mây bên ngoài.

Hệ thống cần một hợp đồng giao tiếp trừu tượng hóa tuyệt đối, cơ chế ép buộc định dạng đầu ra (Constrained Structured Outputs) và chốt chặn an ninh bảo vệ dữ liệu Restricted tại ranh giới Provider.

---

## 2. Decision Drivers

- **Độc lập nhà cung cấp 100% (Vendor Neutrality):** Khả năng chuyển đổi giữa OpenAI, Claude, Gemini hoặc vLLM cục bộ chỉ bằng cấu hình.
- **Bảo vệ dữ liệu Restricted (INV-11 & FND-M1-01):** Tuyệt đối cấm gửi dữ liệu Restricted tới External Cloud AI Providers; mặc định từ chối (Deny-by-default) nếu thiếu metadata phân loại.
- **Tính tin cậy về cấu trúc dữ liệu:** Bảo đảm 100% dữ liệu trả về từ mô hình tuân thủ đúng JSON Schema mong muốn.
- **Khả năng chịu lỗi và Quản trị chi phí:** Tự động chuyển đổi nhà cung cấp dự phòng (Failover) và kiểm soát ngân sách token thời gian thực.

---

## 3. Options Considered

- **Option A: Sử dụng Trực tiếp SDK Chính hãng (Direct Vendor SDKs in Core):**
  - Nhập trực tiếp crate `async-openai` vào các phân hệ nghiệp vụ.
  - *Nhược điểm:* Vi phạm bất biến INV-05; làm ô nhiễm Domain Core; không thể chuyển sang Anthropic hay mô hình local.
- **Option B (Được chọn): Universal AI Provider Gateway với Constrained Decoding và Policy Gatekeeper:**
  - Định nghĩa Trait `AIProviderPort` trong tầng Application/Core.
  - Hiện thực hóa lớp Gateway trong Crate `pfs-infra` với các Adapter riêng cho từng nhà cung cấp.
  - Tích hợp Policy Gatekeeper kiểm tra `ClassificationTier` trước khi gửi HTTP request:
    - Nếu `tier == Restricted` và `destination == ExternalCloud` -> Chặn đứng ngay lập tức với lỗi `DENY_RESTRICTED_EXTERNAL_DISPATCH`.
    - Chỉ cho phép gửi dữ liệu Restricted sang máy chủ nội bộ (AirGappedLocal) khi có ngoại lệ được ký số bởi Project Owner (L5 Authority).
  - Tận dụng tính năng Structured Outputs chuẩn (`response_format: json_schema`) kết hợp bộ xác thực JSON Schema thứ cấp trên Rust Core.

---

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Universal AI Provider Gateway với Constrained Decoding và Policy Gatekeeper**.
- Lõi Core chỉ gửi đi `UniversalLLMRequest` và nhận lại `UniversalLLMResponse`. Toàn bộ sự khác biệt về cú pháp API, định dạng tool calling hay phân tích token đều được xử lý gọn gàng bên trong Gateway.
- Tích hợp cơ chế **3-Tier Failover Policy**: Nếu Primary Model (vd: Claude 3.7 Sonnet) gặp lỗi 503 hoặc timeout, Gateway tự động chuyển sang Secondary Model (vd: GPT-4o) trong vòng < 2 giây. Nếu mất toàn bộ kết nối Internet, tự động kích hoạt Local Fallback Adapter kết nối tới máy chủ vLLM nội bộ.
- Bắt buộc kích hoạt cờ Do-Not-Train và Zero Data Retention để bảo đảm bí mật dữ liệu doanh nghiệp (INV-11).

---

## 5. Consequences & Trade-offs

### 5.1. Tích cực (Positive Consequences)
- Loại bỏ hoàn toàn Vendor Lock-in; hệ thống có thể hoạt động hoàn toàn offline (Air-gapped); dữ liệu đầu ra có tính xác định cao.
- Bảo đảm an toàn tuyệt đối cho dữ liệu doanh nghiệp; ngăn chặn nguy cơ rò rỉ dữ liệu mật sang bên thứ ba.

### 5.2. Thách thức (Negative Consequences)
- Cần duy trì mã nguồn Adapter cho từng nhà cung cấp khi họ cập nhật phiên bản API mới.
- Độ trễ bổ sung nhỏ (< 5ms) do việc kiểm tra chính sách phân loại dữ liệu tại Gateway trước mỗi cuộc gọi mạng.

---

## 6. Security & Operational Implications

- **Chốt chặn an ninh Gateway:** Mọi request đều được kiểm tra `ClassificationTier`. Dữ liệu thiếu metadata bị từ chối với mã lỗi `DENY_UNCLASSIFIED_DATA`.
- **Bảo mật kênh truyền:** 100% kết nối ra ngoài sử dụng TLS 1.3 với cipher suites an toàn; không cho phép bypass chứng chỉ SSL.

---

## 7. Dependencies & Compatibility

- **Phụ thuộc:** `MOD-18-CTX` (Context Management), `MOD-11-POL` (Policy Engine).
- **Hạ tầng mạng:** Cần kết nối Internet ra các endpoint OpenAI/Anthropic ở chế độ Cloud, hoặc mạng LAN nội bộ kết nối tới cụm vLLM/Ollama ở chế độ Air-gapped.

---

## 8. Status & Owner Governance

- **Trạng thái:** `Proposed — Ready for Owner Review`.
- **Thẩm quyền phê duyệt:** Project Owner (Nguyễn Thế Thuận) — Bảo lưu cho quyết định OD-M1-01.
- **Bằng chứng kiến trúc:** `E2 — Specified` (Đặc tả chi tiết tại `docs/M1-architecture/04-execution-architecture/17-AI-PROVIDER-AND-TOOL-ADAPTERS.md` và `docs/M1-architecture/contracts/provider-contracts.json`).

---

## 9. Revisit Conditions

Hợp đồng trừu tượng hóa AI Provider và Gateway sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. **Thay đổi giao thức suy luận:** Khi các nhà cung cấp AI hàng đầu chuyển đổi hoàn toàn sang một giao thức suy luận nhị phân streaming đa phương thức thế hệ mới (như gRPC/Protobuf hoặc WebSocket binary streaming độc quyền) mà kiến trúc REST HTTP/JSON hiện tại không thể hỗ trợ với độ trễ thấp (< 50ms time-to-first-token).
2. **Chính sách dữ liệu của các hãng AI:** Khi chính sách quyền riêng tư của các nhà cung cấp đám mây bên ngoài không còn cam kết Zero Data Retention (ZDR) hoặc hủy bỏ thỏa thuận Enterprise Do-Not-Train, buộc toàn bộ hệ sinh thái PFS phải chuyển dịch bắt buộc 100% sang các mô hình On-Premise Air-gapped.
3. **Chi phí hoặc giới hạn tốc độ (Rate Limits):** Khi chi phí API bên thứ ba vượt quá ngân sách phân bổ cho dự án hoặc tình trạng lỗi 429 (Rate Limit Exceeded) xảy ra trên 15% tổng số yêu cầu trong 3 ngày làm việc liên tiếp.
