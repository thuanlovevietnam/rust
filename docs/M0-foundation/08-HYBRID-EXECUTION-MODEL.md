# PFS-M0-SPEC-008 — Hybrid Execution Model

**Document ID:** PFS-M0-SPEC-008  
**Document Type:** Hybrid Execution Architecture Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-001, PFS-M0-SPEC-002, PFS-M0-SPEC-004, PFS-M0-SPEC-005, PFS-M0-SPEC-006, PFS-M0-SPEC-007, PFS-M0-SPEC-009, PFS-M0-SPEC-010, PFS-M0-SPEC-011, PFS-M0-SPEC-012

---

## 1. Purpose

Tài liệu này định nghĩa mô hình thực thi Hybrid của PFS.

PFS kết hợp:

1. AI Reasoning.
2. Deterministic Automation.
3. Human Authority and Approval.
4. Validation and Evidence.

Mục tiêu là khai thác khả năng reasoning linh hoạt của AI mà vẫn giữ được tính xác định, an toàn, có kiểm soát và có thể kiểm chứng của các thao tác quan trọng.

## 2. Core Architecture Principle

**AI quyết định cách phân tích và đề xuất trong phạm vi nhiệm vụ; deterministic automation thực hiện các quy tắc có thể xác định; con người giữ authority đối với các quyết định cần phê duyệt; validation kiểm tra kết quả.**

Không thành phần nào được tự ý chiếm chức năng của thành phần khác.

## 3. Execution Domains

### 3.1. AI Reasoning Domain

AI phù hợp với:

- Natural-language understanding.
- Discovery.
- Requirements analysis.
- Semantic analysis.
- Architecture alternatives.
- Trade-off analysis.
- Draft generation.
- Conflict detection.
- Evidence interpretation.
- Recommendations.
- Multi-agent collaboration.

AI output là một kết quả reasoning, không mặc nhiên là một quyết định có hiệu lực.

### 3.2. Deterministic Automation Domain

Automation phù hợp với:

- Schema validation.
- ID validation.
- Metadata validation.
- File inventory.
- Reference validation.
- Manifest validation.
- Version checks.
- Hash computation.
- File generation theo manifest.
- Diff generation.
- Permission enforcement.
- Operation logging.
- Reproducibility checks.

Automation MUST có rules và inputs xác định đủ để kết quả có thể kiểm tra.

### 3.3. Human Authority Domain

Con người có thẩm quyền chịu trách nhiệm:

- Phê duyệt mục tiêu và scope.
- Phê duyệt quyết định thuộc authority.
- Chấp thuận exception.
- Cấp hoặc thu hồi quyền.
- Phê duyệt critical changes.
- Phê duyệt baseline.

Không yêu cầu người dùng phê duyệt từng thao tác kỹ thuật vô hại nếu policy cho phép thực hiện tự động.

### 3.4. Validation Domain

Validation có trách nhiệm:

- Kiểm tra output.
- So sánh với requirements.
- Kiểm tra consistency.
- Kiểm tra integrity.
- Xác minh operation results.
- Thu thập evidence.
- Báo cáo failure và uncertainty.

Validation có thể sử dụng cả deterministic checks và human/AI review, nhưng phải phân biệt phương pháp và mức độ tin cậy.

## 4. Logical Execution Flow

Mô hình tổng thể:

`Input → Context Resolution → Task Planning → Authority Check → AI Reasoning / Deterministic Processing → Review / Approval → Execution → Validation → Evidence → Audit`

Luồng thực tế có thể khác nhau theo task type.

Không phải mọi task đều cần AI.

Không phải mọi task đều cần human approval.

Không task nào được bỏ qua permission enforcement và các validation bắt buộc.

## 5. Task Classification

Mỗi task SHOULD được phân loại theo:

- Task Type.
- Required Capability.
- Risk.
- Data Classification.
- Required Authority.
- Required Permission.
- Reversibility.
- Validation Level.
- Expected Evidence.

Task types tham khảo:

