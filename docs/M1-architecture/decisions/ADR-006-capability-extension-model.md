# ADR-006 — Capability Extension Model: Dynamic Registry and Plugin Architecture

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-006 |
| Title | Capability Extension Model: Dynamic Registry and Plugin Architecture |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-06-CAP`, `MOD-17-TOL` |
| Related Requirements | M1-PROD-003 |
| Related Diagrams | DIA-002-capability-map.mmd |

---

## 1. Context & Problem Statement

PFS là một Universal Foundation Engine phục vụ đa dạng các lĩnh vực (Phần mềm, Kinh doanh, Nghiên cứu khoa học, Quy trình vận hành). Nếu danh mục năng lực (Capabilities) bị mã hóa cứng (Hard-coded) trong mã nguồn Rust Core, mỗi khi có một chuẩn công nghệ mới, một quy định pháp lý mới hoặc một domain chuyên biệt do người dùng tự định nghĩa (Custom Domain), đội ngũ phát triển sẽ phải sửa đổi và biên dịch lại toàn bộ hệ thống.

Cần một cơ chế cho phép mở rộng danh mục năng lực động (Dynamic Capability Extension) mà không làm tổn hại đến tính an toàn và tính xác định của Core.

## 2. Decision Drivers
- **Khả năng mở rộng mở (Open Extension):** Người dùng và các bên thứ ba có thể định nghĩa và nạp thêm Capabilities mới thông qua cấu hình.
- **Tính an toàn tuyệt đối:** Các Capabilities mở rộng không được phép làm sập hệ thống hoặc thực thi mã độc tùy ý.
- **Khả năng phân giải xung đột:** Tự động phát hiện các quan hệ phụ thuộc thiếu hụt hoặc các capabilities mâu thuẫn lẫn nhau.

## 3. Options Considered
- **Option A: Hard-coded Rust Enums:**
  - Định nghĩa toàn bộ Capabilities bằng Enum trong Rust Core.
  - *Nhược điểm:* Đóng băng hệ thống; không thể mở rộng domain mới nếu không phát hành phiên bản PFS Core mới.
- **Option B: Dynamic Shared Libraries (C ABI / `.so` / `.dll` plugins):**
  - Nạp mã máy nhị phân động vào tiến trình PFS.
  - *Nhược điểm:* Nguy cơ sập bộ nhớ (Segfault) và đe dọa an ninh nghiêm trọng nếu plugin chứa mã độc.
- **Option C (Được chọn): Dynamic Capability Registry kết hợp WebAssembly (WASM) Sandbox:**
  - Năng lực được mô tả trừu tượng bằng bản kê khai JSON/YAML chuẩn hóa (Declarative Manifest).
  - Logic xác thực mở rộng (nếu có) được đóng gói và thực thi an toàn trong môi trường WebAssembly (WASM) thông qua runtime `wasmtime`.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Dynamic Capability Registry kết hợp WebAssembly (WASM) Sandbox**.
- PFS Core cung cấp một `CapabilityCatalog` có thể nạp động từ thư mục cấu hình `.pfs/capabilities/` hoặc từ các gói mở rộng.
- Mỗi Capability bao gồm: Định danh ổn định, lược đồ xác thực đầu vào/đầu ra, danh mục artifacts bắt buộc và các quy tắc kiểm định chất lượng (Quality Criteria).
- Trạng thái áp dụng (Required, Optional, Conditional, Not Applicable) được giải quyết linh hoạt dựa trên Project Profile của từng dự án.

## 5. Consequences & Trade-offs
- *Tích cực:* Hệ thống mở rộng không giới hạn; hỗ trợ mọi domain mới của con người; an toàn bộ nhớ tuyệt đối.
- *Thách thức:* Cần duy trì tính tương thích phiên bản của Capability Schemas khi Core nâng cấp.

## 6. Revisit Conditions

Kiến trúc Capability Registry và WASM Extension sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi đồ thị phụ thuộc giữa các capabilities trong một domain phức tạp vượt quá 100 nút (nodes) dẫn đến thuật toán topological sort và dependency resolution của MOD-06-CAP vượt quá ngưỡng thời gian trễ 500ms trong quá trình khởi tạo dự án.
2. Khi môi trường WebAssembly (WASM) gặp rào cản tương thích nghiêm trọng trên một số nền tảng phần cứng mục tiêu hoặc không đáp ứng được yêu cầu gọi các thư viện tối ưu hóa phần cứng đặc thù (như CUDA/OpenCL cho các extension AI chuyên biệt).
