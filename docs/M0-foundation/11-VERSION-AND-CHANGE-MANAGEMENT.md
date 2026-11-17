# PFS-M0-SPEC-011 — Version and Change Management

**Document ID:** PFS-M0-SPEC-011  
**Document Type:** Versioning, Compatibility and Change Control Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-003, PFS-M0-SPEC-005, PFS-M0-SPEC-006, PFS-M0-SPEC-007, PFS-M0-SPEC-008, PFS-M0-SPEC-010, PFS-M0-SPEC-012

---

## 1. Purpose

Tài liệu này định nghĩa cách PFS quản lý phiên bản, tương thích, thay đổi và migration trong toàn bộ vòng đời project foundation.

Mục tiêu:

- Tránh nhầm lẫn giữa các loại version.
- Bảo vệ baseline đã được phê duyệt.
- Kiểm soát thay đổi có ảnh hưởng.
- Phát hiện incompatibility.
- Hỗ trợ migration có thể kiểm tra.
- Giữ lịch sử quyết định.
- Tránh việc agent tự ý thay đổi kiến trúc hoặc requirements.
- Cho phép phát triển PFS mà không phá vỡ project foundation đã tạo.

## 2. Core Principles

1. Explicit Version Identity.
2. Compatibility Must Be Declared.
3. Approved Baselines Are Traceable.
4. Changes Require Impact Analysis.
5. Migration Must Be Controlled.
6. No Silent Breaking Changes.
7. History Must Be Preserved.
8. Rollback Must Be Considered.
9. Versioning Is Not Authority.
10. Reproducibility Requires Version Context.

## 3. Version Domains

PFS MUST phân biệt các version domains:

| Domain | Meaning |
|---|---|
| PFS Engine Version | Phiên bản phần mềm PFS |
| Methodology Version | Phiên bản phương pháp luận |
| Project Profile Version | Phiên bản hồ sơ dự án |
| Artifact Version | Phiên bản của từng artifact |
| Schema Version | Phiên bản cấu trúc dữ liệu |
| Template Version | Phiên bản template |
| Agent Instruction Version | Phiên bản chỉ dẫn agent |
| Skill Version | Phiên bản skill |
| Workflow Version | Phiên bản workflow |
| Provider Adapter Version | Phiên bản adapter |
| Generator Version | Phiên bản generator |
| Foundation Baseline Version | Phiên bản nền tảng được phê duyệt |
| Validation Rules Version | Phiên bản quy tắc kiểm tra |

Không được giả định tăng PFS Engine Version đồng nghĩa tất cả artifact versions đều tăng.

## 4. Semantic Versioning

PFS SHOULD sử dụng Semantic Versioning khi phù hợp.

Dạng:

`MAJOR.MINOR.PATCH`

Ý nghĩa:

- MAJOR: Breaking changes.
- MINOR: Backward-compatible functionality.
- PATCH: Backward-compatible fixes.

### 4.1. Applicability

Semantic Versioning phù hợp với những interfaces và packages có contract tương đối ổn định.

Với các artifacts không có API contract, PFS có thể sử dụng revision-based versioning hoặc versioning policy riêng, nhưng phải khai báo rõ.

### 4.2. Version Is Not Approval

Version mới hơn không tự động được phê duyệt.

Một artifact `2.0.0 Proposed` không có authority cao hơn artifact `1.0.0 Approved` chỉ vì số version lớn hơn.

## 5. Compatibility Model

PFS phải đánh giá compatibility giữa:

- Engine và methodology.
- Engine và schema.
- Generator và template.
- Agent instruction và skill.
- Workflow và tool contract.
- Provider adapter và provider API.
- Foundation baseline và current PFS.
- Project profile và applicable methodology.

Compatibility states:

- Compatible.
- Compatible with Conditions.
- Requires Migration.
- Incompatible.
- Unknown.

Không được mặc định Unknown là Compatible.

### 5.1. Compatibility Declaration

Một component hoặc artifact package SHOULD khai báo:

- Component ID.
- Version.
- Supported version range.
- Required dependencies.
- Incompatible versions.
- Migration requirements.
- Compatibility evidence.

### 5.2. Compatibility Matrix

PFS SHOULD duy trì compatibility matrix cho các components có dependencies.

Matrix phải có thể truy vết tới version cụ thể, không chỉ dựa vào tên sản phẩm.

## 6. Change Classification

Mọi change SHOULD được phân loại:

| Class | Meaning | Example |
|---|---|---|
| Editorial | Không thay đổi semantics | Sửa chính tả |
| Clarification | Làm rõ nội dung | Làm rõ thuật ngữ |
| Corrective | Sửa lỗi | Sửa contract sai |
| Additive | Thêm capability | Thêm optional field |
| Behavioral | Thay đổi behavior | Thay đổi workflow |
| Structural | Thay đổi structure | Thay đổi schema |
| Security | Thay đổi security controls | Thu hẹp quyền |
| Breaking | Phá compatibility | Xóa required field |
| Emergency | Thay đổi khẩn cấp | Vá lỗ hổng nghiêm trọng |

Classification phải dựa trên impact thực tế, không chỉ tên change.

## 7. Change Request

Một change request SHOULD chứa:

- Change ID.
- Requester.
- Date.
- Reason.
- Objective.
- Affected artifacts.
- Proposed change.
- Expected benefits.
- Risks.
- Compatibility impact.
- Security impact.
- Migration impact.
- Validation requirements.
- Required approvals.
- Status.

