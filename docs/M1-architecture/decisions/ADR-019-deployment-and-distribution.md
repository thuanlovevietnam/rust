# ADR-019 — Deployment and Distribution: Zero-Downtime Migration & Portable Packaging

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-019 |
| Title | Deployment and Distribution: Zero-Downtime Migration and Portable Packaging |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & DevOps Lead |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `pfs-cli`, `pfs-server`, `MOD-25-VER` |
| Related Requirements | M1-OPS-001, M1-OPS-002 |
| Related Diagrams | DIA-014-deployment-topology.mmd |
| Invariant Reference | INV-10 |

---

## 1. Context & Problem Statement

PFS cần được phân phối tới nhiều nhóm người dùng trên đa dạng các nền tảng hệ điều hành (Linux x86_64, Linux aarch64, macOS Apple Silicon, Windows x64).
- Người dùng không muốn phải cài đặt trình thông dịch Python, Node.js hay các thư viện liên kết động phức tạp (`glibc` version mismatch).
- Trong môi trường doanh nghiệp có nhiều người dùng đồng thời, việc cập nhật phiên bản PFS Core hoặc nâng cấp lược đồ cơ sở dữ liệu không được phép làm gián đoạn các workflow đang chạy hoặc gây thời gian chết của dịch vụ (Downtime).

Cần một chiến lược đóng gói phần mềm di động (Portable Packaging) và quy trình di chuyển cơ sở dữ liệu không thời gian chết (Zero-Downtime Migration).

## 2. Decision Drivers
- **Đóng gói nhị phân độc lập (Static Binaries):** Nhị phân biên dịch tĩnh hoàn toàn không phụ thuộc thư viện runtime bên ngoài (vd: biên dịch với target `x86_64-unknown-linux-musl`).
- **Nâng cấp cơ sở dữ liệu an toàn:** Hỗ trợ quy trình Expand-and-Contract bảo đảm tính tương thích xuôi và ngược giữa các phiên bản phần mềm.
- **Dễ dàng cài đặt và cập nhật:** Cung cấp các kênh phân phối tiêu chuẩn (Homebrew, Cargo install, Shell script, GitHub Releases, Docker container).

## 3. Options Considered
- **Option A: Dynamic Linking with System Dependencies:**
  - Biên dịch phụ thuộc vào `glibc` và các thư viện động của hệ điều hành.
  - *Nhược điểm:* Dễ gặp lỗi "GLIBC_X.XX not found" khi chạy trên các bản phân phối Linux cũ hoặc máy trạm người dùng.
- **Option B (Được chọn): Fully Static Native Binaries kết hợp Expand-and-Contract Migrations:**
  - Biên dịch tĩnh hoàn toàn (Static Linking) sử dụng MUSL trên Linux và MSVC runtime nhúng trên Windows.
  - Quản lý database migration thông qua `sqlx-cli` với chiến lược 2 bước:
    1. *Expand:* Bổ sung bảng hoặc cột mới nhưng vẫn duy trì cấu trúc cũ; phiên bản phần mềm cũ và mới cùng hoạt động bình thường.
    2. *Contract:* Chuyển đổi dữ liệu và chỉ xóa bỏ cột cũ sau khi toàn bộ cụm máy chủ đã được nâng cấp lên phiên bản mới.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Fully Static Native Binaries kết hợp Expand-and-Contract Migrations**.
- Người dùng chỉ cần tải duy nhất 1 tệp nhị phân (`pfs`), đặt vào biến môi trường `PATH` là có thể sử dụng ngay lập tức mà không cần bất kỳ cài đặt phụ thuộc nào.
- Khi khởi động phiên bản mới trên máy chủ, PFS tự động kiểm tra và thực thi các bước migration an toàn. Nếu phát hiện xung đột hoặc lỗi kịch bản, hệ thống tự động rollback và từ chối khởi động để bảo vệ an toàn dữ liệu.

## 5. Consequences & Trade-offs
- *Tích cực:* Phân phối phần mềm cực kỳ mượt mà; tương thích 100% với môi trường container tối giản (Scratch/Alpine); nâng cấp doanh nghiệp không gián đoạn.
- *Thách thức:* Kích thước tệp nhị phân tĩnh lớn hơn một chút (~25MB) so với tệp liên kết động.

## 6. Revisit Conditions

Chiến lược phân phối nhị phân tĩnh và triển khai sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi kích thước tệp nhị phân tĩnh vượt quá 100MB do tích hợp thêm các thư viện máy học hoặc công cụ phụ trợ, gây khó khăn cho việc phân phối trên các mạng băng thông thấp hoặc thiết bị nhúng IoT, đòi hỏi phải tách các plugin phụ thuộc thành các shared dynamic libraries (.so/.dll) hoặc WASM modules tải theo nhu cầu.
2. Khi nền tảng triển khai mục tiêu yêu cầu ký số bằng chứng nhận phần cứng bắt buộc (Hardware-Signed Driver/Binary) theo chính sách kiểm soát ứng dụng nghiêm ngặt (như Windows AppLocker / WDAC) mà quy trình CI/CD phân phối hiện tại chưa đáp ứng được.
