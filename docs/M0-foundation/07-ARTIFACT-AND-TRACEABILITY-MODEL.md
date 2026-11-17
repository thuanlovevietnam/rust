# PFS-M0-SPEC-007 — Artifact and Traceability Model

**Document ID:** PFS-M0-SPEC-007  
**Document Type:** Artifact and Traceability Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-000, PFS-M0-SPEC-003, PFS-M0-SPEC-004, PFS-M0-SPEC-005, PFS-M0-SPEC-006, PFS-M0-SPEC-010, PFS-M0-SPEC-011, PFS-M0-SPEC-012

---

## 1. Purpose

Tài liệu này định nghĩa mô hình quản lý artifacts và traceability trong PFS.

PFS không được coi tài liệu chỉ là các file Markdown rời rạc. Mỗi artifact là một đối tượng có identity, type, version, provenance, authority, lifecycle và relationships.

Mục tiêu:

- Nhận diện artifact ổn định.
- Xác định nguồn có thẩm quyền.
- Truy vết nguồn gốc và thay đổi.
- Liên kết requirements, decisions, designs và tests.
- Phát hiện orphan artifacts.
- Phát hiện nội dung lỗi thời hoặc mâu thuẫn.
- Hỗ trợ reproducibility và baseline management.
- Hỗ trợ nhiều loại dữ liệu và nhiều định dạng đầu ra.

## 2. Artifact Definition

Artifact là một đơn vị thông tin có ý nghĩa trong Project Foundation.

Ví dụ:

- Requirement.
- Specification.
- Policy.
- Decision Record.
- Architecture Description.
- Contract.
- Project Profile.
- Agent Instruction.
- Skill.
- Workflow.
- Template.
- Test Specification.
- Validation Report.
- Audit Report.
- Manifest.
- Baseline.

Artifact có thể được lưu trong:

- Markdown.
- JSON.
- YAML.
- Diagram.
- Source files.
- Structured database records.
- Other approved formats.

Không được đồng nhất artifact với file. Một file có thể chứa nhiều artifacts; một artifact có thể được biểu diễn bằng nhiều file hoặc representation.

## 3. Artifact Identity

Mỗi artifact có identity ổn định, không phụ thuộc:

- Tên file.
- Đường dẫn.
- File extension.
- Nội dung hiện tại.
- AI provider.
- Người tạo.

### 3.1. Identity Rules

- Artifact ID MUST unique trong namespace và scope được xác định.
- ID MUST NOT được tái sử dụng sau khi artifact bị retire.
- Đổi tên file không làm thay đổi Artifact ID.
- Di chuyển vị trí lưu trữ không làm thay đổi Artifact ID.
- Một artifact có nhiều version vẫn giữ cùng logical identity.
- Artifact khác nhau không được dùng chung identity chỉ vì có nội dung giống nhau.

### 3.2. ID Namespace

Ví dụ:

| Prefix | Artifact Type |
|---|---|
| PFS-PRJ | Project |
| PFS-REQ | Requirement |
| PFS-SPEC | Specification |
| PFS-ADR | Architecture Decision Record |
| PFS-POL | Policy |
| PFS-CON | Contract |
| PFS-SKILL | Agent Skill |
| PFS-WF | Workflow |
| PFS-TPL | Template |
| PFS-TEST | Test Specification |
| PFS-REPORT | Report |
| PFS-EXC | Exception |
| PFS-APR | Approval |
| PFS-EVD | Evidence |
| PFS-MAN | Manifest |
| PFS-BL | Baseline |

Milestone-specific prefixes có thể được bổ sung nhưng không được gây trùng lặp.

## 4. Artifact Metadata

Mỗi artifact SHOULD có metadata phù hợp với loại artifact.

### 4.1. Core Metadata

- Artifact ID.
- Title.
- Artifact Type.
- Project ID.
- Version.
- Status.
- Owner.
- Author / Creator.
- Approver nếu cần.
- Created At.
- Updated At.
- Source.
- Provenance.
- Classification.
- Related Artifacts.
- Supersedes.
- Superseded By.
- Effective Scope.