AI có thể soạn change request nhưng không tự phê duyệt change.

## 8. Change Impact Analysis

Trước khi phê duyệt một change có ảnh hưởng, PFS SHOULD phân tích:

- Direct dependencies.
- Transitive dependencies.
- Requirements.
- Decisions.
- Contracts.
- Policies.
- Templates.
- Agent instructions.
- Tests.
- Existing baselines.
- External integrations.
- Operational environments.

Impact analysis phải phân biệt:

- Confirmed impact.
- Potential impact.
- Unknown impact.

Không suy diễn rằng không có dependency chỉ vì registry chưa ghi nhận dependency.

## 9. Change Lifecycle

Change lifecycle đề xuất:

1. Submitted.
2. Classified.
3. Analyzed.
4. Reviewed.
5. Approved hoặc Rejected.
6. Planned.
7. Implemented.
8. Validated.
9. Released.
10. Closed.

Không phải mọi change đều cần cùng quy trình chi tiết, nhưng critical changes không được bỏ approval và validation bắt buộc.

### 9.1. Change Status Integrity

Agent không được tự chuyển change thành Approved.

Automation không được thực thi change chưa đạt authorization conditions.

Release không được coi là hoàn tất nếu validation bắt buộc chưa đạt.

## 10. Migration Model

Migration là quá trình chuyển artifact, schema, configuration hoặc baseline từ version cũ sang version mới.

Migration plan SHOULD có:

- Migration ID.
- Source version.
- Target version.
- Preconditions.
- Affected artifacts.
- Transformation rules.
- Data preservation requirements.
- Validation rules.
- Failure handling.
- Recovery strategy.
- Approval.
- Evidence.

### 10.1. Migration Safety

Migration SHOULD hỗ trợ:

- Dry-run.
- Preview.
- Backup hoặc recoverable snapshot khi phù hợp.
- Validation trước và sau.
- Conflict detection.
- Audit record.
- Controlled execution.

Không được tuyên bố migration có thể rollback tuyệt đối nếu operation có external side effects hoặc destructive transformations không thể đảo ngược.

### 10.2. Migration Failure

Khi migration thất bại:

- Dừng các bước phụ thuộc nếu an toàn.
- Ghi nhận trạng thái thực tế.
- Không giả định toàn bộ migration đã được rollback.
- Kiểm tra integrity.
- Áp dụng recovery plan.
- Yêu cầu authority nếu cần quyết định tiếp theo.

## 11. Deprecation and Retirement

Một artifact hoặc capability có thể được đánh dấu Deprecated trước khi Retired.

Deprecation notice SHOULD ghi:

- Item ID.
- Current version.
- Reason.
- Replacement.
- Effective date.
- Removal target.
- Migration instructions.
- Compatibility impact.

Không xóa artifact đã được tham chiếu bởi baseline mà không xử lý dependencies và retention requirements.

## 12. Baseline Evolution

Baseline mới không ghi đè lịch sử baseline cũ.

Mỗi baseline phải tham chiếu:

- Parent baseline nếu có.
- Included artifact versions.
- Change records.
- Validation evidence.
- Approved exceptions.
- Approval record.

Baseline mới phải được đánh giá như một candidate mới, không mặc nhiên kế thừa approval của baseline trước.

## 13. Emergency Changes

Emergency changes có thể cần quy trình rút gọn nhưng không được loại bỏ:

- Identity.
- Authorization.
- Scope.
- Audit.
- Post-change validation.
- Retrospective review.

Emergency change phải được đánh dấu và theo dõi riêng.

## 14. Version Pinning

Các execution và generation tasks SHOULD pin những dependency cần thiết:

- Methodology version.
- Template version.
- Schema version.
- Generator version.
- Agent instruction version.
- Skill/workflow version.
- Provider adapter version khi liên quan.

Không được dùng floating latest version cho một reproducible baseline mà không có compatibility control.

## 15. Version and Change Requirements

| ID | Requirement |
|---|---|
| M0-VER-001 | PFS MUST distinguish all relevant version domains. |
| M0-VER-002 | PFS MUST NOT treat newer versions as automatically authoritative. |
| M0-VER-003 | PFS MUST declare compatibility states. |
| M0-VER-004 | PFS MUST classify changes by impact. |
| M0-VER-005 | PFS MUST support structured change requests. |
| M0-VER-006 | PFS MUST support change impact analysis. |
| M0-VER-007 | PFS MUST control approval and execution transitions. |
| M0-VER-008 | PFS MUST support migration planning and validation. |
| M0-VER-009 | PFS MUST preserve baseline history. |
| M0-VER-010 | PFS MUST support deprecation and retirement. |
| M0-VER-011 | PFS MUST record emergency changes. |
| M0-VER-012 | PFS MUST support dependency version pinning for reproducible operations. |
| M0-VER-013 | PFS MUST identify unknown compatibility rather than assuming compatibility. |
| M0-VER-014 | PFS MUST preserve source and target version context for migrations. |

## 16. M1 and M4 Design Dependencies

M1 phải định nghĩa:

- Version Metadata Schema.
- Compatibility Declaration.
- Dependency Registry.
- Change Request Contract.
- Change Impact Contract.
- Migration Plan Contract.
- Baseline Version Contract.
- Deprecation Policy.

M4 phải triển khai generation và migration operations theo các contracts đã được phê duyệt.

M3 phải kiểm tra compatibility, migration safety và baseline integrity.

---

**End of Document — PFS-M0-SPEC-011 v1.1.0**
