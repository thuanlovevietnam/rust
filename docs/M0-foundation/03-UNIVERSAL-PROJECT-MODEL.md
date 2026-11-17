# PFS-M0-SPEC-003 — Universal Project Model

**Document ID:** PFS-M0-SPEC-003  
**Document Type:** Domain Model Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-001, PFS-M0-SPEC-002, PFS-M0-SPEC-004, PFS-M0-SPEC-007, PFS-M0-SPEC-010

---

## 1. Purpose

Tài liệu này định nghĩa mô hình dự án universal mà PFS sử dụng để hiểu, phân loại, cấu hình và xây dựng nền móng cho nhiều loại dự án.

Mục tiêu quan trọng nhất:

**PFS phải có một mô hình chung đủ ổn định để quản lý mọi dự án, nhưng không được áp đặt một cấu trúc hoặc quy trình giống nhau lên mọi dự án.**

Tài liệu này giải quyết vấn đề Universal Project Model (F01) và Project Tailoring.

## 2. Core Design Rules

PFS MUST tuân thủ các quy tắc:

1. Project là đơn vị trung tâm của việc tạo nền móng.
2. Project category chỉ mô tả loại hình, không quyết định toàn bộ architecture.
3. Project Profile mô tả bối cảnh và constraints.
4. Capability Model xác định năng lực hoặc thành phần nào áp dụng.
5. Architecture View Model xác định các góc nhìn kiến trúc cần xử lý.
6. Tailoring decisions phải có rationale và authority.
7. Mọi requirement critical phải được xử lý rõ ràng.
8. Not Applicable không đồng nghĩa với việc được phép bỏ qua.
9. Không được suy diễn rằng một dự án thuộc category nào đó thì bắt buộc phải sử dụng một stack hoặc methodology cố định.
10. Universal model phải hỗ trợ mở rộng mà không phá vỡ định danh và lịch sử của dự án.

## 3. Universal Project Concept

Một Project trong PFS là một sáng kiến có:

- Mục tiêu hoặc kết quả mong muốn.
- Phạm vi.
- Chủ thể chịu trách nhiệm.
- Bối cảnh.
- Constraints.
- Stakeholders.
- Requirements hoặc mục tiêu cần đạt.
- Cách đánh giá kết quả.
- Một tập hợp artifact và decision cần quản lý.

Một Project có thể là:

- Một sản phẩm.
- Một hệ thống.
- Một chương trình.
- Một hoạt động nghiên cứu.
- Một dự án kinh doanh.
- Một quy trình tổ chức.
- Một sáng kiến sáng tạo.
- Một dự án kết hợp nhiều loại hình.

PFS MAY hỗ trợ project decomposition thành sub-project, workstream hoặc component nếu quy mô yêu cầu.

Quan hệ giữa các đơn vị này phải được định danh rõ, không chỉ thể hiện bằng cấu trúc thư mục.

## 4. Project Profile

Project Profile là bản mô tả có cấu trúc về bối cảnh và đặc điểm của một dự án.

### 4.1. Profile Sections

Một Project Profile SHOULD bao gồm:

| Section | Mô tả |
|---|---|
| Identity | Project ID, name, description, version |
| Ownership | Project Owner và các vai trò liên quan |
| Purpose | Mục tiêu, outcome, success definition |
| Category | Loại hình dự án |
| Scope | In-scope, out-of-scope |
| Context | Bối cảnh và môi trường |
| Stakeholders | Các bên liên quan |
| Constraints | Ràng buộc |
| Assumptions | Giả định |
| Dependencies | Phụ thuộc bên ngoài và nội bộ |
| Complexity | Độ phức tạp |
| Risk | Rủi ro |
| Capabilities | Năng lực cần có |
| Architecture | Architecture views áp dụng |
| Governance | Yêu cầu quản trị |
| Quality | Chất lượng và acceptance expectations |
| Data | Dữ liệu và phân loại dữ liệu |
| Technology | Technology constraints nếu có |
| Compliance | Nghĩa vụ pháp lý hoặc tiêu chuẩn nếu áp dụng |
| Lifecycle | Vòng đời dự án |
| Baseline | Trạng thái baseline và version |

Không phải mọi section đều bắt buộc có giá trị ngay từ lúc khởi tạo. Section chưa xác định phải được đánh dấu `TBD`, không tự lấp bằng giả định không có căn cứ.

### 4.2. Project Identity

Mỗi Project MUST có một Project ID ổn định.

Project ID:

- Không phụ thuộc tên hiển thị.
- Không thay đổi khi đổi tên.
- Không được tái sử dụng.
- Có thể được tham chiếu bởi artifact, agent tasks và reports.

