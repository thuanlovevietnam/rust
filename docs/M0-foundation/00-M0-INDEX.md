# PFS-M0-SPEC-000 — M0 Foundation Document Index

**Document ID:** PFS-M0-SPEC-000  
**Document Type:** Specification Index  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Proposed — Awaiting Owner Approval  
**Language:** Vietnamese (technical terms retained in English)  
**Parent:** PFS-M0-SPEC-001 v1.0.0  
**Amendment Reference:** PFS-M0-REVIEW-001 v1.0.0  
**Target Milestone:** M0 — Foundation Methodology  
**Document Authority:** This index governs navigation, document identity, and the allocation of authoritative subject matter across the M0 document package. It does not override the substantive rules in domain documents.

---

## 1. Purpose

Tài liệu này là điểm vào chính thức của bộ tài liệu M0. Nó xác định:

1. Danh mục tài liệu thuộc M0.
2. Phạm vi và trách nhiệm của từng tài liệu.
3. Nguồn có thẩm quyền đối với từng nhóm nội dung.
4. Quy tắc tham chiếu, định danh và truy vết.
5. Trạng thái phát hành và điều kiện nghiệm thu M0.

Mục tiêu là để Project Owner, Architect, AI Agent, Reviewer và Auditor có thể xác định đúng tài liệu cần đọc, không tự tạo ra các quy tắc trùng lặp hoặc diễn giải mâu thuẫn.

## 2. Document Package

Thư mục chuẩn:

`docs/M0-foundation/`

| File | Document ID | Tên | Nội dung có thẩm quyền |
|---|---|---|---|
| `00-M0-INDEX.md` | PFS-M0-SPEC-000 | M0 Foundation Document Index | Danh mục, điều hướng, document authority |
| `01-PFS-VISION.md` | PFS-M0-SPEC-001 | PFS Vision | Tầm nhìn, vấn đề, mục tiêu dài hạn |
| `02-PRODUCT-DEFINITION.md` | PFS-M0-SPEC-002 | Product Definition | Định nghĩa sản phẩm, phạm vi, ranh giới |
| `03-UNIVERSAL-PROJECT-MODEL.md` | PFS-M0-SPEC-003 | Universal Project Model | Project Profile, capability, tailoring |
| `04-FOUNDATION-METHODOLOGY.md` | PFS-M0-SPEC-004 | Foundation Methodology | Quy trình tạo nền móng dự án |
| `05-GOVERNANCE-MODEL.md` | PFS-M0-SPEC-005 | Governance Model | Cơ chế quản trị xuyên suốt |
| `06-AUTHORITY-AND-DECISION-MODEL.md` | PFS-M0-SPEC-006 | Authority and Decision Model | Vai trò, quyền quyết định, xử lý xung đột |
| `07-ARTIFACT-AND-TRACEABILITY-MODEL.md` | PFS-M0-SPEC-007 | Artifact and Traceability Model | Artifact identity, metadata, traceability |
| `08-HYBRID-EXECUTION-MODEL.md` | PFS-M0-SPEC-008 | Hybrid Execution Model | AI reasoning và deterministic automation |
| `09-AGENT-SECURITY-MODEL.md` | PFS-M0-SPEC-009 | Agent Security Model | Quyền hạn và giới hạn thực thi của agent |
| `10-QUALITY-AND-ACCEPTANCE-MODEL.md` | PFS-M0-SPEC-010 | Quality and Acceptance Model | Quality dimensions, evidence, acceptance |
| `11-VERSION-AND-CHANGE-MANAGEMENT.md` | PFS-M0-SPEC-011 | Version and Change Management | Versioning, compatibility, change control |
| `12-SECURITY-AND-SUPPLY-CHAIN.md` | PFS-M0-SPEC-012 | Security and Supply Chain | Data classification, provenance, trust |
| `13-MILESTONE-ROADMAP.md` | PFS-M0-SPEC-013 | Milestone Roadmap | Ranh giới M0–M4 và dependency |
| `14-M0-ACCEPTANCE-CRITERIA.md` | PFS-M0-SPEC-014 | M0 Acceptance Criteria | Điều kiện kiểm chứng M0 |
| `15-M0-REVIEW-REPORT.md` | PFS-M0-SPEC-015 | M0 Review Report | Kết quả review, findings, disposition |