### 4.2. Type-Specific Metadata

Một Requirement có thể cần:

- Priority.
- Criticality.
- Verification Method.
- Acceptance Criteria.

Một ADR có thể cần:

- Context.
- Options.
- Decision.
- Rationale.
- Consequences.
- Approval.

Một Test Specification có thể cần:

- Preconditions.
- Steps.
- Expected Results.
- Evidence.
- Coverage.

Không ép mọi artifact phải có toàn bộ fields của mọi loại.

### 4.3. Unknown Metadata

Thông tin chưa có phải được biểu diễn bằng trạng thái phù hợp như:

- TBD.
- Unknown.
- Not Assigned.
- Not Applicable.

Không tự tạo giá trị để làm cho metadata có vẻ đầy đủ.

## 5. Artifact Lifecycle

Artifact lifecycle gồm:

- Draft.
- Proposed.
- Under Review.
- Approved.
- Active.
- Superseded.
- Rejected.
- Retired.
- Archived.

Ý nghĩa:

**Draft:** Nội dung đang được soạn thảo.

**Proposed:** Đã hình thành đề xuất để xem xét.

**Under Review:** Đang được đánh giá.

**Approved:** Được authority phê duyệt.

**Active:** Đang có hiệu lực trong phạm vi xác định.

**Superseded:** Đã bị thay thế nhưng vẫn được giữ lịch sử.

**Rejected:** Bị từ chối.

**Retired:** Không còn được sử dụng.

**Archived:** Được lưu để tham khảo hoặc audit.

Không phải mọi artifact đều phải đi qua tất cả trạng thái. Lifecycle chi tiết phụ thuộc artifact type.

`Approved` không đồng nghĩa `Active` nếu artifact cần điều kiện hiệu lực hoặc ngày áp dụng.

## 6. Versioning

Phân biệt:

- Artifact Identity: ID ổn định.
- Artifact Version: phiên bản nội dung.
- Package Version: phiên bản của nhóm artifacts.
- Baseline Version: phiên bản foundation được chấp thuận.
- Generator Version: phiên bản công cụ tạo artifacts.
- Template Version: phiên bản template.
- Schema Version: phiên bản cấu trúc dữ liệu.

Không gộp tất cả vào một version number.

### 6.1. Version Change

Một version mới phải ghi:

- Change summary.
- Reason.
- Source.
- Affected requirements.
- Affected decisions.
- Compatibility impact.
- Approval requirements.
- Validation evidence.

### 6.2. Approved Version Integrity

Nội dung đã được phê duyệt phải có khả năng xác định chính xác.

Có thể sử dụng content hash hoặc immutable revision identifier để phát hiện thay đổi.

Hash không chứng minh nội dung đúng; nó chỉ hỗ trợ xác định tính toàn vẹn của nội dung được tham chiếu.

## 7. Artifact Relationships

Artifact relationships là mô hình quan hệ có định danh giữa các artifacts.

Các relationship types tham khảo:

- derives_from.
- satisfies.
- refines.
- constrains.
- implements.
- verifies.
- validates.
- approves.
- supersedes.
- depends_on.
- references.
- contradicts.
- mitigates.
- produces.
- owned_by.
- reviewed_by.

Relationship type phải có ý nghĩa xác định, không được dùng tùy tiện.

### 7.1. Relationship Record

Một relationship SHOULD có:

- Relationship ID.
- Source Artifact ID.
- Target Artifact ID.
- Relationship Type.
- Scope.
- Version context.
- Created By.
- Evidence hoặc rationale.
- Status.

### 7.2. Directionality

Relationship phải xác định chiều.

Ví dụ:

`PFS-REQ-001 --verified_by--> PFS-TEST-001`

Không diễn giải quan hệ ngược chiều nếu semantics không cho phép.

### 7.3. Relationship Integrity

PFS MUST phát hiện:

