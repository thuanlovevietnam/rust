# PFS-M0-SPEC-006 — Authority and Decision Model

**Document ID:** PFS-M0-SPEC-006  
**Document Type:** Authority and Decision Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-003, PFS-M0-SPEC-004, PFS-M0-SPEC-005, PFS-M0-SPEC-007, PFS-M0-SPEC-009, PFS-M0-SPEC-011

---

## 1. Purpose

Tài liệu này định nghĩa cách PFS xác định:

- Ai có quyền quyết định.
- Ai có quyền đề xuất.
- Ai có quyền phê duyệt.
- Ai được phép thực thi.
- Ai có quyền xác minh.
- Cách giải quyết xung đột giữa các quyết định và tài liệu.
- Cách xử lý nhiều AI agents có kết luận khác nhau.

Mục tiêu là tránh tình trạng AI, tài liệu hoặc automation tự trở thành authority chỉ vì chúng được tạo ra trước hoặc xuất hiện ở vị trí có vẻ quan trọng.

## 2. Fundamental Authority Principles

### 2.1. Authority Comes from Explicit Delegation

Quyền phải đến từ Project Owner hoặc một authority được ủy quyền hợp lệ.

Quyền không phát sinh chỉ vì:

- Một agent có model mạnh hơn.
- Một tài liệu được tạo gần đây hơn.
- Một file nằm trong thư mục có vẻ quan trọng hơn.
- Một người đã thực hiện nhiều công việc.
- Một kết quả có nhiều agent đồng ý.

### 2.2. Domain-Specific Authority

Authority được xác định theo domain và loại quyết định.

Một người có thể có quyền quyết định architecture nhưng không có quyền phê duyệt ngân sách hoặc legal obligations.

### 2.3. Proposal Is Not Approval

Proposal, recommendation, consensus và approval là các trạng thái khác nhau.

### 2.4. Execution Is Not Decision Authority

Có quyền thực thi một tác vụ không đồng nghĩa với quyền thay đổi policy hoặc quyết định nền tảng.

### 2.5. Verification Is Not Approval

Người xác minh có thể xác nhận kết quả đạt tiêu chí, nhưng không mặc nhiên có quyền chấp thuận toàn bộ dự án.

## 3. Authority Model

Mỗi authority grant phải có:

- Principal.
- Role.
- Domain.
- Decision type.
- Resource scope.
- Permission.
- Conditions.
- Delegator.
- Validity.
- Revocation status.

Một authority grant chỉ hợp lệ khi:

1. Người cấp có quyền cấp.
2. Scope rõ ràng.
3. Permission cụ thể.
4. Chưa hết hiệu lực.
5. Chưa bị thu hồi.
6. Không vi phạm higher-level governance constraints.

Authority không được kế thừa ngầm chỉ từ tên role.

## 4. Decision Domains

Các domain điển hình:

- Project Objectives.
- Scope.
- Requirements.
- Product.
- Architecture.
- Security.
- Data.
- Technology.
- Budget and Resources.
- Operations.
- Compliance.
- Agent Policy.
- Quality.
- Baseline and Release.

Project Owner có thể ủy quyền một phần authority theo domain.

Các quyết định liên domain phải xác định tất cả approval cần thiết hoặc một authority được ủy quyền có phạm vi bao phủ rõ ràng.

## 5. Decision Lifecycle

Một decision có lifecycle:

1. Proposed.
2. Under Review.
3. Changes Requested.
4. Approved hoặc Rejected.
5. Superseded hoặc Withdrawn khi có lý do hợp lệ.

Sau khi được Approved, decision có thể được thực thi hoặc dùng làm cơ sở cho artifact khác.

Việc thực thi phải có execution permission riêng nếu thao tác cần quyền.

### 5.1. Proposed

Đã được đề xuất nhưng chưa được phê duyệt.

### 5.2. Under Review

Đang được authority hoặc reviewer đánh giá.

### 5.3. Changes Requested

Cần bổ sung thông tin hoặc sửa đổi trước khi quyết định.

### 5.4. Approved

Đã được authority phù hợp phê duyệt.

### 5.5. Rejected

Bị authority từ chối. Phải giữ lại lý do và history.

### 5.6. Superseded

Được thay thế bởi decision mới. Decision cũ vẫn được giữ để truy vết lịch sử.

### 5.7. Withdrawn

Người đề xuất rút proposal trước khi được phê duyệt, hoặc authority cho phép rút theo policy.

Không được xóa decision đã tồn tại để thay bằng nội dung mới mà không giữ history.

