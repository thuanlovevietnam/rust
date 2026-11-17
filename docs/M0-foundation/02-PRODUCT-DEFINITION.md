# PFS-M0-SPEC-002 — Product Definition

**Document ID:** PFS-M0-SPEC-002  
**Document Type:** Product Definition Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Proposed — Awaiting Owner Approval  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-001, PFS-M0-SPEC-003, PFS-M0-SPEC-004, PFS-M0-SPEC-008

---

## 1. Product Definition

Project Foundation System (PFS) là một hệ thống hỗ trợ khởi tạo, chuẩn hóa, kiểm chứng và duy trì nền móng dự án.

PFS nhận đầu vào từ Project Owner và các nguồn được cho phép, phân tích bối cảnh dự án, xây dựng các artifact cần thiết, phối hợp AI agents với automation, kiểm tra chất lượng và tạo ra một Project Foundation có thể được quản lý như một baseline.

**Product statement:**

PFS biến một ý tưởng hoặc yêu cầu ban đầu thành một nền móng dự án có cấu trúc, có governance, có thể truy vết, có thể kiểm chứng và có thể tiếp tục phát triển.

## 2. Product Boundary

PFS có hai phạm vi cần phân biệt:

### 2.1. PFS System

Là chính sản phẩm PFS, bao gồm:

- Methodology.
- Project model.
- Requirements và artifact model.
- Architecture và governance model.
- Agent system.
- AI provider integration.
- Deterministic execution engine.
- Validation và quality gates.
- Generator và CLI.
- Foundation management.

### 2.2. Generated Project Foundation

Là đầu ra PFS tạo cho một dự án cụ thể.

Có thể gồm:

- Project Profile.
- Project Vision.
- Product Definition.
- Requirements.
- Constraints và assumptions.
- Architecture descriptions.
- Decision records.
- Interface contracts.
- Security policies.
- Governance rules.
- Agent instructions.
- Skills và workflows.
- Test và validation specifications.
- Bootstrap configuration.
- Baseline manifest.

Không phải dự án nào cũng cần tất cả artifact trên. Danh mục cụ thể được xác định bởi Project Profile, Capability Model và tailoring decisions.

### 2.3. Generated Project

Là dự án thực tế tiếp tục được phát triển dựa trên Foundation.

PFS có thể hỗ trợ các giai đoạn sau này, nhưng M0 không tuyên bố PFS đã là một IDE, một coding agent hoàn chỉnh hoặc một nền tảng triển khai ứng dụng tự động.

## 3. Product Users and Stakeholders

PFS được thiết kế để hỗ trợ các vai trò:

### 3.1. Project Owner

Người chịu trách nhiệm cuối cùng về mục tiêu, phạm vi, các quyết định thuộc quyền sở hữu và việc chấp thuận kết quả.

### 3.2. Project Initiator

Người khởi tạo ý tưởng hoặc đề xuất dự án. Có thể là Project Owner hoặc người được ủy quyền.

### 3.3. Project Architect

Người chịu trách nhiệm thiết kế và đánh giá kiến trúc trong phạm vi được giao.

### 3.4. Domain Expert

Người cung cấp kiến thức chuyên môn về lĩnh vực dự án.

### 3.5. Security Reviewer

Người đánh giá các vấn đề bảo mật, dữ liệu, quyền hạn và rủi ro.

### 3.6. AI Agent

Tác nhân AI thực hiện các nhiệm vụ được giao theo policy, scope và permission.

### 3.7. Operator

Người vận hành PFS hoặc thực hiện các thao tác được ủy quyền.

### 3.8. Independent Auditor

Người đánh giá độc lập chất lượng, tính nhất quán và evidence.

Các vai trò này có thể do một người đảm nhiệm trong dự án nhỏ, nhưng quyền hạn và trách nhiệm MUST vẫn được phân biệt về mặt logic. Một agent không tự trở thành Project Owner chỉ vì được giao nhiều nhiệm vụ.

## 4. Core Product Capabilities

