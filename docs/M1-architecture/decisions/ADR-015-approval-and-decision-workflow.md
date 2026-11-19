# ADR-015 — Approval and Decision Workflow: Human-in-the-Loop Ed25519 Sign-off

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-015 |
| Title | Approval and Decision Workflow: Human-in-the-Loop Ed25519 Sign-off |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & Governance Lead |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-10-GOV`, `MOD-09-DEC`, `pfs-governance` |
| Related Requirements | M1-SEC-002, M1-DOM-001 |
| Related Diagrams | DIA-010-governance-approval-sequence.mmd |
| Invariant Reference | INV-04, INV-12 |

---

## 1. Context & Problem Statement

Trong quá trình xây dựng Foundation, việc phê duyệt chuyển đổi giai đoạn (Stage Transitions), chấp thuận các quyết định kiến trúc chiến lược (ADRs) và nghiệm thu Milestone Baseline là những hành động pháp lý và kỹ thuật quan trọng nhất.
- Nếu để hệ thống tự động đánh dấu phê duyệt hoặc chấp nhận việc AI Agent tự ký duyệt cho chính mình, trách nhiệm giải trình sẽ bị xóa bỏ hoàn toàn (Lack of Accountability).
- Nếu cơ chế phê duyệt chỉ là việc click một nút bấm đơn giản trên giao diện web mà không có niêm phong mật mã, các bản ghi kiểm toán có thể bị chỉnh sửa lén lút trong cơ sở dữ liệu.

Cần một cơ chế phê duyệt Human-in-the-Loop nghiêm ngặt có chữ ký số mật mã không thể chối bỏ (Non-Repudiation).

## 2. Decision Drivers
- **Thẩm quyền con người tối cao (Human Authority Dominance):** AI Agent tuyệt đối không có quyền tự phê duyệt các quyết định L3+.
- **Chống chối bỏ (Non-Repudiation):** Bản ghi phê duyệt phải được ký bằng khóa bí mật bất đối xứng của người có thẩm quyền.
- **Bảo toàn toàn vẹn nội dung:** Chữ ký số phải khóa chặt mã băm SHA-256 của toàn bộ nội dung tài liệu tại thời điểm phê duyệt; bất kỳ sự thay đổi nào sau đó sẽ làm chữ ký mất hiệu lực.

## 3. Options Considered
- **Option A: Simple Boolean Flag in Database (`is_approved = true`):**
  - Cập nhật một cột boolean trong database.
  - *Nhược điểm:* Dễ dàng bị giả mạo bởi bất kỳ ai có quyền truy cập SQL; không thể chứng minh ai là người thực sự bấm duyệt; không có giá trị kiểm toán pháp lý.
- **Option B (Được chọn): Cryptographic Approval Workflow với Chữ ký số Ed25519:**
  - Mỗi cấp thẩm quyền con người (Project Owner, Lead Architect, QA Lead) sở hữu một cặp khóa bất đối xứng Ed25519 (Khóa công khai lưu trong Authority Registry, khóa bí mật lưu an toàn trên máy trạm cá nhân hoặc Secure Enclave).
  - Khi phê duyệt, người dùng tạo một **Approval Record** bao gồm: Target Resource Hash + Policy Version + Timestamp + Decision, được ký số bằng thuật toán Ed25519.
  - Bản ghi được niêm phong vĩnh viễn vào Append-only Audit Ledger.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Cryptographic Approval Workflow với Chữ ký số Ed25519**.
- Quy trình chuyển đổi giai đoạn bắt buộc phải kiểm tra sự tồn tại của một `ApprovalRecord` hợp lệ:
  1. Kiểm tra chữ ký số khớp với Public Key của chủ thể được ủy quyền trong `AuthorityRegistry`.
  2. Kiểm tra mã băm của tài liệu đích trùng khớp 100% với mã băm trong chữ ký.
  3. Kiểm tra người ký duyệt thỏa mãn nguyên tắc Phân tách nhiệm vụ (Separation of Duties - SoD: Người duyệt không được là người tạo đề xuất).
- Nếu chữ ký không hợp lệ hoặc thiếu, Workflow State Machine chặn đứng việc chuyển trạng thái sang `Approved`.

## 5. Consequences & Trade-offs
- *Tích cực:* Tính minh bạch tuyệt đối; bằng chứng kiểm toán không thể chối bỏ; đáp ứng các tiêu chuẩn khắt khe nhất của ISO 27001 và SOC 2.
- *Thách thức:* Người vận hành cần quản lý an toàn khóa bí mật cá nhân (Private Key) trên thiết bị của mình.

## 6. Revisit Conditions

Quy trình phê duyệt và chữ ký số Ed25519 sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi máy tính lượng tử (Quantum Computing) đạt bước đột phá có khả năng phá vỡ thuật toán đường cong elliptic Edwards (Curve25519) trong khung thời gian dự báo của NIST, đòi hỏi chuyển đổi sang các thuật toán chữ ký kháng lượng tử (Post-Quantum Cryptography như ML-DSA / Dilithium).
2. Khi quy trình quản trị doanh nghiệp yêu cầu tích hợp bắt buộc với hạ tầng chứng thực khóa công khai x509 truyền thống của doanh nghiệp (Enterprise PKI / Hardware Security Modules - HSM qua chuẩn PKCS#11) thay cho local raw key pairs.