## 6. Decision Record

Mỗi decision quan trọng SHOULD được ghi thành Decision Record.

Các trường tối thiểu:

- Decision ID.
- Title.
- Domain.
- Status.
- Context.
- Problem statement.
- Requirements affected.
- Options considered.
- Selected option.
- Rationale.
- Evidence.
- Assumptions.
- Risks.
- Consequences.
- Rejected alternatives.
- Proposed by.
- Reviewed by.
- Approved by.
- Approval timestamp.
- Effective version.
- Supersedes / Superseded by.
- Review trigger.

Một decision chưa approved phải hiển thị rõ là proposal.

## 7. Authority Matrix

Ma trận dưới đây là baseline logic; quyền thực tế phải được cấu hình theo từng Project Profile và delegation.

| Action | Project Owner | Decision Approver | Architect | Reviewer | Operator | AI Agent |
|---|---|---|---|---|---|---|
| Đề xuất thay đổi | Yes | Yes | Yes | Yes | Yes | Yes |
| Phân tích tác động | Yes | Yes | Yes | Yes | Yes | Yes |
| Phê duyệt theo domain | Yes, within authority | Within delegation | Only if delegated | Only if delegated | No by default | No |
| Thực thi thao tác | If permitted | If permitted | If permitted | If permitted | Within scope | Within scope |
| Xác minh kết quả | Yes | Yes | Yes | Yes | If assigned | If assigned |
| Phê duyệt baseline | Yes | Only if delegated | No by default | No by default | No | No |
| Thay đổi authority policy | Yes | Only if delegated | No by default | No | No | No |

`Yes` không đồng nghĩa với quyền vô hạn. Mọi quyền đều bị giới hạn bởi domain, scope, conditions và higher-level policies.

## 8. Source of Truth and Authority Resolution

PFS không sử dụng một thứ tự ưu tiên đơn giản như:

- File mới nhất thắng.
- File ở thư mục cao nhất thắng.
- ADR luôn thắng SPEC.
- Người sửa cuối cùng thắng.

Thay vào đó, authority được xác định theo các chiều:

1. Domain.
2. Artifact type.
3. Owner hoặc approver được chỉ định.
4. Approval status.
5. Scope.
6. Effective version.
7. Supersession relationship.

### 8.1. Authoritative Artifact

Một artifact chỉ có thể được coi là authoritative trong phạm vi xác định khi:

- Đúng artifact type.
- Có authority được xác định.
- Đã được phê duyệt nếu nội dung yêu cầu approval.
- Có version và effective scope.
- Chưa bị superseded.
- Không có xung đột chưa giải quyết làm vô hiệu hóa việc áp dụng.

### 8.2. Conflict Conditions

Conflict có thể xuất hiện khi:

- Hai approved decisions đưa ra yêu cầu không tương thích.
- Một SPEC mâu thuẫn với một ADR.
- Requirement mâu thuẫn với architecture.
- Một policy cho phép hành động mà security rule cấm.
- Artifact mới thay đổi nội dung đã được approval.
- Hai authorities cùng tuyên bố có quyền quyết định một vấn đề.
- Agent tạo output không phù hợp với approved source.

## 9. Conflict Resolution Procedure

Khi phát hiện conflict:

### Step 1 — Detect

Ghi nhận hai hoặc nhiều nội dung mâu thuẫn.

### Step 2 — Preserve

Giữ nguyên các artifact và evidence liên quan.

### Step 3 — Classify

Xác định:

- Domain.
- Conflict type.
- Severity.
- Affected scope.
- Related decisions.
- Related requirements.

### Step 4 — Contain

Dừng hoặc hạn chế các task phụ thuộc vào conflict nếu tiếp tục có thể tạo ra thay đổi sai hoặc rủi ro.

### Step 5 — Identify Authority

Xác định người có quyền giải quyết theo domain và delegation.

### Step 6 — Analyze

Đánh giá tác động đến:

- Project objectives.
- Requirements.
- Architecture.
- Security.
- Data.
- Interfaces.
- Operations.
- Existing artifacts.
- Baseline compatibility.

### Step 7 — Propose Resolution

Đưa ra các phương án, rationale, trade-offs và evidence.

### Step 8 — Approve

Authority phù hợp phê duyệt phương án.

### Step 9 — Update

Cập nhật các artifacts liên quan và traceability.

### Step 10 — Verify

Kiểm tra các conflict đã được giải quyết và các dependency đã được cập nhật.