PFS hướng tới các nhóm năng lực sau.

### 4.1. Project Intake

- Tiếp nhận ý tưởng, mục tiêu và bối cảnh.
- Thu thập constraints, assumptions và stakeholders.
- Phát hiện thông tin còn thiếu.
- Ghi nhận mức độ tin cậy của thông tin.
- Tạo Project Profile ban đầu.

### 4.2. Requirements Engineering

- Phân loại requirements.
- Xác định functional và non-functional requirements khi phù hợp.
- Quản lý constraints và assumptions.
- Phát hiện ambiguity và contradiction.
- Thiết lập acceptance criteria.
- Liên kết requirements với mục tiêu và verification.

### 4.3. Architecture Foundation

- Phân tích các architecture concerns.
- Xác định các architecture views cần thiết.
- Đánh giá phương án và trade-offs.
- Quản lý Architecture Decision Records.
- Xác định interfaces, dependencies và constraints.
- Ghi nhận các vấn đề chưa được quyết định.

### 4.4. Documentation Foundation

- Tạo tài liệu theo template có version.
- Duy trì document identity.
- Quản lý quan hệ giữa artifacts.
- Kiểm tra metadata và cấu trúc.
- Phát hiện nội dung mâu thuẫn hoặc lỗi thời.

### 4.5. Governance Foundation

- Xác định vai trò.
- Phân quyền quyết định.
- Thiết lập approval workflow.
- Quản lý exception.
- Quản lý change history.
- Ghi nhận authority conflicts.

### 4.6. Agent Foundation

- Định nghĩa agent roles.
- Quản lý policies, skills và workflows.
- Thiết lập permission boundaries.
- Quản lý provider adapters.
- Phối hợp nhiều agent.
- Ghi nhận agent actions và evidence.

### 4.7. Quality Foundation

- Xác định quality dimensions.
- Thiết lập validation rules.
- Đánh giá requirement coverage.
- Kiểm tra consistency.
- Thực hiện independent review.
- Đưa ra acceptance recommendation.

### 4.8. Bootstrap and Baseline

- Tạo cấu trúc thư mục và artifact.
- Kiểm tra file ownership và conflict.
- Preview thay đổi.
- Tạo generation manifest.
- Xác minh kết quả.
- Ghi nhận baseline và version.

Các năng lực trên là product direction. Phân bổ vào milestone được quy định tại `PFS-M0-SPEC-013`.

## 5. Product Operating Model

PFS sử dụng mô hình Hybrid Execution.

### 5.1. AI Reasoning Responsibilities

AI MAY:

- Phân tích nội dung và ngữ cảnh.
- Đặt câu hỏi làm rõ.
- Đề xuất requirements.
- Phân tích trade-offs.
- Soạn thảo tài liệu.
- Phát hiện mâu thuẫn ngữ nghĩa.
- Đề xuất phương án giải quyết.
- Tóm tắt evidence.
- Đưa ra recommendation.

AI MUST:

- Phân biệt fact, assumption, inference và recommendation.
- Chỉ rõ thông tin thiếu hoặc chưa được xác minh.
- Tôn trọng authority và approval state.
- Không tự chuyển proposal thành approved decision.
- Không vượt permission được cấp.

### 5.2. Deterministic Automation Responsibilities

Automation MAY:

- Kiểm tra schema.
- Kiểm tra metadata.
- Kiểm tra ID uniqueness.
- Kiểm tra file conflict.
- Kiểm tra requirement references.
- Validate manifest.
- Tạo hoặc cập nhật artifact theo kế hoạch được phê duyệt.
- Kiểm tra version compatibility.
- Tạo report có thể tái lập.

Automation MUST thực hiện theo quy tắc xác định, có thể kiểm tra và có kết quả quan sát được.

### 5.3. Responsibility Boundary

AI chịu trách nhiệm hỗ trợ reasoning, không phải là nguồn thẩm quyền cuối cùng.

Automation chịu trách nhiệm thực hiện quy tắc xác định, không được tự tạo ra quyết định nghiệp vụ hoặc kiến trúc vượt ngoài policy.

