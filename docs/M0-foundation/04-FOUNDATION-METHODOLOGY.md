# PFS-M0-SPEC-004 — Foundation Methodology

**Document ID:** PFS-M0-SPEC-004  
**Document Type:** Methodology Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-001, PFS-M0-SPEC-002, PFS-M0-SPEC-003, PFS-M0-SPEC-005, PFS-M0-SPEC-006, PFS-M0-SPEC-007, PFS-M0-SPEC-010, PFS-M0-SPEC-013

---

## 1. Purpose

Tài liệu này định nghĩa phương pháp chuẩn để PFS xây dựng Project Foundation từ một ý tưởng, yêu cầu ban đầu hoặc một dự án đã tồn tại.

Methodology phải đảm bảo:

- Hiểu đúng vấn đề trước khi thiết kế giải pháp.
- Thu thập và xác minh bối cảnh.
- Xây dựng requirements có thể kiểm chứng.
- Thiết kế architecture phù hợp.
- Thiết lập governance và authority.
- Tạo documentation và agent foundation.
- Xác lập quality gates.
- Bootstrap và kiểm chứng kết quả.
- Đánh giá độc lập trước khi phê duyệt baseline.

Methodology không phải một chuỗi thao tác máy móc áp dụng giống nhau cho mọi dự án. Đây là một framework có tailoring, có điều kiện chuyển giai đoạn và có cơ chế quay lại khi phát hiện vấn đề.

## 2. Methodology Design Principles

### 2.1. Understand Before Design

Không lựa chọn architecture, technology hoặc automation trước khi hiểu mục tiêu, bối cảnh và constraints.

### 2.2. Requirements Before Implementation

Các yêu cầu có ảnh hưởng lớn đến kiến trúc, bảo mật, dữ liệu và vận hành phải được xác định trước khi triển khai tương ứng.

### 2.3. Progressive Elaboration

Thông tin được hoàn thiện theo từng bước. Không bắt buộc giải quyết mọi chi tiết ngay từ đầu, nhưng phải ghi nhận những gì chưa biết.

### 2.4. Evidence-Based Decisions

Các quyết định quan trọng phải có rationale, evidence hoặc ghi rõ assumptions và uncertainty.

### 2.5. Tailored Process

Mức độ chi tiết, deliverables và verification phụ thuộc Project Profile, complexity, risk và capability applicability.

### 2.6. Controlled Transitions

Không chuyển giai đoạn chỉ vì đã tạo đủ file. Phải đáp ứng entry/exit conditions tương ứng.

### 2.7. Reversible Where Practical

Ưu tiên phương án có thể kiểm tra, phục hồi hoặc điều chỉnh khi uncertainty còn cao. Những thay đổi khó đảo ngược phải có đánh giá rủi ro và approval phù hợp.

## 3. Foundation Lifecycle

PFS sử dụng lifecycle gồm 11 stage.

`Initialize → Discover → Requirements → Architecture → Governance → Documentation → Agents → Quality → Bootstrap → Audit → Baseline`

Đây là mô hình tổng thể. Một dự án có thể lặp lại stage hoặc thực hiện một số hoạt động song song khi dependency cho phép.

Không được hiểu việc song song hóa là bỏ qua dependency hoặc approval.

## 4. Stage 1 — Initialize Project

### Objective

Tạo project identity và xác định cơ sở để bắt đầu.

### Activities

- Tiếp nhận project brief.
- Xác định người khởi tạo.
- Xác định Project Owner hoặc ghi nhận chưa được chỉ định.
- Đặt tên và tạo Project ID.
- Ghi nhận mục tiêu ban đầu.
- Xác định phạm vi sơ bộ.
- Ghi nhận nguồn đầu vào.
- Xác định mức độ nhạy cảm ban đầu của dữ liệu.
- Khởi tạo Project Profile.

### Deliverables

- Initial Project Profile.
- Project Brief.
- Initial Stakeholder Register.
- Initial Assumptions and Constraints.
- Initial Risk Notes.

### Exit Conditions

- Project identity được xác định.
- Có mục tiêu sơ bộ.
- Có authority tiếp nhận hoặc trạng thái owner được ghi rõ.
- Các thông tin chưa biết được đánh dấu.
- Không có việc tự động phê duyệt mục tiêu hoặc scope chỉ từ nội dung AI tạo.

## 5. Stage 2 — Discover Context

### Objective

Hiểu bối cảnh thực tế trước khi định nghĩa giải pháp.

### Activities

- Thu thập tài liệu và thông tin liên quan.
- Phỏng vấn hoặc đặt câu hỏi làm rõ.
- Xác định stakeholders.
- Xác định hiện trạng.
- Phân tích môi trường.
- Xác định dependencies.
- Xác định constraints.
- Phân loại fact, assumption, inference và unknown.
- Xác định các nguồn thông tin có thẩm quyền.

