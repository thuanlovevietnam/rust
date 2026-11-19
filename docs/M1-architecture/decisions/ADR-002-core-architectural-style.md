# ADR-002 — Core Architectural Style: Clean Hexagonal Architecture (Ports & Adapters)

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-002 |
| Title | Core Architectural Style: Clean Hexagonal Architecture (Ports & Adapters) |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `pfs-core`, `pfs-app`, `pfs-infra` |
| Related Requirements | M1-SYS-002, M1-PROD-004 |
| Related Diagrams | DIA-004-c4-component.mmd, DIA-005-dependency-graph.mmd |

---

## 1. Context & Problem Statement

PFS là một Universal Foundation Engine cần hoạt động ổn định qua nhiều năm, trong khi hệ sinh thái công nghệ bên ngoài (các AI models, cơ sở dữ liệu, giao diện người dùng) biến động liên tục. Nếu mã nguồn miền nghiệp vụ cốt lõi (Domain Core) phụ thuộc trực tiếp vào SDK của OpenAI, cú pháp truy vấn của PostgreSQL, hay giao diện của một framework web cụ thể, hệ thống sẽ trở nên cực kỳ mong manh và khó kiểm thử tự động.

Hệ thống đòi hỏi một phong cách kiến trúc có khả năng cô lập tuyệt đối lõi nghiệp vụ khỏi mọi biến động hạ tầng ngoại vi.

## 2. Decision Drivers
- **Độc lập công nghệ:** Lõi nghiệp vụ (Domain Entities, Aggregates, Policy Rules) không phụ thuộc vào bất kỳ thư viện I/O hay SDK bên ngoài nào.
- **Khả năng kiểm thử (Testability):** Có thể viết unit tests cho 100% quy tắc nghiệp vụ mà không cần mở kết nối cơ sở dữ liệu hoặc gọi mạng internet.
- **Dễ dàng thay thế thành phần:** Khả năng thay thế SQLite bằng PostgreSQL hoặc đổi OpenAI sang Anthropic mà không phải sửa một dòng mã nào trong Core.

## 3. Options Considered
- **Option A: Traditional 3-Tier Layered Architecture (UI -> Business Logic -> Data Access):**
  - Tầng Business Logic phụ thuộc trực tiếp vào Tầng Data Access; Data Access phụ thuộc vào Database Driver.
  - *Nhược điểm:* Vi phạm nguyên lý Đảo ngược Phụ thuộc (DIP); khó mock dữ liệu khi kiểm thử độc lập.
- **Option B (Được chọn): Clean Hexagonal Architecture (Ports & Adapters / Onion Architecture):**
  - Tầng Domain Core nằm ở trung tâm tuyệt đối, định nghĩa các "Ports" dưới dạng Rust Traits (ví dụ: `StoragePort`, `AIProviderPort`, `ToolExecutionPort`).
  - Tầng Infrastructure nằm ở vòng ngoài cùng, hiện thực hóa các "Adapters" cắm vào các Ports.
  - Mọi luồng phụ thuộc đều hướng vào tâm (Inward Dependency Direction).

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Clean Hexagonal Architecture (Ports & Adapters)**.
- Toàn bộ Crate `pfs-core` là Pure Rust (Zero External I/O Dependencies), chỉ chứa các mô hình dữ liệu, bất biến và quy tắc nghiệp vụ thuần túy.
- Các tương tác với thế giới bên ngoài (Disk, Network, DB, AI) được biểu diễn bằng các Trait Interfaces trừu tượng trong Core/App và được cài đặt cụ thể trong Crate `pfs-infra`.

## 5. Consequences & Trade-offs
- *Tích cực:* Đạt độ ổn định tối đa ($I = 0.0$ cho Core); kiểm thử tự động cực nhanh và tin cậy; thay thế adapter dễ dàng trong 1 nốt nhạc.
- *Thách thức:* Cần viết thêm các lớp ánh xạ (Data Transfer Objects - DTOs) giữa Domain Structs và Database Rows, đòi hỏi nhiều mã nguồn boilerplate hơn ban đầu.

## 6. Revisit Conditions

Kiến trúc Clean Hexagonal (Ports & Adapters) sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Chi phí hiệu năng chuyển đổi bộ nhớ giữa Domain Entities và Infrastructure DTOs trên đường truyền dữ liệu lớn (ví dụ: streaming I/O hàng gigabyte dữ liệu nhị phân của CAS blob) vượt quá 20% tổng thời gian xử lý của hệ thống, đòi hỏi phải áp dụng zero-copy memory mapping trực tiếp cho một số adapter chuyên biệt.
2. Khi một adapter ngoại vi đòi hỏi cơ chế concurrency đặc thù không thể trừu tượng hóa bằng standard Rust async traits mà không làm suy giảm hiệu năng xử lý của runtime.