- Broken references.
- Missing targets.
- Invalid relationship types.
- Unsupported cycles.
- Version mismatch.
- Relationships đến retired artifacts khi không được phép.

Một số cycles có thể hợp lệ về mặt nghiệp vụ, nhưng phải được xác định rõ thay vì mặc định cấm hoặc mặc định cho phép.

## 8. Traceability Model

Traceability phải hỗ trợ đường truy vết từ mục tiêu đến evidence.

Mô hình tổng quát:

`Vision → Objective → Requirement → Decision / Design → Artifact → Verification → Evidence → Acceptance`

Đây là một graph logic, không phải cây thư mục.

### 8.1. Forward Traceability

Từ requirement có thể xác định:

- Decision liên quan.
- Architecture hoặc policy liên quan.
- Artifact được tạo.
- Test hoặc validation liên quan.
- Evidence chứng minh.
- Acceptance result.

### 8.2. Backward Traceability

Từ artifact hoặc test có thể xác định:

- Nguồn yêu cầu.
- Mục tiêu phục vụ.
- Decision làm cơ sở.
- Người có authority.
- Version được sử dụng.

### 8.3. Orphan Detection

PFS SHOULD phát hiện:

- Requirement không có verification.
- Design không có requirement hoặc decision source.
- Test không có target.
- Policy không có owner.
- Decision không có context.
- Artifact không có provenance.
- Baseline thiếu manifest.

Không phải mọi artifact đều phải có parent requirement. Artifact có thể được tạo bởi governance, compliance hoặc operational necessity; trường hợp này phải ghi source phù hợp.

## 9. Source of Truth

Source of truth không phải một file cố định.

Nó là artifact hoặc tập hợp artifacts có authority trong một domain, version và scope cụ thể.

Để được dùng làm authoritative source, cần kiểm tra:

- Artifact identity.
- Type.
- Domain ownership.
- Approval.
- Effective scope.
- Version.
- Supersession.
- Conflicts.

Chi tiết authority resolution thuộc `PFS-M0-SPEC-006`.

Không tự động coi nội dung mới hơn là authoritative.

## 10. Provenance

Provenance trả lời:

- Artifact đến từ đâu?
- Ai hoặc thành phần nào tạo ra?
- Dựa trên nguồn nào?
- Dùng template nào?
- Dùng AI provider hoặc automation nào nếu cần ghi nhận?
- Có những biến đổi nào?
- Đã được kiểm chứng ra sao?

Provenance có thể bao gồm:

- Creator.
- Source Artifact IDs.
- External source references.
- Tool identity and version.
- Template ID and version.
- Model/provider metadata khi phù hợp.
- Generation run ID.
- Timestamp.
- Content hash.
- Validation report.

Không ghi secrets hoặc dữ liệu nhạy cảm không cần thiết vào provenance.

## 11. Evidence Model

Evidence là dữ liệu hỗ trợ một claim, verification result hoặc approval.

Các loại evidence:

- Document evidence.
- Test result.
- Validation result.
- Review finding.
- Source reference.
- Measurement.
- Audit record.
- Execution log.
- Human approval record.

Evidence SHOULD có:

- Evidence ID.
- Claim hoặc requirement được hỗ trợ.
- Source.
- Collection method.
- Timestamp.
- Scope.
- Version context.
- Integrity information.
- Reviewer hoặc validator nếu có.
- Limitations.

### 11.1. Evidence Quality

Đánh giá evidence theo:

- Relevance.
- Authenticity.
- Integrity.
- Completeness.
- Freshness.
- Reproducibility.
- Independence nếu cần.

Không phải mọi evidence đều có cùng mức độ tin cậy.

### 11.2. Evidence Limitation

Một test pass chỉ chứng minh test đó đạt kết quả trong điều kiện đã thực hiện.

Không suy diễn thành bảo đảm toàn hệ thống nếu coverage không hỗ trợ kết luận đó.

## 12. Artifact Ownership and Storage

PFS phải phân biệt:

- Logical ownership.
- Physical storage location.
- Execution ownership.
- Approval authority.