### Deliverables

- Context Description.
- Stakeholder Map.
- Existing-State Assessment nếu có.
- Assumptions Register.
- Constraints Register.
- Dependency Register.
- Discovery Findings.

### Exit Conditions

- Bối cảnh đủ để bắt đầu requirements engineering.
- Critical unknowns được ghi nhận và có kế hoạch xử lý.
- Các nguồn thông tin quan trọng có provenance.
- Không trình bày thông tin chưa xác minh như sự thật.

## 6. Stage 3 — Requirements Engineering

### Objective

Chuyển mục tiêu và nhu cầu thành requirements có thể đánh giá và kiểm chứng.

### Activities

1. Xác định business hoặc project objectives.
2. Xác định outcomes.
3. Phân rã scope.
4. Thu thập requirements.
5. Phân loại requirements.
6. Xác định priority và criticality.
7. Phát hiện ambiguity.
8. Phát hiện contradiction.
9. Xác định dependencies.
10. Xây dựng acceptance criteria.
11. Xác định verification methods.
12. Trình requirements để authority phù hợp xem xét.

### Requirement Classes

Tùy loại dự án, có thể gồm:

- Functional.
- Non-functional.
- Business.
- Operational.
- Security.
- Data.
- Interface.
- Compliance.
- Quality.
- Governance.
- Constraint.

Không bắt buộc mọi project phải sử dụng toàn bộ các lớp này.

### Deliverables

- Requirements Specification.
- Requirements Register.
- Assumptions and Constraints Register.
- Requirements Traceability.
- Acceptance Criteria.
- Open Issues Register.

### Exit Conditions

- Critical requirements có ID.
- Critical requirements có owner hoặc authority.
- Requirements có verification method.
- Ambiguity và conflicts quan trọng được giải quyết hoặc có disposition được phê duyệt.
- Các requirements cần phê duyệt đã có trạng thái rõ ràng.

## 7. Stage 4 — Architecture Design

### Objective

Xác định cấu trúc và cách thức hoạt động phù hợp với requirements.

### Activities

- Xác định architecture concerns.
- Đánh giá applicability của Architecture Views.
- Đề xuất architecture options.
- Phân tích trade-offs.
- Đánh giá security và trust boundaries.
- Đánh giá data ownership và integrity.
- Đánh giá interfaces và dependencies.
- Đánh giá deployment và operations nếu áp dụng.
- Ghi lại quyết định kiến trúc.
- Xác định vấn đề còn mở.

### Architecture Views

Tham chiếu `PFS-M0-SPEC-003`:

- Context.
- Structure.
- Behavior.
- Data.
- Security.
- Interface.
- Deployment.
- Operations.

### Deliverables

- Architecture Description.
- Architecture Decision Records.
- Architecture Risks.
- Interface Contracts nếu phù hợp.
- Architecture Traceability.
- Open Architecture Issues.

### Exit Conditions

- Các view Required được xử lý.
- Architecture đáp ứng critical requirements ở mức nền tảng.
- Các quyết định quan trọng có rationale và authority.
- Security và data concerns đã được xem xét.
- Không còn critical architecture contradiction chưa có phương án xử lý được phê duyệt.

## 8. Stage 5 — Establish Governance

### Objective

Thiết lập cơ chế quản trị trước khi tăng cường tự động hóa hoặc giao quyền cho agents.

### Activities

- Xác định roles.
- Xác định decision authority.
- Xác định approval workflow.
- Xác định execution permissions.
- Xác định exception process.
- Xác định escalation path.
- Xác định change control.
- Xác định audit requirements.
- Xác định conflict resolution.

### Deliverables

- Governance Model.
- Authority Matrix.
- Decision Register.
- Approval Rules.
- Agent Permission Policy.
- Exception Policy.
- Escalation Rules.

### Exit Conditions

- Project Owner hoặc trạng thái chưa có owner được ghi rõ.
- Các quyền quyết định quan trọng có người chịu trách nhiệm.
- Agent execution boundaries được xác định.
- Có cơ chế xử lý xung đột và ngoại lệ.

## 9. Stage 6 — Documentation Foundation

### Objective

Tạo bộ tài liệu có cấu trúc và nguồn có thẩm quyền rõ ràng.

### Activities

- Xác định artifact types.
- Thiết lập Document IDs.
- Thiết lập metadata.
- Thiết lập document authority map.
- Thiết lập versioning.
- Liên kết requirements, decisions và artifacts.
- Kiểm tra nội dung trùng lặp.
- Kiểm tra tài liệu mâu thuẫn.
- Ghi nhận unresolved items.