| Task Type | Ví dụ | Execution Preference |
|---|---|---|
| Reasoning | Phân tích requirements | AI |
| Drafting | Viết tài liệu | AI |
| Structured Validation | Kiểm tra schema | Deterministic |
| Search and Retrieval | Tìm artifact | Deterministic hoặc connector |
| Decision Proposal | Đề xuất architecture | AI + review |
| Approval | Phê duyệt ADR | Human authority |
| Generation | Tạo file theo manifest | Deterministic |
| High-Risk Operation | Xóa hoặc ghi đè | Explicit authorization + controls |
| Audit | Kiểm tra độc lập | Independent validation |

## 6. AI Reasoning Contract

AI task phải có context và constraints phù hợp.

Một AI task SHOULD nhận:

- Task ID.
- Project ID.
- Objective.
- Task scope.
- Relevant artifact IDs and versions.
- Applicable policies.
- Permission context.
- Input data classification.
- Expected output format.
- Constraints.
- Verification expectations.

AI output SHOULD chứa:

- Result.
- Reasoning summary phù hợp với mục tiêu audit.
- Assumptions.
- Facts và sources.
- Uncertainties.
- Recommendations.
- Risks.
- Conflicts.
- Related artifact references.
- Validation needs.

Không yêu cầu lưu private chain-of-thought. Audit cần kết quả, căn cứ có thể kiểm tra, nguồn và các giả định liên quan, không cần lưu nội dung suy nghĩ nội bộ của model.

### 6.1. AI Output Classification

AI output phải được phân biệt:

- Draft.
- Analysis.
- Recommendation.
- Proposed Decision.
- Validation Observation.
- Approved Instruction khi có approval hợp lệ.

AI không được tự đánh dấu output của mình là Approved chỉ vì hoàn thành task.

## 7. Deterministic Automation Contract

Một automation task SHOULD có:

- Task ID.
- Operation ID.
- Input references.
- Input versions.
- Expected preconditions.
- Rule or operation definition.
- Permission context.
- Target scope.
- Expected result.
- Validation rules.
- Recovery strategy.
- Audit requirements.

Automation MUST:

- Kiểm tra preconditions.
- Kiểm tra permissions.
- Phát hiện conflicts.
- Thực hiện theo plan được phép.
- Ghi operation result.
- Validate output.
- Không mở rộng target scope ngoài plan.

### 7.1. Determinism

Cùng một operation, cùng input, cùng version của rules và cùng môi trường được kiểm soát SHOULD tạo ra kết quả tương đương.

Nếu operation phụ thuộc yếu tố không xác định, yếu tố đó phải được ghi nhận.

Không tuyên bố deterministic nếu kết quả thực tế phụ thuộc thời gian, mạng, provider hoặc dữ liệu ngoài chưa được cố định.

### 7.2. Idempotency

Các operations được thiết kế idempotent SHOULD cho kết quả an toàn khi chạy lại với cùng điều kiện.

Operation không idempotent phải ghi rõ side effects và cách xử lý retry.

## 8. AI Provider Independence

PFS MUST hỗ trợ nhiều AI providers thông qua adapter boundary.

Provider adapter chịu trách nhiệm:

- Connection.
- Authentication handling.
- Model selection.
- Request/response mapping.
- Capability declaration.
- Tool support mapping.
- Error normalization.
- Rate-limit handling.
- Data handling constraints.

Core PFS không được phụ thuộc trực tiếp vào proprietary provider-specific behavior.

### 8.1. Capability-Based Selection

PFS SHOULD lựa chọn provider dựa trên capability phù hợp với task:

- Reasoning.
- Structured output.
- Context capacity.
- Tool use.
- Multimodal input nếu cần.
- Latency.
- Cost.
- Privacy and data handling.
- Availability.

Không giả định một provider luôn tốt nhất cho mọi task.

### 8.2. Provider Failure

Khi provider lỗi:

- Ghi nhận lỗi.
- Không tự coi output chưa nhận được là thành công.
- Retry theo policy phù hợp.
- Có thể chuyển provider nếu policy cho phép.
- Giữ context và artifact versions.
- Kiểm tra lại output từ provider thay thế.

Không tự động chuyển dữ liệu Confidential hoặc Restricted sang provider khác nếu chưa được phép.

## 9. Multi-Agent Coordination

Multi-agent coordination có thể sử dụng:

- Coordinator.
- Specialist agents.
- Reviewer agents.
- Independent auditor agents.