## 3. Document Authority Map

Mỗi chủ đề có một tài liệu chịu trách nhiệm định nghĩa nội dung chuẩn. Các tài liệu khác chỉ được:

- Tham chiếu bằng Document ID hoặc Requirement ID.
- Giải thích cách áp dụng trong phạm vi của mình.
- Đưa ra quy tắc triển khai chi tiết nếu được tài liệu có thẩm quyền cho phép.

Không sao chép một quy tắc chuẩn vào nhiều tài liệu rồi duy trì độc lập.

| Chủ đề | Tài liệu có thẩm quyền |
|---|---|
| Tầm nhìn và mục tiêu PFS | PFS-M0-SPEC-001 |
| Định nghĩa sản phẩm và scope | PFS-M0-SPEC-002 |
| Project Profile và Capability Model | PFS-M0-SPEC-003 |
| Lifecycle và phương pháp tạo nền móng | PFS-M0-SPEC-004 |
| Governance xuyên suốt | PFS-M0-SPEC-005 |
| Roles, decision rights, authority conflicts | PFS-M0-SPEC-006 |
| Artifact identity, metadata, traceability | PFS-M0-SPEC-007 |
| AI reasoning và deterministic automation | PFS-M0-SPEC-008 |
| Agent permission và execution restrictions | PFS-M0-SPEC-009 |
| Quality evaluation và acceptance evidence | PFS-M0-SPEC-010 |
| Versioning, compatibility, change control | PFS-M0-SPEC-011 |
| Data classification, provenance, supply chain | PFS-M0-SPEC-012 |
| Milestone scope và dependency | PFS-M0-SPEC-013 |
| M0 pass/fail conditions | PFS-M0-SPEC-014 |
| Review findings và remediation evidence | PFS-M0-SPEC-015 |

Nếu phát hiện xung đột giữa các tài liệu, không tự chọn tài liệu theo số thứ tự hoặc ngày sửa gần nhất. Phải ghi nhận xung đột và xử lý theo Authority and Decision Model.

## 4. Normative Language

Các từ khóa sau có ý nghĩa bắt buộc:

- **MUST:** Bắt buộc phải thực hiện.
- **MUST NOT:** Tuyệt đối không được thực hiện.
- **SHOULD:** Nên thực hiện; nếu không thực hiện phải có lý do.
- **SHOULD NOT:** Không nên thực hiện; ngoại lệ phải được giải trình.
- **MAY:** Có thể lựa chọn.
- **PROPOSED:** Đề xuất, chưa được Project Owner phê duyệt.
- **APPROVED:** Đã được đúng người có thẩm quyền phê duyệt.
- **ACCEPTED:** Đã được nghiệm thu theo tiêu chí tương ứng.
- **SUPERSEDED:** Đã được thay thế bởi phiên bản hoặc quyết định mới.

AI Agent MUST giữ nguyên sự khác biệt giữa yêu cầu bắt buộc, khuyến nghị và lựa chọn tùy nghi.

## 5. Artifact Identification

Mỗi tài liệu chuẩn MUST có Document ID ổn định, không phụ thuộc tên file hoặc vị trí lưu trữ.

Quy tắc ID:

`PFS-M0-SPEC-NNN`

Trong đó:

- `PFS`: Project Foundation System.
- `M0`: Milestone.
- `SPEC`: loại artifact.
- `NNN`: số thứ tự ba chữ số.

Các loại artifact khác sử dụng namespace tương ứng, ví dụ:

- `PFS-REQ-NNN`: Requirement.
- `PFS-ADR-NNN`: Architecture Decision Record.
- `PFS-POL-NNN`: Policy.
- `PFS-CON-NNN`: Contract.
- `PFS-SKILL-NNN`: Agent Skill.
- `PFS-TEST-NNN`: Test Specification.
- `PFS-REPORT-NNN`: Report.

ID đã phát hành MUST NOT được tái sử dụng cho artifact khác. Việc đổi tên hoặc di chuyển file không làm thay đổi ID.

## 6. Standard Document Metadata

Các tài liệu M0 SHOULD sử dụng metadata sau:

- Document ID
- Title
- Document Type
- Project
- Version
- Status
- Owner
- Approver
- Created Date
- Updated Date
- Parent / Related Documents
- Supersedes / Superseded By
- Target Milestone

