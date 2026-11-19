# ADR-008 — Artifact Storage and Versioning: Content-Addressed Storage & Merkle DAG

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-008 |
| Title | Artifact Storage and Versioning: Content-Addressed Storage & Merkle DAG |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-20-ART`, `MOD-22-GEN`, `MOD-24-EVI` |
| Related Requirements | M1-DOM-004, M1-DOM-001 |
| Related Diagrams | DIA-011-artifact-provenance-graph.mmd |

---

## 1. Context & Problem Statement

Trong quá trình xây dựng Foundation, hệ thống sản sinh ra hàng ngàn phiên bản tài liệu, mã nguồn và báo cáo kiểm định. Các giải pháp lưu trữ tệp tin truyền thống dựa trên đường dẫn tệp (File Path) gặp phải các vấn đề nghiêm trọng:
- Khi đổi tên hoặc di chuyển tệp tin, toàn bộ lịch sử truy vết và liên kết phụ thuộc bị đứt gãy.
- Không thể phát hiện được nếu một tệp tin bị chỉnh sửa lén lút ngoài tầm kiểm soát của hệ thống.
- Lãng phí dung lượng lưu trữ do sao chép nhiều tệp tin có nội dung giống nhau qua các phiên bản.

Cần một kiến trúc lưu trữ và phiên bản hóa bảo đảm tính toàn vẹn toán học và truy vết phả hệ nguồn gốc (Provenance).

## 2. Decision Drivers
- **Tính toàn vẹn mật mã (Cryptographic Integrity):** Bất kỳ sự thay đổi dù chỉ 1 ký tự trong nội dung tệp tin đều làm thay đổi định danh của nó.
- **Truy vết phả hệ (Provenance DAG):** Có khả năng biểu diễn quan hệ "Tạo tác con được sinh ra từ Tạo tác cha nào".
- **Chống trùng lặp dữ liệu (Deduplication):** Tối ưu hóa dung lượng ổ đĩa.

## 3. Options Considered
- **Option A: Traditional File System Storage with Version Suffixes (`file_v1.md`, `file_v2.md`):**
  - Lưu tệp trực tiếp với hậu tố phiên bản.
  - *Nhược điểm:* Dễ vỡ liên kết, không có cơ chế kiểm tra tính toàn vẹn tự động, rủi ro ghi đè tệp tin ngoài ý muốn.
- **Option B: Git-only Subprocess Wrapper:**
  - Dùng lệnh Git ngầm bên dưới để quản lý phiên bản.
  - *Nhược điểm:* Phụ thuộc nặng nề vào nhị phân Git cài trên máy người dùng; khó tích hợp sâu vào cơ sở dữ liệu quan hệ và môi trường Web/Cloud.
- **Option C (Được chọn): Content-Addressed Storage (CAS) kết hợp Merkle DAG:**
  - Áp dụng nguyên lý của Git và IPFS: Nội dung tệp tin (Blob) được lưu trữ theo địa chỉ là mã băm SHA-256 của chính nó (`.pfs/cas/objects/ab/cd/...`).
  - Mối quan hệ giữa các tệp tin và nguồn gốc tạo tác được biểu diễn bằng cây Merkle Directed Acyclic Graph (Merkle DAG) trong cơ sở dữ liệu.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Content-Addressed Storage (CAS) kết hợp Merkle DAG**.
- Siêu dữ liệu (Metadata, ACL, Traceability) được quản lý trong RDBMS (SQLite/PostgreSQL), trong khi nội dung tệp tin thô được lưu trữ dạng blob nén (Zstandard) trong CAS Store.
- Mỗi Artifact Version là một node bất biến trong Merkle DAG. Khi nghiệm thu một Milestone, mã băm gốc (Merkle Root Hash) đại diện cho toàn bộ trạng thái của hàng ngàn tệp tin dự án trong duy nhất một chuỗi băm 64 ký tự.
- Cho phép đối soát tính toàn vẹn (Tampering Detection) trong nháy mắt bằng cách so sánh mã băm của tệp tin trên đĩa với giá trị lưu trong Merkle DAG.

## 5. Consequences & Trade-offs
- *Tích cực:* Chống giả mạo tuyệt đối, chống trùng lặp dữ liệu tự động, khôi phục phiên bản lịch sử tức thì.
- *Thách thức:* Cần một tầng trừu tượng hóa để ánh xạ từ CAS Blob sang cây thư mục làm việc thông thường khi xuất bản tệp tin cho người dùng.

## 6. Revisit Conditions

Cơ chế lưu trữ CAS và Merkle DAG sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi kích thước trung bình của các artifact nhị phân vượt quá 500MB (ví dụ: các mô hình máy học hoặc dữ liệu dataset nghiên cứu lớn) dẫn đến việc tính toán mã băm SHA-256 toàn phần gây nghẽn CPU và I/O, đòi hỏi phải chuyển sang thuật toán băm phân mảnh dạng cây (Tree Hashing / BLAKE3) kết hợp chunking động (Content-Defined Chunking qua FastCDC).
2. Khi chi phí dọn rác (Garbage Collection / unreferenced blobs retention) trên ổ đĩa vượt quá 25% tổng dung lượng lưu trữ của workspace và việc quét đồ thị Merkle DAG để xóa tệp rác làm chậm tiến trình vận hành nền.
