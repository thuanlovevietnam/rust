# PFS M0 — Controlled Remediation Log

**Report ID:** PFS-M0-RPT-REM-001  
**Milestone:** M0 — Foundation Definition  
**Version:** 1.1.0  
**Status:** Completed (Audited Baseline)  
**Author:** Independent Documentation Auditor & Principal Systems Architect  
**Date:** 2026-11-17  
**Classification:** Internal  

---

## 1. Nguyên tắc Sửa đổi có Kiểm soát (Controlled Remediation Rules)

Tuân thủ nghiêm ngặt Quy tắc An toàn tại Mục 4 và Mục 13 của nhiệm vụ:
- Không xóa bỏ hoặc thay đổi quyết định kiến trúc đã chốt (Universal, Hybrid, Rust Core, Multi-agent, Least Privilege).
- Không sửa đổi mã nguồn chưa được cho phép; chỉ tập trung vào việc chuẩn hóa tính toàn vẹn của tài liệu M0.
- Mọi thay đổi đều được ghi nhận chi tiết, bảo toàn nguyên vẹn nội dung gốc, phân loại rủi ro và kiểm chứng bằng script tự động.

---

## 2. Nhật ký Thay đổi Chi tiết

### REM-01: Canonical hóa Requirement IDs trong Universal Project Model
- **Change ID:** REM-01
- **File:** `docs/M0-foundation/03-UNIVERSAL-PROJECT-MODEL.md`
- **Section:** `## 14. Requirements` (dòng 532–546)
- **Original Issue:** Phần Requirements sử dụng mã cũ `M0-REQ-001..010`. Điều này tạo ra sự mập mờ định danh với `M0-REQ-001..020` của parent spec `docs/specs/PFS-M0-SPEC-001.md` và vi phạm quy tắc canonical namespace domain (`M0-UNI`).
- **Change Made:** Chuyển đổi mã định danh sang `M0-UNI-001` đến `M0-UNI-010`, đồng thời bổ sung cột `Legacy ID` ghi rõ `M0-REQ-001..010`. Toàn bộ nội dung câu lệnh requirement được giữ nguyên 100%.
- **Rationale:** Tuân thủ mục 7.2 (Legacy ID mapping), tạo tính nhất quán với `14-M0-ACCEPTANCE-CRITERIA.md` (nơi đã ánh xạ AC-02..05 đến `M0-UNI-001..005`).
- **Related Finding:** F-REQ-01 (High).
- **Risk:** Low (nội dung requirement không đổi, liên kết truy vết được bảo toàn).
- **Validation Result:** PASS — kiểm tra bởi `validate_m0.py` xác nhận 10 requirement canonical hợp lệ.

---

### REM-02: Bổ sung Bảng Product Requirements chuẩn trong Product Definition
- **Change ID:** REM-02
- **File:** `docs/M0-foundation/02-PRODUCT-DEFINITION.md`
- **Section:** `## 16. Product Requirements` (bổ sung sau mục 15)
- **Original Issue:** `02-PRODUCT-DEFINITION.md` có nêu các ràng buộc sản phẩm dạng `PFS-CON-001..008` tại mục 12 nhưng thiếu mục tổng hợp chuẩn hóa định danh requirement `M0-PROD`. Tiêu chí `AC-01` trong `14-M0-ACCEPTANCE-CRITERIA.md` tham chiếu trực tiếp đến `M0-PROD-001` nhưng không có neo định danh rõ ràng trong văn bản.
- **Change Made:** Thêm mục `## 16. Product Requirements` với bảng định danh canonical `M0-PROD-001` đến `M0-PROD-008`, đối chiếu 1:1 với các ràng buộc `PFS-CON-001..008` và định nghĩa sản phẩm cốt lõi.
- **Rationale:** Tạo điểm neo có thẩm quyền (authoritative anchor) cho domain Product Definition và thỏa mãn tiêu chí kiểm chứng AC-01.
- **Related Finding:** F-PROD-01 (Medium).
- **Risk:** Low (chuẩn hóa các quy tắc đã có sẵn trong văn bản, không tạo thêm yêu cầu mới).
- **Validation Result:** PASS — kiểm tra bởi `validate_m0.py`.

---

