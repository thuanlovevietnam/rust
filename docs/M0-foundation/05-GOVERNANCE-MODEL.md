# PFS-M0-SPEC-005 — Governance Model

**Document ID:** PFS-M0-SPEC-005  
**Document Type:** Governance Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-004, PFS-M0-SPEC-006, PFS-M0-SPEC-007, PFS-M0-SPEC-009, PFS-M0-SPEC-010, PFS-M0-SPEC-011, PFS-M0-SPEC-012

---

## 1. Purpose

Tài liệu này xác định mô hình governance áp dụng cho PFS và các Project Foundation được PFS quản lý.

Governance đảm bảo:

- Có người chịu trách nhiệm.
- Có quyền quyết định rõ ràng.
- Có giới hạn thực thi.
- Có quy trình phê duyệt.
- Có lịch sử và auditability.
- Có cơ chế xử lý bất đồng.
- Có kiểm soát thay đổi.
- Có quản lý rủi ro và ngoại lệ.

Governance là một cross-cutting concern, áp dụng xuyên suốt lifecycle, không chỉ là một stage riêng.

## 2. Governance Principles

### 2.1. Explicit Accountability

Mỗi quyết định và hoạt động quan trọng phải có trách nhiệm rõ ràng.

### 2.2. Separation of Duties

Đề xuất, phê duyệt, thực thi và xác minh là các chức năng khác nhau về mặt logic.

Trong dự án nhỏ, một người có thể đảm nhiệm nhiều vai trò nếu policy cho phép, nhưng phải ghi nhận rõ và áp dụng kiểm soát bù trừ cho thao tác có rủi ro cao.

### 2.3. Least Authority

Chỉ cấp quyền cần thiết cho nhiệm vụ cụ thể.

### 2.4. Traceable Decisions

Quyết định quan trọng phải có nguồn, rationale, authority và trạng thái.

### 2.5. Risk-Proportionate Governance

Kiểm soát phải tương xứng với impact, likelihood, reversibility và data sensitivity.

### 2.6. No Implicit Approval

Im lặng, hết thời gian chờ hoặc agent báo hoàn tất không đồng nghĩa với approval, trừ khi một policy được Project Owner phê duyệt quy định rõ điều đó cho một thao tác cụ thể.

### 2.7. Independent Verification

Đối với critical changes, người hoặc cơ chế kiểm tra phải có tính độc lập phù hợp với mức độ rủi ro.

## 3. Governance Scope

Governance bao gồm:

1. Project ownership.
2. Role assignment.
3. Decision authority.
4. Approval.
5. Agent execution permissions.
6. Resource ownership.
7. Artifact lifecycle.
8. Change management.
9. Exception management.
10. Risk management.
11. Audit.
12. Conflict resolution.
13. Baseline approval.

## 4. Governance Domains

Các domain governance được tổ chức như sau:

| Domain | Phạm vi |
|---|---|
| Project Governance | Mục tiêu, scope, ownership |
| Requirements Governance | Yêu cầu, priority, acceptance |
| Architecture Governance | Kiến trúc, constraints, ADR |
| Data Governance | Ownership, classification, integrity |
| Security Governance | Trust, access, security decisions |
| Agent Governance | Agent roles, permissions, execution |
| Documentation Governance | Authority, version, status |
| Quality Governance | Validation, exceptions, acceptance |
| Change Governance | Impact, approval, migration |
| Operational Governance | Operation, recovery, audit |

Một quyết định có thể ảnh hưởng nhiều domain. Khi đó phải xác định các authority liên quan và cách phối hợp.

## 5. Governance Roles

### 5.1. Project Owner

Chịu trách nhiệm cuối cùng đối với dự án trong phạm vi quyền sở hữu.

Quyền và trách nhiệm:

- Xác định hoặc phê duyệt mục tiêu.
- Phê duyệt scope quan trọng.
- Chỉ định người có thẩm quyền.
- Phê duyệt các quyết định thuộc quyền owner.
- Chấp thuận các exception thuộc quyền owner.
- Phê duyệt baseline.
- Quyết định tiếp tục, tạm dừng hoặc kết thúc dự án.

Project Owner không nhất thiết phải trực tiếp thực hiện mọi công việc.

### 5.2. Decision Approver

Người được Project Owner hoặc governance policy ủy quyền phê duyệt một domain hoặc loại quyết định cụ thể.

Ủy quyền phải xác định:

- Domain.
- Decision type.
- Scope.
- Limitations.
- Validity period.
- Revocation condition.

Không được hiểu ủy quyền một quyết định là ủy quyền toàn bộ quyền sở hữu dự án.

### 5.3. Project Architect

Chịu trách nhiệm đề xuất và đánh giá architecture.

Có thể:

- Đề xuất architecture.
- Tạo ADR.
- Đánh giá trade-offs.
- Phát hiện architecture conflicts.
- Xác định technical risks.

Không tự động có quyền phê duyệt các quyết định nằm ngoài authority được giao.

### 5.4. Security Reviewer

Đánh giá security, trust boundaries, data protection và permission risks.

Có thể đưa ra security findings và yêu cầu xử lý theo policy.

Không tự ý bỏ qua authority hoặc legal obligations.

### 5.5. Operator

Thực hiện các thao tác vận hành được cấp quyền.

Operator phải tuân thủ execution scope và ghi nhận kết quả.

### 5.6. AI Agent

Thực hiện nhiệm vụ theo role, policy và permission.

AI Agent không mặc nhiên có quyền:

- Phê duyệt chính output của mình.
- Tự mở rộng quyền.
- Thay đổi project scope.
- Thay đổi approved architecture.
- Xóa audit history.
- Tự miễn trừ validation.

### 5.7. Independent Auditor

Đánh giá độc lập tính đầy đủ, consistency và evidence.

Auditor phải ghi nhận findings trung thực và không được tự phê duyệt thay owner.

### 5.8. Observer

Có quyền xem những nội dung được phép, không có quyền thay đổi nếu không được cấp quyền bổ sung.

## 6. Role Assignment and Separation

Một user có thể đảm nhiệm nhiều roles, nhưng mỗi action phải được kiểm tra theo role và permission tương ứng.

Các kiểm soát:

- Không dùng role name làm bằng chứng duy nhất về quyền.
- Phải kiểm tra scope và permission cụ thể.
- Delegation phải có thời hạn hoặc điều kiện hiệu lực.
- Revoked authority không được tiếp tục sử dụng.
- Approval phải gắn với đúng decision version.
- Agent không được tự gán role cho chính nó.

Đối với các thao tác critical, SHOULD áp dụng separation giữa người đề xuất, người phê duyệt và người kiểm tra.

Nếu không thể tách vai trò, phải có compensating control được phê duyệt.

## 7. Governance Control Lifecycle

Một governance-controlled action đi qua các bước:

1. Initiation.
2. Classification.
3. Authority Check.
4. Risk Assessment.
5. Proposal hoặc Plan.
6. Review.
7. Approval nếu cần.
8. Execution.
9. Verification.
10. Audit Recording.
11. Closure.

Không phải mọi hành động đều cần approval riêng. Tuy nhiên, action phải tuân thủ policy đã được phê duyệt và không được vượt quyền.

## 8. Approval Model

Approval phải xác định:

- Decision hoặc action được phê duyệt.
- Người phê duyệt.
- Authority basis.
- Scope.
- Artifact version hoặc plan hash nếu có.
- Conditions.
- Timestamp.
- Expiration nếu có.
- Related evidence.

Approval chỉ có hiệu lực với nội dung và phạm vi được phê duyệt.

Nếu nội dung thay đổi đáng kể sau approval, phải đánh giá lại và có thể yêu cầu approval mới.

## 9. Risk-Based Governance

Governance phải đánh giá rủi ro theo:

- Impact.
- Likelihood.
- Data sensitivity.
- Reversibility.
- Scope of change.
- External exposure.
- Security implications.
- Legal or contractual implications.

Các mức risk tham khảo:

- Low.
- Medium.
- High.
- Critical.

Không dùng risk rating để tự động miễn trừ yêu cầu approval khi authority policy yêu cầu approval.

Một risk chưa có dữ liệu không được mặc định là Low.

## 10. Change Governance

Mọi thay đổi có ảnh hưởng đáng kể đến project foundation phải có:

- Change request hoặc change record.
- Source.
- Reason.
- Affected artifacts.
- Impact assessment.
- Compatibility assessment.
- Risk assessment.
- Required approvals.
- Validation plan.
- Execution result.
- Updated traceability.

Không được sửa approved artifacts mà không để lại lịch sử.

## 11. Exception Governance

Exception là sự cho phép có kiểm soát để không tuân thủ một rule hoặc requirement trong phạm vi xác định.