Người có thẩm quyền chịu trách nhiệm phê duyệt các quyết định được yêu cầu.

## 6. Product Inputs

PFS có thể nhận các đầu vào sau:

- Natural-language project brief.
- Existing documents.
- Requirements lists.
- Diagrams.
- Data models.
- Source code hoặc repository metadata.
- Policies và standards.
- Templates.
- Domain knowledge.
- External references được cho phép.
- User decisions và approval records.

Mỗi đầu vào cần có provenance phù hợp.

PFS MUST phân biệt:

- Nội dung do Project Owner cung cấp.
- Nội dung từ tài liệu bên ngoài.
- Nội dung do AI suy luận.
- Nội dung do automation tạo.
- Nội dung đã được kiểm chứng.
- Nội dung đã được phê duyệt.

## 7. Product Outputs

PFS có thể tạo:

1. Project Profile.
2. Project Brief.
3. Vision và Product Definition.
4. Requirements Specification.
5. Architecture Description.
6. Architecture Decision Records.
7. Interface và Data Contracts.
8. Governance Policies.
9. Agent Instructions.
10. Skills và Workflows.
11. Validation Specifications.
12. Acceptance Reports.
13. Bootstrap Artifacts.
14. Generation Manifest.
15. Foundation Baseline.

Đầu ra phải có ID, version và provenance theo artifact type tương ứng.

## 8. Product Lifecycle

PFS định hướng lifecycle gồm:

1. Initialize Project.
2. Discover Context.
3. Engineer Requirements.
4. Design Architecture.
5. Establish Governance.
6. Build Documentation Foundation.
7. Build Agent Foundation.
8. Establish Quality Foundation.
9. Bootstrap Project.
10. Independent Audit.
11. Approve Baseline.

Lifecycle này là quy trình tổng thể. Dự án có thể lặp lại một số bước khi phát hiện thiếu sót hoặc thay đổi, nhưng không được bỏ qua approval và verification bắt buộc.

Chi tiết phương pháp được quy định trong `PFS-M0-SPEC-004`.

## 9. Product Configuration and Tailoring

PFS MUST hỗ trợ cấu hình theo từng dự án.

Project Profile xác định:

- Project category.
- Objectives.
- Scope.
- Complexity.
- Risk.
- Constraints.
- Stakeholders.
- Applicable capabilities.
- Required architecture views.
- Governance needs.
- Quality expectations.
- Technology constraints.
- Regulatory hoặc compliance context nếu có.

Một capability có thể là:

- Required.
- Optional.
- Not Applicable.

`Not Applicable` MUST có rationale.

Không được bỏ qua một requirement critical chỉ bằng cách đổi capability thành `Not Applicable` mà không có authority phù hợp.

## 10. Product Quality Attributes

PFS itself SHOULD được đánh giá theo các thuộc tính:

- Correctness.
- Reliability.
- Security.
- Reproducibility.
- Traceability.
- Maintainability.
- Extensibility.
- Provider Independence.
- Interoperability.
- Usability.
- Performance phù hợp với workload.
- Recoverability.

Các thuộc tính này phải được cụ thể hóa thành requirement và verification criteria ở milestone thiết kế và triển khai. Không coi danh sách này là bằng chứng sản phẩm đã đạt các thuộc tính đó.

## 11. Product Security Boundary

PFS phải xem các nguồn sau là không mặc nhiên đáng tin:

- AI-generated content.
- External templates.
- Third-party skills.
- Imported documents.
- Provider responses.
- Scripts.
- Plugins hoặc extensions.
- User-provided artifacts từ nguồn chưa xác minh.

PFS MUST áp dụng data classification, provenance, permission checks và validation tương ứng.

PFS MUST NOT đưa secrets vào generated documentation, prompts, manifests hoặc logs nếu không có cơ chế bảo vệ được phê duyệt.

Chi tiết security và supply chain thuộc `PFS-M0-SPEC-012`; agent permission thuộc `PFS-M0-SPEC-009`.