Nếu chưa có thông tin hoặc chưa được quyết định, ghi rõ `TBD` hoặc `Not Assigned`; không tự tạo tên người phê duyệt, ngày phê duyệt hay trạng thái.

## 7. Requirement and Traceability Rules

Mọi requirement có ảnh hưởng đến kiến trúc, bảo mật, governance hoặc acceptance MUST có ID ổn định theo canonical domain namespace.

Ví dụ:

`M0-UNI-001` (canonical) — kế thừa/ánh xạ từ legacy ID `M0-REQ-001`.

Requirement tối thiểu phải thể hiện:

- ID.
- Statement.
- Rationale.
- Priority hoặc criticality.
- Source.
- Owner hoặc authority.
- Verification method.
- Acceptance evidence.
- Status.

Traceability SHOULD thể hiện được quan hệ:

`Vision → Product Objective → Requirement → Design Rule / Decision → Artifact → Verification → Acceptance`

Không được coi việc một requirement xuất hiện trong văn bản là bằng chứng nó đã được thực hiện.

## 8. Status and Approval Integrity

Trạng thái tài liệu và trạng thái milestone là hai khái niệm khác nhau.

Một tài liệu `Proposed` không được trình bày như quy tắc đã được phê duyệt.

Một milestone chỉ được đánh dấu `Accepted` khi:

1. Đủ deliverables bắt buộc.
2. Các acceptance criteria đã được kiểm chứng.
3. Không còn critical unresolved finding.
4. Có evidence phù hợp.
5. Project Owner hoặc người được ủy quyền đã phê duyệt.

AI Agent không có quyền tự chuyển trạng thái tài liệu hoặc milestone sang `Approved` hay `Accepted`.

## 9. Conflict Handling

Khi hai tài liệu hoặc hai quyết định mâu thuẫn:

1. Dừng việc thực hiện các task phụ thuộc vào nội dung đang xung đột.
2. Ghi lại các nguồn mâu thuẫn và đoạn nội dung liên quan.
3. Xác định domain authority và người có quyền quyết định.
4. Phân tích tác động đến requirement, architecture, security, implementation và acceptance.
5. Đề xuất phương án giải quyết kèm evidence.
6. Chờ đúng người có thẩm quyền phê duyệt.
7. Cập nhật tài liệu và traceability sau quyết định.

Không được âm thầm sửa một tài liệu để làm cho mâu thuẫn biến mất.

## 10. M0 Package Completion

M0 package chỉ được xem là hoàn thành về mặt tài liệu khi:

- Đủ 16 tài liệu trong danh mục.
- Mỗi tài liệu có ID và metadata hợp lệ.
- Có document authority map.
- Có requirement traceability.
- Các thuật ngữ được sử dụng nhất quán.
- Các ranh giới milestone không chồng lấn.
- Mọi finding có disposition.
- Có acceptance evidence.
- Không có critical contradiction chưa được giải quyết.

Việc hoàn thành tài liệu không đồng nghĩa với Owner Approval hoặc M0 Acceptance.

## 11. Change Control

Mọi thay đổi đối với tài liệu M0 sau khi được phê duyệt MUST:

- Có lý do và nguồn yêu cầu.
- Xác định artifact bị ảnh hưởng.
- Đánh giá tác động và compatibility.
- Giữ lại lịch sử phiên bản.
- Được phê duyệt theo authority tương ứng.

Không sửa trực tiếp nội dung đã phê duyệt mà không ghi nhận thay đổi.

## 12. Current Package Status

| Item | Status |
|---|---|
| M0 v1.0 review | Completed |
| M0 review findings | 12 findings identified |
| M0 v1.1 package | Proposed |
| M0 document package | In preparation |
| Owner approval | Pending |
| M0 acceptance | Not accepted |
| M1 authorization | Not authorized |

## 13. Next Milestone

M1 chỉ được khởi động sau khi M0 đạt điều kiện phê duyệt và nghiệm thu. M1 sẽ phát triển chi tiết document model, architecture model, contracts và decision records trên cơ sở phương pháp luận đã được M0 chốt.

---

**End of Document — PFS-M0-SPEC-000 v1.1.0**