### Deliverables

- Documentation Index.
- Specifications.
- Policies.
- Contracts.
- Decision Records.
- Traceability Register.
- Artifact Manifest.

### Exit Conditions

- Tài liệu bắt buộc tồn tại.
- Artifact identity hợp lệ.
- Authority được xác định.
- Critical requirements có traceability.
- Nội dung chưa phê duyệt không bị trình bày như approved.

## 10. Stage 7 — Agent Foundation

### Objective

Chuẩn bị hệ thống AI agents có thể làm việc trong phạm vi project đã được quản trị.

### Activities

- Xác định agent roles.
- Xác định responsibilities.
- Xây dựng agent instructions.
- Xác định skills và workflows.
- Xác định provider requirements.
- Xác định permission levels.
- Xác định data handling rules.
- Xác định multi-agent coordination.
- Xác định conflict reporting.
- Xác định audit trail.

### Deliverables

- Agent Registry.
- Agent Policies.
- Agent Instructions.
- Skills.
- Workflows.
- Provider Adapter Requirements.
- Permission Matrix.
- Agent Validation Cases.

### Exit Conditions

- Mỗi agent có role và scope.
- Không có agent tự cấp quyền.
- Có cơ chế ghi nhận action và output.
- Có cơ chế xử lý bất đồng.
- Provider independence được duy trì.

## 11. Stage 8 — Quality Foundation

### Objective

Xác định cách đánh giá nền móng và bằng chứng cần thiết trước khi bootstrap hoặc nghiệm thu.

### Activities

- Xác định quality dimensions.
- Xác định critical requirements.
- Xây dựng validation rules.
- Xây dựng consistency checks.
- Xây dựng acceptance criteria.
- Xác định evidence sources.
- Xác định exception conditions.
- Xác định independent review requirements.

### Deliverables

- Quality Plan.
- Validation Specification.
- Test Specifications.
- Acceptance Criteria.
- Evidence Register.
- Quality Risk Register.

### Exit Conditions

- Critical requirements có verification path.
- Có acceptance criteria.
- Có quy tắc xử lý failed checks.
- Có cơ chế không cho phép critical failure bị che bởi điểm tổng hợp.

## 12. Stage 9 — Bootstrap Project

### Objective

Tạo các artifact và cấu trúc nền móng thực tế từ tài liệu đã được phê duyệt.

### Activities

- Kiểm tra generation plan.
- Xác định target paths.
- Kiểm tra file ownership.
- Kiểm tra conflicts.
- Preview changes.
- Kiểm tra permissions.
- Tạo staging plan.
- Thực hiện các thao tác được ủy quyền.
- Validate generated outputs.
- Ghi nhận manifest và operation results.

### Deliverables

- Generated Foundation.
- Generation Manifest.
- Operation Log.
- Validation Report.
- Recovery Information.

### Exit Conditions

- Không ghi đè nội dung ngoài quyền.
- Các artifact được tạo đúng kế hoạch.
- Validation đạt yêu cầu.
- Các thao tác thất bại được ghi nhận.
- Recovery path được xác định cho các thay đổi có rủi ro.

## 13. Stage 10 — Independent Audit

### Objective

Đánh giá độc lập trước khi Project Foundation được công nhận là baseline.

### Audit Scope

- Requirements coverage.
- Architecture consistency.
- Governance completeness.
- Authority correctness.
- Document integrity.
- Traceability.
- Agent permissions.
- Security and data handling.
- Version compatibility.
- Quality evidence.
- Bootstrap correctness.
- Open risks and exceptions.

### Deliverables

- Independent Audit Report.
- Findings Register.
- Remediation Recommendations.
- Residual Risk Assessment.

### Exit Conditions

- Critical findings không bị bỏ qua.
- Các finding có severity, evidence và disposition.
- Finding cần remediation đã được xử lý hoặc có exception được phê duyệt.
- Auditor không tự phê duyệt thay Project Owner.

## 14. Stage 11 — Baseline Approval

### Objective

Xác lập một Project Foundation version cụ thể làm baseline chính thức.

### Activities

- Tổng hợp deliverables.
- Kiểm tra acceptance criteria.
- Xem xét audit report.
- Xem xét unresolved risks.
- Xem xét exceptions.
- Xác định baseline version.
- Ghi nhận approval.
- Đóng gói manifest và evidence.

### Deliverables

- Approved Project Foundation Baseline.
- Baseline Manifest.
- Approval Record.
- Final Acceptance Report.

### Exit Conditions

- Acceptance criteria được đáp ứng.
- Không còn critical unresolved finding.
- Exceptions có authority, rationale và review condition.
- Project Owner hoặc người được ủy quyền phê duyệt.
- Baseline identity và version được ghi nhận.