Quy tắc định dạng ID cụ thể sẽ được chuẩn hóa ở M1.

### 4.3. Project Category

Project category là nhãn phân loại để hỗ trợ discovery, template selection và gợi ý capability.

Ví dụ:

- Software.
- Research.
- Business.
- Operations.
- Data.
- Content.
- Product.
- Infrastructure.
- Organizational.
- Mixed / Hybrid.

Danh sách này có tính mở rộng.

Category MUST NOT tự động quyết định:

- Technology stack.
- Architecture pattern.
- Agent permissions.
- Security level.
- Approval authority.
- Quality threshold.

Những quyết định đó phải dựa trên profile, requirements, risks và constraints.

## 5. Capability Model

Capability là một năng lực hoặc nhóm chức năng cần được xử lý để tạo nền móng phù hợp.

Ví dụ capability:

- Requirements Management.
- Architecture Design.
- Data Management.
- Security Management.
- Financial Control.
- Inventory Management.
- Research Management.
- Content Governance.
- Operations Planning.
- Agent Automation.
- Quality Assurance.
- Regulatory Compliance.
- Deployment Planning.

Capability catalog là extensible; các ví dụ không tạo thành danh sách đóng.

### 5.1. Capability Applicability States

Mỗi capability phải có một trong ba trạng thái:

**Required**

- Capability bắt buộc trong phạm vi dự án.
- Phải có owner hoặc authority phù hợp.
- Phải có deliverable và verification tương ứng.
- Không được bỏ qua chỉ vì chi phí hoặc độ phức tạp nếu chưa có exception được phê duyệt.

**Optional**

- Có thể áp dụng tùy mục tiêu, nguồn lực và risk.
- Nếu được chọn, phải xác định phạm vi và cách kiểm chứng phù hợp.

**Not Applicable**

- Capability không áp dụng cho dự án hoặc phần phạm vi được xét.
- MUST có rationale.
- MUST xác định ai có quyền chấp thuận trạng thái này.
- MUST được đánh giá lại nếu scope hoặc risk thay đổi.

### 5.2. Capability Record

Một Capability Record SHOULD chứa:

- Capability ID.
- Name.
- Description.
- Applicability state.
- Rationale.
- Source requirement.
- Owner.
- Dependencies.
- Related artifacts.
- Verification method.
- Approval status.
- Review trigger.

### 5.3. Dependency Rules

Capability có thể phụ thuộc vào capability khác.

Ví dụ:

- Financial Control có thể cần Data Management.
- Agent Automation có thể cần Security Management.
- Deployment Planning có thể cần Architecture Design.
- Regulatory Compliance có thể tác động đến Data Management và Security Management.

Dependency không tự động biến capability phụ thuộc thành Required. PFS phải đánh giá dependency và đưa ra quyết định có căn cứ.

## 6. Architecture View Model

Mọi dự án cần được xem xét về kiến trúc theo các concern phù hợp.

PFS sử dụng các architecture views chuẩn sau:

| View | Câu hỏi trọng tâm |
|---|---|
| Context View | Hệ thống hoặc dự án tồn tại trong môi trường nào? |
| Structure View | Các thành phần và quan hệ được tổ chức ra sao? |
| Behavior View | Quy trình, hành vi, trạng thái và luồng hoạt động thế nào? |
| Data View | Dữ liệu được tạo, lưu trữ, xử lý, bảo vệ và lưu chuyển ra sao? |
| Security View | Trust boundary, threats, permissions và controls là gì? |
| Interface View | Các bên và thành phần giao tiếp với nhau bằng cách nào? |
| Deployment View | Các thành phần được triển khai hoặc phân bố ở đâu? |
| Operations View | Hệ thống được vận hành, giám sát, bảo trì và phục hồi thế nào? |

### 6.1. View Applicability

Mỗi view có trạng thái:

- Required.
- Optional.
- Not Applicable.

View Required MUST có deliverable hoặc mô tả được kiểm chứng.

View Optional có thể được tạo khi cần.

View Not Applicable MUST có rationale và approval phù hợp.

### 6.2. Context View

Phải xem xét:

- External actors.
- External systems.
- Environment.
- Dependencies.
- Trust boundaries.
- Regulatory hoặc operational context nếu áp dụng.

### 6.3. Structure View

Phải xem xét:

- Components.
- Responsibilities.
- Ownership.
- Dependencies.
- Boundaries.
- Coupling và cohesion nếu phù hợp.

### 6.4. Behavior View

Phải xem xét:

- Workflows.
- Processes.
- Events.
- State transitions.
- Business rules.
- Failure paths.
- Human interactions.

### 6.5. Data View

Phải xem xét:

- Data entities.
- Data ownership.
- Data lifecycle.
- Data quality.
- Data integrity.
- Access and retention.
- Backup và recovery nếu áp dụng.

### 6.6. Security View

Phải xem xét:

- Assets.
- Threats.
- Trust boundaries.
- Identity.
- Authentication và authorization nếu phù hợp.
- Least privilege.
- Auditability.
- Data classification.
- Security controls.

### 6.7. Interface View

Phải xem xét:

- Human interfaces.
- System interfaces.
- API hoặc protocol nếu có.
- Data exchange.
- Contracts.
- Compatibility.
- Error handling.

### 6.8. Deployment View

Phải xem xét:

- Physical hoặc logical deployment units.
- Hosting environment.
- Distribution.
- Infrastructure dependencies.
- Deployment constraints.
- Environment separation.

### 6.9. Operations View

Phải xem xét:

- Monitoring.
- Logging.
- Maintenance.
- Support.
- Incident handling.
- Recovery.
- Operational ownership.

Không phải mọi dự án đều có đầy đủ các view này. Nhưng PFS MUST đánh giá applicability của chúng thay vì mặc định bỏ qua.

## 7. Project Complexity Model

PFS SHOULD đánh giá complexity theo nhiều chiều, không chỉ theo kích thước.

Các chiều tham khảo:

- Scope complexity.
- Technical complexity.
- Domain complexity.
- Stakeholder complexity.
- Data complexity.
- Integration complexity.
- Operational complexity.
- Security complexity.
- Regulatory complexity.
- Change volatility.

Có thể sử dụng mức:

- Low.
- Medium.
- High.
- Critical.

Mỗi mức phải có rationale dựa trên evidence hoặc đánh giá được ghi nhận.

Không được dùng một điểm tổng hợp để che giấu một chiều có risk critical.

## 8. Risk Model

Risk assessment SHOULD xem xét:

- Likelihood.
- Impact.
- Exposure.
- Detectability.
- Reversibility.
- Affected stakeholders.
- Existing controls.
- Residual risk.

Risk rating có thể được chuẩn hóa ở các milestone sau.

Một risk critical MUST được đưa vào governance và acceptance process.

Không được coi việc chưa có thông tin về risk là bằng chứng risk thấp.

## 9. Project Tailoring

Tailoring là quá trình điều chỉnh methodology, artifacts, architecture views, governance và quality requirements theo project context.

### 9.1. Tailoring Inputs

Tailoring phải căn cứ vào:

- Project objectives.
- Scope.
- Project category.
- Complexity.
- Risk.
- Stakeholders.
- Constraints.
- Capabilities.
- Applicable architecture views.
- Legal hoặc regulatory requirements.
- Resources.
- Delivery model.

### 9.2. Tailoring Decisions

Mỗi quyết định tailoring SHOULD ghi:

- Decision ID.
- Project ID.
- Affected capability hoặc view.
- Selected applicability.
- Rationale.
- Evidence.
- Risk and impact.
- Approver.
- Effective version.
- Review condition.

### 9.3. Tailoring Restrictions

Tailoring MUST NOT:

- Vô hiệu hóa quyền quyết định của Project Owner.
- Bỏ qua security requirements bắt buộc.
- Xóa traceability đối với critical requirements.
- Biến assumption thành fact.
- Hạ quality threshold mà không có authority.
- Vượt qua nghĩa vụ pháp lý hoặc hợp đồng áp dụng.

Nếu có ngoại lệ, phải sử dụng exception process.

## 10. Universal Artifact Relationship

Các thành phần của Project Model có quan hệ logic:

`Project → Profile → Objectives → Requirements → Capabilities → Architecture Views → Decisions → Artifacts → Verification → Baseline`

Quan hệ này không bắt buộc là một cây phân cấp đơn giản.

Một requirement có thể liên quan đến nhiều capabilities.

Một architecture view có thể phục vụ nhiều requirements.

Một decision có thể tác động đến nhiều artifacts.

Một artifact có thể được tạo ra từ nhiều nguồn.

Các quan hệ phải được định danh và truy vết theo Artifact and Traceability Model.

## 11. Handling Unknown Information

PFS MUST phân biệt các trạng thái thông tin:

- Known: Có nguồn xác định.
- Assumed: Giả định cần xác nhận.
- Inferred: Được suy luận từ thông tin khác.
- Proposed: Được đề xuất.
- Validated: Đã kiểm chứng theo phương pháp phù hợp.
- Approved: Được người có thẩm quyền phê duyệt.
- Rejected: Bị từ chối.
- TBD: Chưa xác định.