## 12. Product Constraints

Các quyết định nền tảng:

| ID | Constraint |
|---|---|
| PFS-CON-001 | PFS Core được triển khai bằng Rust. |
| PFS-CON-002 | PFS sử dụng Hybrid AI Reasoning + Deterministic Automation. |
| PFS-CON-003 | PFS không khóa vào một AI provider. |
| PFS-CON-004 | PFS hỗ trợ nhiều loại dự án, không giới hạn software. |
| PFS-CON-005 | Technology stack của PFS không áp đặt lên generated projects. |
| PFS-CON-006 | Quyền quyết định và quyền thực thi phải được phân biệt. |
| PFS-CON-007 | Quality claims quan trọng phải có evidence. |
| PFS-CON-008 | Thay đổi phải có version và traceability phù hợp. |

Các constraint trên là nền tảng của M0; chi tiết implementation chưa được coi là đã quyết định nếu chưa có ADR hoặc SPEC tương ứng.

## 13. Explicit Non-Goals for M0

M0 không triển khai:

- Rust execution engine.
- AI provider adapters thực tế.
- Multi-agent runtime.
- CLI hoàn chỉnh.
- File generator.
- Repository bootstrap automation.
- Production UI.
- Deployment orchestration.
- Autonomous coding.
- Automatic project release.

M0 chỉ xác lập methodology, product definition, principles, governance và các hợp đồng nền tảng cần thiết cho các milestone tiếp theo.

## 14. Product Acceptance Direction

Một Project Foundation chỉ được xem là có thể bàn giao khi:

- Đáp ứng Project Profile đã phê duyệt.
- Các requirements bắt buộc có trạng thái rõ ràng.
- Architecture views cần thiết đã được xử lý.
- Decision authority được xác định.
- Các artifact có identity và traceability.
- Agent permissions được xác định.
- Validation evidence có thể kiểm tra.
- Critical conflicts đã được giải quyết hoặc được xử lý theo exception policy có thẩm quyền.
- Baseline có version và manifest phù hợp.

## 15. Product Evolution

PFS được phát triển theo milestone, không mở rộng tùy tiện.

Mỗi milestone MUST:

- Có scope.
- Có deliverables.
- Có dependencies.
- Có acceptance criteria.
- Có non-goals.
- Có exit conditions.

Milestone sau không được âm thầm thay đổi các nguyên tắc đã được phê duyệt ở milestone trước.

## 16. Product Requirements

Các yêu cầu định nghĩa sản phẩm chuẩn được quản lý trong Global Requirement Registry:

| Canonical ID | Legacy Ref | Product Requirement Statement |
|---|---|---|
| M0-PROD-001 | PFS-CON-004 | PFS MUST hỗ trợ universal product scope cho nhiều loại project, không chỉ software project, kết hợp methodology, structured project knowledge, AI reasoning và deterministic automation. |
| M0-PROD-002 | PFS-CON-001, PFS-CON-005 | PFS Core MUST được triển khai bằng Rust và không ép project đích dùng Rust. |
| M0-PROD-003 | PFS-CON-002 | PFS MUST sử dụng mô hình thực thi Hybrid (AI reasoning + Deterministic automation). |
| M0-PROD-004 | PFS-CON-003 | PFS MUST độc lập với AI provider (provider-independent). |
| M0-PROD-005 | — | PFS MUST phân biệt ranh giới giữa PFS system, generated foundation và generated project. |
| M0-PROD-006 | PFS-CON-006 | PFS MUST phân biệt rõ ràng giữa quyền quyết định (decision authority) và quyền thực thi (execution permission). |
| M0-PROD-007 | PFS-CON-007 | PFS MUST yêu cầu quality claims quan trọng phải có verifiable evidence. |
| M0-PROD-008 | PFS-CON-008 | PFS MUST quản lý thay đổi có version, compatibility và traceability. |

---

**End of Document — PFS-M0-SPEC-002 v1.1.0**