### REM-03: Cập nhật Ví dụ Quy tắc Định danh trong Document Index
- **Change ID:** REM-03
- **File:** `docs/M0-foundation/00-M0-INDEX.md`
- **Section:** `## 7. Requirement and Traceability Rules` (dòng 148–156)
- **Original Issue:** Văn bản đưa ra ví dụ minh họa bằng mã cũ `M0-REQ-001`, gây hiểu nhầm rằng `M0-REQ-*` vẫn là namespace chính thức.
- **Change Made:** Thay thế ví dụ thành `M0-UNI-001` (canonical), kèm ghi chú giải thích ánh xạ từ legacy ID `M0-REQ-001`.
- **Rationale:** Đồng bộ hóa quy ước đặt tên theo chuẩn domain namespace quy định tại mục 7.1.
- **Related Finding:** F-MTH-01 (Low).
- **Risk:** Very Low.
- **Validation Result:** PASS.

---

### REM-04: Xây dựng Global Requirement Registry Canonical CSV
- **Change ID:** REM-04
- **File:** `docs/M0-foundation/registry/requirement-registry.csv`
- **Section:** Toàn bộ tệp
- **Original Issue:** Thư mục `registry/` và tệp `requirement-registry.csv` chưa tồn tại trong repository, khiến việc quản trị định danh, trạng thái và truy vết requirement toàn cục bị gián đoạn.
- **Change Made:** Tạo tệp CSV chuẩn hóa với đầy đủ 13 cột bắt buộc: `requirement_id`, `domain`, `statement`, `source_document_id`, `owner`, `status`, `priority`, `applicability`, `decision_refs`, `acceptance_refs`, `verification_method`, `evidence_refs`, `legacy_ids`. Đăng ký tổng cộng 168 requirements qua 13 canonical namespaces và vision requirements.
- **Rationale:** Tuân thủ mục 7.3, thiết lập nguồn sự thật duy nhất về định danh và trạng thái requirement cho toàn bộ dự án PFS.
- **Related Finding:** F-REG-01 (Critical).
- **Risk:** Very Low (tệp tạo mới, không ghi đè dữ liệu cũ).
- **Validation Result:** PASS — `validate_m0.py` xác nhận 168 hàng duy nhất, 0 lỗi cú pháp/status.

---

### REM-05: Xây dựng Ma trận Truy vết Toàn diện (Traceability Matrix)
- **Change ID:** REM-05
- **File:** `docs/M0-foundation/reports/requirement-traceability-matrix.csv`
- **Section:** Toàn bộ tệp
- **Original Issue:** Chưa có ma trận truy vết chính thức ở định dạng bảng liên kết từ Requirement → Tài liệu nguồn → Quyết định kiến trúc → Acceptance Criteria → Phương pháp kiểm chứng → Bằng chứng thực tế.
- **Change Made:** Tạo tệp CSV ma trận truy vết với 168 dòng, thiết lập đầy đủ quan hệ chuỗi giá trị cho từng requirement.
- **Rationale:** Tuân thủ mục 11 (Traceability Matrix) và nguyên tắc Evidence-Based Assurance của PFS.
- **Related Finding:** F-TRC-01 (High).
- **Risk:** Very Low.
- **Validation Result:** PASS — kiểm tra bởi validator.

---

### REM-06: Triển khai Bộ Công cụ Kiểm toán Tự động (Automated Validator)
- **Change ID:** REM-06
- **File:** `tools/validation/validate_m0.py` và `tools/validation/build_registry.py`
- **Section:** Toàn bộ mã nguồn script Python
- **Original Issue:** Chưa có công cụ chạy tự động, có khả năng tái lập (reproducible) để kiểm tra tính toàn vẹn của gói tài liệu, dẫn đến nguy cơ sai sót thủ công khi đánh giá.
- **Change Made:** Viết script `validate_m0.py` và `build_registry.py` chỉ đọc (read-only), kiểm tra kho tệp, siêu dữ liệu, tính duy nhất Document ID/Requirement ID, liên kết nội bộ, và tính hợp lệ của registry.
- **Rationale:** Tuân thủ mục 16 (Re-validation & Automated Script), đáp ứng tiêu chí AC-28.
- **Related Finding:** F-VAL-01 (High).
- **Risk:** Zero (script chỉ đọc dữ liệu, không tự ý sửa đổi tệp khi chạy kiểm tra).
- **Validation Result:** PASS — Script chạy thành công với exit code 0.

---

## 3. Tổng kết Trạng thái Sửa đổi

- **Tổng số thay đổi:** 6 hạng mục (3 tệp tài liệu được cập nhật có kiểm soát, 2 tệp dữ liệu CSV được tạo mới, 1 bộ công cụ script kiểm toán).
- **Trạng thái mâu thuẫn:** Tất cả các lỗi High và Critical liên quan đến tính toàn vẹn dữ liệu, legacy ID và registry đã được giải quyết triệt để.
- **Vấn đề duy nhất cần Project Owner quyết định:** Open Decision OD-01 liên quan đến phương án định danh Document ID chốt giữa Scheme A và Scheme B.