## 15. Stage Transition Model

Mỗi stage phải có trạng thái:

- Not Started.
- In Progress.
- Blocked.
- Ready for Review.
- Changes Requested.
- Approved.
- Completed.
- Not Applicable.

Quy tắc:

1. `Ready for Review` chỉ có nghĩa là đã gửi để xem xét.
2. `Approved` chỉ được thiết lập bởi authority phù hợp.
3. `Completed` chỉ được thiết lập khi exit conditions đã đạt.
4. `Blocked` phải có lý do và dependency.
5. `Not Applicable` phải có rationale và approval.
6. Một stage Completed có thể được mở lại khi phát hiện thông tin mới hoặc thay đổi có ảnh hưởng.

Không được dùng một trạng thái duy nhất `Done` để thay thế các trạng thái trên.

## 16. Iteration and Rework

Methodology cho phép quay lại stage trước khi có lý do chính đáng.

Ví dụ:

- Discovery phát hiện dữ liệu sai → quay lại Discovery.
- Requirements thay đổi → đánh giá lại Requirements và Architecture.
- Architecture change tác động security → mở lại Security View.
- Scope thay đổi → đánh giá lại Capability Model.
- Audit phát hiện thiếu traceability → mở lại Documentation Foundation.

Khi quay lại:

- Ghi nhận trigger.
- Xác định affected artifacts.
- Phân tích impact.
- Giữ lịch sử phiên bản.
- Chạy lại các validation bị ảnh hưởng.
- Cập nhật baseline nếu đã được phê duyệt trước đó.

## 17. Parallel Work

Các stage có thể thực hiện song song khi không vi phạm dependency.

Ví dụ:

- Discovery và thu thập domain knowledge.
- Requirements và inventory tài liệu hiện có.
- Architecture views khác nhau do các chuyên gia khác nhau phân tích.

Điều kiện:

- Mỗi workstream có owner.
- Có input version rõ ràng.
- Có interface hoặc dependency contract.
- Có quy trình tích hợp kết quả.
- Có cơ chế xử lý conflicts.

Không được coi output của nhiều agent là một kết quả thống nhất khi chưa tích hợp và kiểm tra.

## 18. Tailoring Methodology

Project Profile quyết định:

- Stage nào cần thực hiện đầy đủ.
- Stage nào có thể đơn giản hóa.
- Deliverables nào bắt buộc.
- Mức độ độc lập của audit.
- Quality thresholds.
- Approval requirements.

Không được loại bỏ các kiểm soát cần thiết cho critical risks chỉ để rút ngắn quy trình.

Mọi tailoring phải có rationale và authority theo `PFS-M0-SPEC-003` và `PFS-M0-SPEC-006`.

## 19. Methodology Failure Conditions

Một stage phải bị đánh dấu Blocked hoặc không được hoàn tất khi:

- Thiếu authority cần thiết.
- Có critical contradiction chưa giải quyết.
- Requirements quan trọng chưa rõ.
- Thiếu evidence bắt buộc.
- Agent vượt quyền.
- Generated output không xác minh được.
- Có data/security issue chưa được xử lý.
- Có approval giả định hoặc không hợp lệ.

## 20. Methodology Requirements

| ID | Requirement |
|---|---|
| M0-MTH-001 | PFS MUST có lifecycle từ project initialization đến baseline approval. |
| M0-MTH-002 | Mỗi stage MUST có objective, activities, deliverables và exit conditions. |
| M0-MTH-003 | PFS MUST hỗ trợ iteration và reopening khi có trigger hợp lệ. |
| M0-MTH-004 | Stage transition MUST tuân thủ dependency và approval rules. |
| M0-MTH-005 | PFS MUST phân biệt Ready for Review, Approved và Completed. |
| M0-MTH-006 | PFS MUST hỗ trợ methodology tailoring có rationale. |
| M0-MTH-007 | Critical failures MUST NOT bị bỏ qua để hoàn tất stage. |
| M0-MTH-008 | Parallel work MUST có ownership và integration control. |
| M0-MTH-009 | Baseline approval MUST có evidence và authority hợp lệ. |
| M0-MTH-010 | Mọi reopening hoặc rework quan trọng MUST có impact record. |

## 21. M1 Design Dependencies

M1 phải cụ thể hóa:

- Stage state machine.
- Stage transition schema.
- Deliverable registry.
- Dependency representation.
- Workflow contracts.
- Evidence model.
- Baseline manifest.
- Reopening and change propagation model.

M1 MUST giữ nguyên lifecycle và governance invariants được M0 phê duyệt.

---

**End of Document — PFS-M0-SPEC-004 v1.1.0**