Một thông tin có thể vừa được validated về mặt kỹ thuật nhưng vẫn chưa được approved về mặt governance.

Không được gộp các trạng thái trên thành một nhãn chung như `Complete`.

## 12. Universal Project Model Invariants

Các invariants sau MUST được giữ:

1. Mỗi Project có identity ổn định.
2. Mỗi Project có Project Owner hoặc trạng thái owner chưa được xác định phải được thể hiện rõ.
3. Project category không áp đặt architecture.
4. Capability applicability phải được xác định.
5. Not Applicable cần rationale.
6. Architecture view applicability phải được đánh giá.
7. Critical requirements không được âm thầm loại bỏ.
8. Assumptions không được trình bày như facts.
9. Tailoring decisions phải có traceability.
10. Các thay đổi scope phải kích hoạt đánh giá lại capability, view, risk và acceptance.

## 13. Example: Applying the Model

### Example A — Software Product

Một sản phẩm SaaS có thể cần:

- Requirements Management: Required.
- Architecture Design: Required.
- Data Management: Required.
- Security Management: Required.
- Operations Planning: Required.
- Deployment View: Required.
- Financial Control: Optional hoặc Required tùy business scope.

PFS không tự chọn Rust, Flutter, database hay cloud provider chỉ dựa vào nhãn SaaS.

### Example B — Research Project

Một dự án nghiên cứu có thể cần:

- Research Management: Required.
- Data Management: Required.
- Methodology: Required.
- Evidence and Quality: Required.
- Software Deployment: Not Applicable nếu không có phần mềm cần triển khai; phải ghi rationale.

### Example C — Business Operations Project

Một dự án quản lý kho và tài chính có thể cần:

- Financial Control: Required.
- Inventory Management: Required.
- Data Integrity: Required.
- Security: Required.
- Auditability: Required.
- Deployment View: tùy mô hình vận hành.

Ba ví dụ chỉ minh họa cách áp dụng model, không tạo ra template bắt buộc.

## 14. Requirements

| Canonical ID | Legacy ID | Requirement |
|---|---|---|
| M0-UNI-001 | M0-REQ-001 | PFS MUST hỗ trợ Universal Project Model độc lập với project category. |
| M0-UNI-002 | M0-REQ-002 | PFS MUST có Project Profile mô tả bối cảnh, mục tiêu, constraints và stakeholders. |
| M0-UNI-003 | M0-REQ-003 | PFS MUST phân biệt project category với architecture decisions. |
| M0-UNI-004 | M0-REQ-004 | PFS MUST hỗ trợ capability applicability: Required, Optional, Not Applicable. |
| M0-UNI-005 | M0-REQ-005 | Not Applicable MUST có rationale và approval phù hợp. |
| M0-UNI-006 | M0-REQ-006 | PFS MUST đánh giá applicability của các architecture views. |
| M0-UNI-007 | M0-REQ-007 | PFS MUST phân biệt known, assumed, inferred, proposed, validated và approved information. |
| M0-UNI-008 | M0-REQ-008 | PFS MUST ghi nhận tailoring decisions và traceability. |
| M0-UNI-009 | M0-REQ-009 | PFS MUST đánh giá lại tác động khi scope hoặc risk thay đổi. |
| M0-UNI-010 | M0-REQ-010 | PFS MUST NOT áp đặt technology stack của PFS lên generated projects. |

## 15. Verification Criteria

Universal Project Model đạt yêu cầu khi:

1. Có thể mô tả ít nhất hai loại dự án khác nhau mà không phải thay đổi cấu trúc lõi của model.
2. Có thể khai báo capability Required, Optional và Not Applicable.
3. Có thể ghi rationale cho Not Applicable.
4. Có thể đánh giá architecture views độc lập với project category.
5. Có thể ghi nhận assumption và unknown information.
6. Có thể truy vết tailoring decisions.
7. Không có quy tắc ngầm buộc mọi dự án dùng cùng một architecture.
8. Có cơ chế đánh giá lại khi scope hoặc risk thay đổi.

Evidence phải bao gồm model definition, ví dụ áp dụng và kết quả review.

## 16. Open Design Items for M1

Các nội dung sau được giữ lại để thiết kế chi tiết ở M1, không tự ý coi là đã quyết định ở M0:

- Machine-readable Project Profile schema.
- Canonical capability registry schema.
- Canonical architecture view schema.
- Project ID format.
- Taxonomy extension mechanism.
- Project hierarchy representation.
- Formal risk scoring model.
- Formal tailoring decision schema.
- Artifact relationship schema.

M1 MUST giữ nguyên các invariants đã được M0 phê duyệt.

---

**End of Document — PFS-M0-SPEC-003 v1.1.0**
