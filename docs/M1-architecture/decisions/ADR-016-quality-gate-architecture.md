# ADR-016 — Quality Gate Architecture: Hierarchical Gates and Evidence Sufficiency

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-016 |
| Title | Quality Gate Architecture: Hierarchical Gates and Evidence Sufficiency |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & QA Lead |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-23-QLT`, `MOD-24-EVI`, `pfs-quality` |
| Related Requirements | M1-SEC-004, M1-DOM-003 |
| Related Diagrams | DIA-008-workflow-state-machine.mmd |
| Parent Baseline | [PFS-M0-SPEC-010](file:///C:/Users/OK259/rust/docs/M0-foundation/10-QUALITY-AND-ACCEPTANCE-MODEL.md) |
| Invariant Reference | INV-07 |

---

## 1. Context & Problem Statement

Trong nhiều dự án phần mềm, việc đánh giá chất lượng thường bị biến tướng thành các buổi họp hình thức, hoặc dựa trên điểm số trung bình (Weighted Score). Khi áp dụng cách tính điểm trung bình: một hệ thống có điểm kiểm thử giao diện 10/10 và tài liệu 10/10 có thể đạt điểm trung bình 8.5/10, che giấu đi một lỗ hổng an ninh nghiêm trọng (Critical Security Finding điểm 0/10).

PFS đòi hỏi một kiến trúc Cổng Chất lượng (Quality Gate Architecture) có tính phân cấp, áp dụng nguyên tắc chặn đứng nghiêm ngặt và yêu cầu bằng chứng kiểm chứng độc lập.

## 2. Decision Drivers
- **Không có bằng chứng, không đạt (No Evidence, No Pass):** Tiêu chí chất lượng chỉ được công nhận khi có tệp bằng chứng thực nghiệm nộp kèm.
- **Khóa chuyển giai đoạn khi có lỗi Critical (Critical Severity Hard Blocking):** Một lỗi Critical duy nhất sẽ lập tức khóa cổng, không cho phép chuyển giai đoạn.
- **Minh bạch về ngoại lệ (Formal Waivers):** Mọi trường hợp bỏ qua lỗi phải được lập biên bản ngoại lệ có thời hạn và có chữ ký số của cấp thẩm quyền L4/L5.

## 3. Options Considered
- **Option A: Weighted Average Score (Điểm trung bình có trọng số):**
  - Chấm điểm từ 1-100; nếu tổng điểm > 80 thì cho qua.
  - *Nhược điểm:* Cho phép các lỗi chí mạng (như rò rỉ secret, sai lệch kiến trúc) bị che lấp bởi các tiêu chí phụ dễ đạt điểm cao.
- **Option B (Được chọn): Hierarchical Quality Gates với Phân loại Mức độ Nghiêm trọng (Severity-Based Hard Gates):**
  - Mỗi giai đoạn sở hữu một danh mục Cổng chất lượng xác định.
  - Mỗi Cổng đánh giá danh sách các Findings theo thang mức độ: `Critical`, `High`, `Medium`, `Low`, `Informational`.
  - Quy tắc đóng mở: **Gate Pass $\iff$ (Critical Count == 0) AND (Unwaived High Count == 0) AND (All Evidence Verified)**.

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option B: Hierarchical Quality Gates với Phân loại Mức độ Nghiêm trọng**.
- Crate `pfs-quality` thực thi việc đánh giá các cổng chất lượng hoàn toàn bằng logic xác định.
- Bằng chứng kiểm chứng (Evidence) phải là các tệp tin có thật (kết quả linter, log kiểm thử, mã băm SHA-256) được lưu trữ trong Evidence Store. Các khẳng định bằng lời nói suông hoặc suy luận chưa kiểm chứng của AI tuyệt đối không được chấp nhận làm bằng chứng.
- Nếu một cổng bị khóa (`Blocked`), hệ thống xuất ra danh sách các vi phạm và hướng dẫn khắc phục cụ thể cho đội ngũ phát triển.

## 5. Consequences & Trade-offs
- *Tích cực:* Đảm bảo chất lượng thực chất 100%; ngăn chặn hoàn toàn nợ kỹ thuật và lỗ hổng an ninh trôi vào giai đoạn sản xuất.
- *Thách thức:* Đòi hỏi đội ngũ phát triển phải xử lý triệt để các lỗi Critical trước khi có thể chuyển giai đoạn.

## 6. Revisit Conditions

Kiến trúc Cổng chất lượng và Evidence Engine sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. Khi thời gian thực thi toàn bộ các bộ kiểm định tự động (Full Automated Verification Suite) tại cổng nghiệm thu vượt quá 10 phút trên quy mô dự án lớn, đòi hỏi phải chia tách cổng thành chế độ kiểm tra nhanh (Fast-Path Verification) cho các commits hàng ngày và chế độ kiểm định chuyên sâu (Deep-Audit) cho các bản phát hành chính thức.
2. Khi chính sách quản trị rủi ro của doanh nghiệp cho phép cơ chế chấp nhận rủi ro có điều kiện (Risk Acceptance Waiver) kèm chữ ký số của cấp lãnh đạo cao hơn đối với một số lỗi High/Medium có biện pháp bồi hoàn thay thế.