Một exception MUST có:

- Exception ID.
- Rule hoặc requirement bị ảnh hưởng.
- Reason.
- Scope.
- Risk.
- Impact.
- Mitigation.
- Compensating controls.
- Approver.
- Start date.
- Expiration hoặc review date.
- Closure condition.

### 11.1. Exception Restrictions

Exception MUST NOT:

- Hợp thức hóa hành vi trái pháp luật.
- Vô hiệu hóa nghĩa vụ pháp lý.
- Cho phép agent tự cấp quyền.
- Xóa audit history.
- Che giấu critical failure.
- Vượt authority của người phê duyệt.

Exception không được trở thành cách thay thế cho việc sửa một thiết kế sai có tính hệ thống.

## 12. Governance Escalation

Escalation bắt buộc khi:

- Có authority conflict.
- Có critical requirement conflict.
- Có security concern nghiêm trọng.
- Có nghi ngờ data exposure.
- Agent vượt quyền.
- Approval không hợp lệ.
- Có destructive action ngoài kế hoạch.
- Không thể xác minh kết quả quan trọng.
- Nhiều agents không thể giải quyết bất đồng bằng evidence.

Escalation record phải ghi:

- Trigger.
- Affected scope.
- Evidence.
- Immediate containment.
- Decision needed.
- Responsible authority.
- Resolution.

## 13. Governance Audit Trail

PFS MUST hỗ trợ ghi nhận các sự kiện governance quan trọng:

- Role assignment.
- Delegation.
- Permission changes.
- Approval.
- Rejection.
- Revocation.
- Exception.
- Critical change.
- Agent execution.
- Security finding.
- Audit finding.
- Baseline approval.

Audit record phải có identity, timestamp, actor, action, target và kết quả phù hợp.

Không được để agent tự xóa hoặc sửa lịch sử audit mà nó đang bị đánh giá.

## 14. Governance Independence

Governance policy phải độc lập với AI provider.

Việc thay model hoặc provider không được làm thay đổi:

- Project Owner authority.
- Approval requirements.
- Permission boundaries.
- Audit obligations.
- Exception rules.

Provider-specific capability chỉ được sử dụng trong giới hạn adapter và execution policy.

## 15. Governance Failure Handling

Khi phát hiện vi phạm governance:

1. Dừng hoặc hạn chế hành động liên quan nếu cần.
2. Bảo toàn evidence.
3. Xác định affected scope.
4. Thu hồi quyền nếu có rủi ro tiếp diễn.
5. Ghi incident hoặc finding.
6. Đánh giá tác động.
7. Thực hiện remediation được phê duyệt.
8. Kiểm tra độc lập khi cần.
9. Ghi nhận closure.

Không được xóa lịch sử để làm cho hệ thống có vẻ hợp lệ.

## 16. Governance Requirements

| ID | Requirement |
|---|---|
| M0-GOV-001 | PFS MUST có governance model xuyên suốt lifecycle. |
| M0-GOV-002 | PFS MUST xác định Project Owner hoặc ghi nhận trạng thái chưa có owner. |
| M0-GOV-003 | PFS MUST phân biệt proposal, approval, execution và verification. |
| M0-GOV-004 | PFS MUST hỗ trợ delegated authority có scope. |
| M0-GOV-005 | Approval MUST gắn với đúng decision hoặc artifact version. |
| M0-GOV-006 | PFS MUST có risk-based governance. |
| M0-GOV-007 | PFS MUST có exception process có thời hạn hoặc review condition. |
| M0-GOV-008 | PFS MUST có escalation path. |
| M0-GOV-009 | PFS MUST duy trì audit trail cho governance-critical actions. |
| M0-GOV-010 | PFS MUST NOT cho phép AI tự phê duyệt hoặc tự mở rộng authority. |
| M0-GOV-011 | PFS MUST hỗ trợ separation of duties hoặc compensating controls. |
| M0-GOV-012 | Governance MUST độc lập với AI provider. |

## 17. M1 Design Dependencies

M1 cần thiết kế chi tiết:

- Role schema.
- Authority grant schema.
- Delegation schema.
- Approval record.
- Exception record.
- Governance event model.
- Audit record contract.
- Escalation workflow.
- Separation-of-duties rules.
- Governance policy evaluation.

---

**End of Document — PFS-M0-SPEC-005 v1.1.0**