Đây là các logical roles, không nhất thiết là các model riêng biệt.

### 9.1. Coordinator Responsibilities

- Phân rã task.
- Phân công workstream.
- Cung cấp context.
- Theo dõi dependencies.
- Tích hợp kết quả.
- Phát hiện conflicts.
- Tổng hợp recommendations.
- Escalate khi cần.

Coordinator không có authority phê duyệt thay Project Owner.

### 9.2. Specialist Agent Responsibilities

- Thực hiện domain task.
- Ghi assumptions.
- Cung cấp evidence.
- Tuân thủ scope.
- Báo cáo uncertainty.
- Không tự thay đổi scope.

### 9.3. Reviewer Responsibilities

- Đánh giá output theo criteria.
- Phát hiện lỗi.
- Yêu cầu bổ sung evidence.
- Báo cáo conflict.
- Không tự sửa approved artifacts ngoài quyền.

### 9.4. Agent Collaboration Contract

Các agents SHOULD trao đổi thông qua structured task/result records thay vì dựa hoàn toàn vào hội thoại không có định danh.

Một result record nên có:

- Agent ID.
- Task ID.
- Input references.
- Output references.
- Status.
- Assumptions.
- Evidence.
- Findings.
- Confidence hoặc uncertainty.
- Required follow-up.

## 10. Execution Permission Boundary

Hybrid execution MUST tuân thủ Agent Security Model.

Logical permission levels được đề xuất:

| Level | Permission | Mô tả |
|---|---|---|
| L0 | Read-only | Chỉ đọc dữ liệu được phép |
| L1 | Analyze / Propose | Phân tích và đề xuất |
| L2 | Draft Artifacts | Tạo bản nháp |
| L3 | Modify Authorized Files | Sửa các file được ủy quyền |
| L4 | Execute Approved Operations | Chạy script, test hoặc operation được phê duyệt |
| L5 | Privileged / Destructive | Thao tác đặc quyền hoặc phá hủy, cần authorization rõ ràng |

Permission thực tế còn phải giới hạn theo:

- Project.
- Resource.
- Operation.
- Environment.
- Session.
- Data classification.
- Time.
- Conditions.

Một level cao không tự động cấp quyền trên mọi resource.

## 11. Safe Execution Model

Trước một operation có khả năng thay đổi trạng thái, PFS SHOULD kiểm tra:

1. Task được xác định.
2. Actor có permission.
3. Target scope hợp lệ.
4. Input version hợp lệ.
5. Preconditions đạt.
6. Conflicts được kiểm tra.
7. Approval tồn tại nếu policy yêu cầu.
8. Operation plan được xác định.
9. Recovery strategy được xem xét.
10. Audit recording được bật.

### 11.1. Read-Only First

Với các task chưa rõ tác động, ưu tiên:

- Read.
- Analyze.
- Preview.
- Diff.
- Propose.

Chỉ chuyển sang write hoặc execute sau khi đáp ứng permission và approval conditions.

### 11.2. No Hidden Side Effects

AI reasoning task không được âm thầm thực hiện file changes hoặc external operations nếu task chỉ được giao phân tích.

Một task phải khai báo rõ khi có side effects.

## 12. Generation and Execution Separation

PFS MUST phân biệt:

- Plan Generation.
- Plan Validation.
- Plan Approval.
- Plan Execution.
- Result Verification.

AI có thể đề xuất generation plan.

Deterministic engine kiểm tra plan.

Authority phê duyệt nếu cần.

Engine thực thi theo plan được cho phép.

Validation kiểm tra kết quả.

Không cho phép AI vừa đề xuất vừa tự động phê duyệt một thao tác privileged chỉ bằng output của chính nó.

## 13. Retry and Recovery

Retry phải căn cứ vào operation semantics.

### Safe Retry

Có thể retry khi:

- Operation idempotent.
- Preconditions vẫn hợp lệ.
- Không có side effect chưa xác định.
- Permission còn hiệu lực.

### Conditional Retry

Cần kiểm tra lại state và impact trước khi retry.

### Prohibited Automatic Retry

Không tự retry đối với thao tác có thể gây side effect trùng lặp hoặc phá hủy nếu chưa xác định được trạng thái lần thực hiện trước.