Việc một agent có thể ghi vào file không đồng nghĩa agent đó sở hữu hoặc có quyền phê duyệt nội dung.

Artifact có thể được lưu ở nhiều nơi, nhưng phải xác định canonical reference và synchronization rules.

## 13. Artifact Integrity

PFS SHOULD hỗ trợ:

- Content hashing.
- Version verification.
- Manifest validation.
- Reference validation.
- Duplicate detection.
- Unauthorized modification detection.
- Signature hoặc trusted approval evidence khi cần.

Hash, signature và manifest là các biện pháp hỗ trợ integrity; không tự chứng minh nguồn tạo ra là đáng tin hoặc nội dung chính xác.

## 14. Baseline Model

Baseline là một tập hợp artifacts và versions được xác định tại một thời điểm, được phê duyệt để sử dụng làm nền tảng chính thức.

Baseline SHOULD chứa:

- Baseline ID.
- Project ID.
- Baseline version.
- Included artifact IDs and versions.
- Content hashes hoặc revision identifiers.
- Generator và template versions nếu liên quan.
- Validation report.
- Audit report.
- Approval record.
- Known exceptions.
- Creation timestamp.

Baseline không chỉ là một bản ZIP hoặc một thư mục được sao chép.

## 15. Change Impact Analysis

Khi một artifact thay đổi, PFS SHOULD xác định:

- Artifacts phụ thuộc trực tiếp.
- Requirements bị ảnh hưởng.
- Decisions cần xem xét lại.
- Tests cần chạy lại.
- Security controls bị ảnh hưởng.
- Baseline cần cập nhật.
- Compatibility risk.

Không được tự động thay đổi mọi dependent artifact mà chưa đánh giá semantics và authority.

## 16. Artifact Deletion and Retention

Xóa artifact không phải thao tác mặc định.

Trước khi xóa phải xem xét:

- Legal hoặc contractual retention.
- Audit requirements.
- Dependency references.
- Baseline history.
- Data classification.
- Recovery requirements.

Với artifacts đã được phê duyệt hoặc được tham chiếu bởi baseline, ưu tiên retirement hoặc archival thay vì xóa vật lý.

Nếu xóa vật lý được phép, phải có authority và audit record phù hợp.

## 17. Requirements

| ID | Requirement |
|---|---|
| M0-ART-001 | Mỗi artifact MUST có stable identity. |
| M0-ART-002 | Artifact identity MUST độc lập với file path và file name. |
| M0-ART-003 | Artifact MUST có metadata phù hợp với type. |
| M0-ART-004 | PFS MUST phân biệt artifact version và baseline version. |
| M0-ART-005 | PFS MUST hỗ trợ typed artifact relationships. |
| M0-ART-006 | PFS MUST hỗ trợ forward và backward traceability. |
| M0-ART-007 | PFS MUST hỗ trợ provenance. |
| M0-ART-008 | PFS MUST hỗ trợ evidence association. |
| M0-ART-009 | PFS MUST phát hiện broken references và orphan critical artifacts. |
| M0-ART-010 | PFS MUST giữ lịch sử approved artifacts khi superseded. |
| M0-ART-011 | PFS MUST hỗ trợ baseline manifest. |
| M0-ART-012 | PFS MUST hỗ trợ change impact analysis. |
| M0-ART-013 | PFS MUST kiểm soát deletion và retention. |
| M0-ART-014 | PFS MUST NOT coi file location hoặc timestamp là authority duy nhất. |

## 18. M1 Design Dependencies

M1 phải thiết kế:

- Artifact Registry Schema.
- Artifact ID Allocation.
- Metadata Schema.
- Typed Relationship Registry.
- Provenance Contract.
- Evidence Contract.
- Content Integrity Model.
- Baseline Manifest Schema.
- Change Impact Graph.
- Artifact Lifecycle State Machine.
- Retention and Archival Policy.

---

**End of Document — PFS-M0-SPEC-007 v1.1.0**