Không được tự chọn phương án chỉ vì nó ít thay đổi file hơn.

## 10. Multi-Agent Decision Conflict

Khi nhiều agents đưa ra kết luận khác nhau:

- Ghi nhận từng kết luận.
- Ghi nhận model/provider và task context phù hợp với audit requirements.
- Ghi rõ assumptions.
- Phân biệt evidence với suy luận.
- Xác định các phần đồng thuận và bất đồng.
- Đánh giá phương pháp và chất lượng evidence.
- Yêu cầu bổ sung phân tích khi cần.
- Escalate nếu ảnh hưởng đến quyết định cần authority.

### 10.1. Consensus Rule

Consensus có thể tăng confidence, nhưng không tạo ra authority.

Ngay cả khi mọi agent đồng ý, một quyết định cần Project Owner approval vẫn phải được phê duyệt.

### 10.2. Model Ranking Rule

Không tự động chọn kết luận từ model có benchmark cao hơn.

Đánh giá phải căn cứ vào task-specific evidence, reasoning, assumptions, source quality và verification.

### 10.3. Unresolved Disagreement

Nếu không thể giải quyết:

- Giữ nguyên các quan điểm.
- Ghi nhận uncertainty.
- Đánh giá risk.
- Chặn các hành động phụ thuộc khi cần.
- Escalate đến authority.

## 11. Emergency and Incident Authority

PFS có thể cần hành động containment khẩn cấp để ngăn thiệt hại.

Một emergency action chỉ được phép khi policy đã phê duyệt định nghĩa rõ:

- Trigger.
- Authorized principal.
- Allowed action.
- Scope.
- Duration.
- Logging.
- Notification.
- Post-action review.

AI Agent không được tự tuyên bố emergency để mở rộng quyền.

Emergency containment không đồng nghĩa với quyền đưa ra quyết định chiến lược hoặc phê duyệt thay đổi dài hạn.

## 12. Delegation and Revocation

Delegation phải ghi:

- Grant ID.
- Delegator.
- Delegate.
- Domain.
- Scope.
- Allowed decision types.
- Conditions.
- Start and expiry.
- Revocation status.

Khi thu hồi:

- Quyền mới không được tiếp tục cấp theo grant cũ.
- Các task đang thực hiện phải được đánh giá.
- Approval đã cấp phải được đánh giá theo policy và effective time.
- Audit trail phải được giữ lại.

## 13. Decision Immutability and Evolution

Decision đã được phê duyệt không được âm thầm sửa nội dung.

Khi cần thay đổi:

1. Tạo decision revision hoặc decision mới.
2. Liên kết decision cũ.
3. Ghi rationale.
4. Đánh giá impact.
5. Thực hiện approval cần thiết.
6. Đánh dấu decision cũ Superseded khi phù hợp.
7. Cập nhật các artifacts phụ thuộc.

Immutability ở đây có nghĩa lịch sử và approval phải truy vết được, không có nghĩa nội dung không bao giờ được thay đổi.

## 14. Authority Requirements

| ID | Requirement |
|---|---|
| M0-AUT-001 | Mọi authority MUST có nguồn cấp hợp lệ. |
| M0-AUT-002 | Authority MUST có domain và scope. |
| M0-AUT-003 | Proposal MUST được phân biệt với Approved Decision. |
| M0-AUT-004 | Execution permission MUST độc lập với decision authority. |
| M0-AUT-005 | Decision quan trọng MUST có Decision Record. |
| M0-AUT-006 | Source-of-truth conflicts MUST được giải quyết theo authority model. |
| M0-AUT-007 | Multi-agent consensus MUST NOT thay thế approval. |
| M0-AUT-008 | Unresolved critical conflicts MUST chặn các task phụ thuộc. |
| M0-AUT-009 | Delegation MUST có scope, conditions và revocation mechanism. |
| M0-AUT-010 | Approved decisions MUST giữ history khi bị thay thế. |
| M0-AUT-011 | Emergency authority MUST được định nghĩa trước bằng policy. |
| M0-AUT-012 | AI MUST NOT tự cấp hoặc tự mở rộng authority. |

## 15. M1 Design Dependencies

M1 phải thiết kế:

- Authority Grant Schema.
- Decision Record Schema.
- Approval Contract.
- Delegation and Revocation Contract.
- Conflict Record Schema.
- Multi-Agent Disagreement Report.
- Decision Supersession Model.
- Authority Resolution Algorithm.
- Emergency Action Contract.

---

**End of Document — PFS-M0-SPEC-006 v1.1.0**