Recovery phải theo Recovery Model ở các tài liệu sau, không tuyên bố rollback tuyệt đối cho mọi external operation.

## 14. Execution Observability

PFS SHOULD ghi nhận:

- Task start/end.
- Actor.
- Agent/provider nếu liên quan.
- Input references.
- Operation plan.
- Permission checks.
- Approval references.
- Output references.
- Error.
- Retry.
- Validation result.
- Recovery action.
- Final status.

Log phải tuân thủ data classification và không chứa secrets không cần thiết.

## 15. Validation and Evidence

Output cần được kiểm tra theo mức phù hợp:

- Syntax validation.
- Schema validation.
- Semantic review.
- Requirement coverage.
- Reference validation.
- Permission validation.
- Security review.
- Integration validation.
- Independent audit.

AI-generated output không được mặc nhiên coi là validated.

Deterministic checks cũng không chứng minh được những thuộc tính mà chúng không kiểm tra.

Evidence phải liên kết với input version và output version.

## 16. Failure Modes

| Failure | Required Handling |
|---|---|
| AI hallucination | Kiểm tra sources và validation |
| Provider timeout | Retry hoặc fallback theo policy |
| Conflicting agent output | Conflict record và authority escalation |
| Invalid structured output | Reject hoặc request correction |
| Unauthorized operation | Block và audit |
| Stale input | Revalidate dependency |
| Partial file generation | Detect và recovery |
| Missing evidence | Không đạt acceptance |
| Unexpected side effect | Containment và incident review |
| Permission revoked | Dừng action chưa được phép tiếp tục |

## 17. Hybrid Execution Invariants

1. AI output không tự trở thành approved decision.
2. Automation không tự tạo authority.
3. Provider adapter không được vượt policy của PFS.
4. Permission phải được kiểm tra trước action.
5. Side effects phải được khai báo và kiểm soát.
6. Input và output versions phải truy vết được.
7. Critical outputs phải có validation evidence.
8. Retry phải phù hợp với operation semantics.
9. Multi-agent consensus không thay thế owner approval.
10. Security và data classification phải được áp dụng xuyên suốt execution.

## 18. Requirements

| ID | Requirement |
|---|---|
| M0-HYB-001 | PFS MUST kết hợp AI reasoning và deterministic automation. |
| M0-HYB-002 | PFS MUST phân biệt AI proposal với approved instruction. |
| M0-HYB-003 | PFS MUST có provider adapter boundary. |
| M0-HYB-004 | PFS MUST hỗ trợ capability-based provider selection. |
| M0-HYB-005 | PFS MUST có structured task/result contracts. |
| M0-HYB-006 | PFS MUST kiểm tra permission trước operation. |
| M0-HYB-007 | PFS MUST tách plan, validation, approval, execution và verification. |
| M0-HYB-008 | PFS MUST ghi nhận side effects và operation results. |
| M0-HYB-009 | PFS MUST hỗ trợ safe retry và recovery policy. |
| M0-HYB-010 | PFS MUST duy trì traceability giữa inputs và outputs. |
| M0-HYB-011 | PFS MUST NOT để provider-specific behavior phá vỡ governance. |
| M0-HYB-012 | PFS MUST NOT cho phép agent tự phê duyệt thao tác vượt quyền. |
| M0-HYB-013 | Critical outputs MUST có validation evidence phù hợp. |
| M0-HYB-014 | PFS MUST hỗ trợ conflict reporting giữa agents. |

## 19. M1 Design Dependencies

M1 phải thiết kế:

- Task Contract.
- Agent Result Contract.
- Provider Adapter Contract.
- Capability Registry.
- Execution Plan Contract.
- Permission Check Contract.
- Approval Gate Contract.
- Operation Record.
- Retry Policy.
- Recovery Contract.
- Evidence Contract.
- Multi-Agent Coordination Protocol.

M2 sẽ xây dựng Agent Foundation dựa trên các contracts được M1 xác định.

M4 sẽ hiện thực hóa deterministic generator và CLI theo các quy tắc đã được phê duyệt.

---

**End of Document — PFS-M0-SPEC-008 v1.1.0**
