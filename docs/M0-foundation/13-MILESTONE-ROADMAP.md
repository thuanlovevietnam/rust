# PFS-M0-SPEC-013 — Milestone Roadmap

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M0-SPEC-013 |
| Tên | PFS Milestone Roadmap |
| Version | 1.1.0 |
| Status | Proposed — Awaiting Owner Approval |
| Phase | M0 — Foundation Definition |
| Authority | Project Owner |
| Classification | Internal |
| Language | Vietnamese |
| Parent specification | PFS-M0-SPEC-001 |
| Related specifications | PFS-M0-SPEC-002..012, PFS-M0-SPEC-014, PFS-M0-SPEC-015 |

## 1. Mục đích

Tài liệu xác định lộ trình phát triển PFS theo các milestone có ranh giới, đầu ra, điều kiện đầu vào và tiêu chí hoàn thành rõ ràng.

Mục tiêu là tránh:
- Triển khai kỹ thuật trước khi mô hình và governance được thống nhất.
- Xây dựng automation khi chưa có policy và permission model.
- Để AI agent tự diễn giải lại kiến trúc đã được phê duyệt.
- Đánh đồng việc hoàn thành tài liệu với việc hoàn thành implementation.
- Chuyển milestone khi chưa có bằng chứng nghiệm thu.

## 2. Nguyên tắc lập lộ trình

1. **Foundation before automation:** xác định mô hình, authority và policy trước khi tự động hóa.
2. **Governance before autonomy:** agent chỉ được thực hiện hành động trong phạm vi đã cấp quyền.
3. **Deterministic enforcement:** các quy tắc quan trọng phải được kiểm tra bằng cơ chế xác định, không phụ thuộc riêng vào lời nhắc AI.
4. **Incremental delivery:** mỗi milestone tạo ra đầu ra có thể kiểm tra độc lập.
5. **Evidence-based acceptance:** milestone chỉ được chấp nhận khi có evidence đáp ứng acceptance criteria.
6. **No implicit scope expansion:** thay đổi phạm vi phải đi qua change management.
7. **Preserve universal scope:** PFS phải hỗ trợ nhiều loại project; không biến Rust thành yêu cầu công nghệ của mọi project được khởi tạo.

## 3. Tổng quan roadmap

| Milestone | Tên | Trọng tâm | Kết quả chính |
|---|---|---|---|
| M0 | Foundation Definition | Phương pháp, mô hình, governance, policy | Bộ đặc tả nền tảng được owner phê duyệt |
| M1 | Documentation & Architecture | Kiến trúc hệ thống PFS và tài liệu kỹ thuật | Architecture baseline và tài liệu thiết kế |
| M2 | Universal Agent System | Agent lifecycle, identity, tools, permissions | Agent system có kiểm soát |
| M3 | Validation & Quality Gates | Validation, traceability, quality enforcement | Bộ kiểm tra và nghiệm thu có thể thực thi |
| M4 | Generator Automation | Sinh project foundation an toàn, lặp lại được | Generator và quy trình bootstrap |

Thứ tự trên là dependency order. Không được coi việc bắt đầu một milestone sau là bằng chứng milestone trước đã được nghiệm thu.

## 4. M0 — Foundation Definition

### 4.1 Mục tiêu

Xác định PFS là sản phẩm gì, phục vụ đối tượng nào, quản lý project ra sao, ai có quyền quyết định, agent được phép làm gì và đầu ra thế nào mới được coi là đạt.

### 4.2 Phạm vi

- Product vision và product definition.
- Universal Project Model.
- Project profile và capability model.
- Foundation lifecycle.
- Architecture View Model.
- Governance và decision authority.
- Artifact identity và traceability.
- Hybrid execution.
- Agent security và permission model.
- Quality và acceptance model.
- Version/change management.
- Security, data classification và supply chain.
- Roadmap và acceptance criteria.

### 4.3 Deliverables

Toàn bộ 16 tài liệu trong `docs/M0-foundation/`, từ `00-M0-INDEX.md` đến `15-M0-REVIEW-REPORT.md`.

### 4.4 Exit criteria

- Tất cả tài liệu có metadata và Document ID hợp lệ.
- Requirement ID được đăng ký duy nhất trong Global Requirement Registry.
- Các authority domain được xác định.
- Các xung đột giữa tài liệu đã được giải quyết hoặc ghi nhận thành quyết định đang chờ.
- AC-01..AC-28 có mapping đến requirement và evidence.
- Project Owner review và phê duyệt rõ ràng.
- Không còn Critical finding chưa được xử lý hoặc chấp thuận ngoại lệ hợp lệ.

M0 chỉ được chuyển `Accepted` sau khi đáp ứng các điều kiện trên. Việc viết xong tài liệu không tự động tạo ra trạng thái Accepted.

## 5. M1 — Documentation & Architecture

### 5.1 Mục tiêu

Chuyển các quyết định M0 đã được phê duyệt thành kiến trúc và tài liệu kỹ thuật có thể triển khai.

### 5.2 Phạm vi

- System context và system boundary.
- Logical architecture và module boundaries.
- Component responsibilities và dependency rules.
- Data architecture và persistence boundaries.
- Interface, contract và integration model.
- Security architecture.
- Deployment architecture.
- Operational architecture.
- Architecture Decision Records.
- Technical requirements và architecture traceability.

### 5.3 Deliverables dự kiến

- Architecture baseline.
- Architecture Decision Records.
- Module/dependency map.
- Interface và contract specifications.
- Data model và migration strategy.
- Threat model ở cấp kiến trúc.
- Architecture validation checklist.
- M1 acceptance evidence.

### 5.4 Exit criteria

- Mỗi architecture decision có owner, rationale, status và impact.
- Không có dependency trái với boundary đã phê duyệt.
- Các architecture view nhất quán với Universal Project Model.
- Requirements có traceability đến architecture element.
- Security và failure boundaries được xem xét.
- Các lựa chọn kỹ thuật có lý do và giới hạn rõ ràng.
- Architecture baseline được Project Owner hoặc người được ủy quyền phê duyệt.

### 5.5 Giới hạn

M1 không được tự ý sửa đổi product scope, governance authority hoặc permission model của M0. Thay đổi phải được xử lý như một change request.

## 6. M2 — Universal Agent System

### 6.1 Mục tiêu

Xây dựng hệ thống agent có thể phối hợp nhiều AI provider và nhiều loại agent nhưng vẫn chịu sự kiểm soát thống nhất của PFS.

### 6.2 Phạm vi

- Agent definition và identity.
- Agent session và lifecycle.
- Role, capability và permission binding.
- Provider/model abstraction.
- Tool registry và tool execution boundary.
- Task assignment và orchestration.
- Multi-agent coordination.
- Conflict/disagreement recording.
- Context management và artifact access.
- Audit events.
- Revocation và session termination.
- Policy enforcement.

### 6.3 Deliverables dự kiến

- Agent system architecture.
- Agent identity/session contract.
- Provider adapter contract.
- Tool execution contract.
- Permission enforcement mechanism.
- Agent orchestration workflow.
- Conflict and escalation workflow.
- Security test suite.
- M2 acceptance evidence.

### 6.4 Exit criteria

- Không có agent nào tự cấp quyền cho chính mình.
- Provider/model không quyết định quyền truy cập.
- Mọi tool execution được kiểm tra authorization.
- Quyền được giới hạn theo project, resource, operation, environment và session khi thích hợp.
- Có audit trail cho hành động quan trọng.
- Có cơ chế revoke và xử lý session bất thường.
- Multi-agent consensus không thay thế owner approval.
- Có test cho prompt injection, privilege escalation và data exfiltration.

## 7. M3 — Validation & Quality Gates

### 7.1 Mục tiêu

Chuyển các yêu cầu chất lượng và acceptance thành các cơ chế validation có thể thực thi, có evidence và có khả năng ngăn chặn việc chuyển trạng thái không hợp lệ.

### 7.2 Phạm vi

- Requirement validation.
- Artifact validation.
- Schema và contract validation.
- Cross-reference validation.
- Traceability validation.
- Policy validation.
- Security validation.
- Quality gates.
- Critical finding management.
- Evidence collection.
- Reproducibility.
- Independent review support.

### 7.3 Deliverables dự kiến

- Validation framework.
- Rule/catalog registry.
- Quality gate definitions.
- Evidence schema.
- Finding lifecycle.
- Requirement coverage report.
- Acceptance report.
- M3 test suite.

### 7.4 Exit criteria

- Các critical gate có pass/fail xác định.
- Critical failure không thể bị bù bằng điểm chất lượng tổng.
- Không thể đánh dấu Accepted khi còn critical finding chưa xử lý.
- Mọi exception có owner, rationale, scope, expiry/review date và compensating controls nếu cần.
- Evidence có provenance và liên kết đến requirement.
- Kết quả validation có thể tái lập trong điều kiện đã ghi nhận.

## 8. M4 — Generator Automation

### 8.1 Mục tiêu

Tạo project foundation theo profile và capability đã chọn, bảo đảm quá trình sinh file có thể preview, kiểm tra, thực hiện an toàn và kiểm toán.

### 8.2 Phạm vi

- Project initialization.
- Profile/capability resolution.
- Template and asset resolution.
- Artifact generation.
- Ownership manifest.
- Dry-run và preview.
- Conflict detection.
- Idempotent execution.
- Staging và validation.
- Recovery.
- Baseline creation.
- Bootstrap handoff.

### 8.3 Deliverables dự kiến

- Generator architecture.
- Template/asset registry.
- Generation manifest.
- Dry-run/preview workflow.
- Conflict detection.
- Safe write mechanism.
- Recovery workflow.
- Bootstrap baseline.
- M4 acceptance evidence.

### 8.4 Exit criteria

- Không ghi đè file ngoài quyền được cấp.
- Phát hiện xung đột trước khi thay đổi dữ liệu.
- Có preview hoặc dry-run trước thao tác có rủi ro.
- Generation operation có record và manifest.
- Có thể chạy lại mà không tạo thay đổi ngoài dự kiến.
- Có staging, validation và recovery path.
- Generated artifacts có provenance.
- Project được sinh ra có thể tiếp tục phát triển độc lập với PFS.

## 9. Dependency và điều kiện chuyển milestone

| Milestone | Phụ thuộc | Điều kiện chuyển |
|---|---|---|
| M0 | Không | Owner-approved foundation baseline |
| M1 | M0 | Architecture baseline accepted |
| M2 | M0, M1 | Agent system security và contract được nghiệm thu |
| M3 | M0, M1; tích hợp với M2 khi cần | Validation và quality gates có evidence |
| M4 | M0, M1, M3; tích hợp M2 khi cần | Generator vượt qua safety, idempotency và recovery tests |

Có thể thực hiện nghiên cứu hoặc prototype song song nếu không làm thay đổi baseline đã phê duyệt. Prototype không được coi là production capability.

## 10. Change control giữa các milestone

Mọi thay đổi có thể ảnh hưởng đến milestone đã duyệt phải có:

- Change ID.
- Requester và thời điểm.
- Lý do và vấn đề cần giải quyết.
- Domain bị ảnh hưởng.
- Requirements và artifacts liên quan.
- Security, compatibility và operational impact.
- Alternatives đã xem xét.
- Decision authority.
- Approval status.
- Migration hoặc remediation plan.
- Verification evidence.

Nếu change làm mất hiệu lực quyết định hoặc requirement của milestone trước, phải đánh giá lại các milestone phụ thuộc.

## 11. Milestone status

Các trạng thái chuẩn:

- `Planned`: đã được đưa vào roadmap.
- `In Progress`: đang thực hiện.
- `In Review`: đã có deliverables, đang review.
- `Blocked`: có dependency hoặc finding ngăn tiến độ.
- `Accepted`: đã đáp ứng exit criteria và có approval.
- `Rejected`: không được chấp nhận.
- `Deferred`: được hoãn bằng quyết định có thẩm quyền.

Không dùng `Completed` thay cho `Accepted` nếu chưa có acceptance decision.

## 12. Ranh giới công nghệ

Rust là công nghệ triển khai PFS Core theo định hướng hiện tại. Đây không phải yêu cầu bắt buộc đối với project được PFS tạo ra.

PFS phải hỗ trợ project profile khai báo công nghệ, runtime, platform và constraints riêng. Generator không được mặc định áp đặt stack của PFS lên project đích.

## 13. Requirement references

Các yêu cầu roadmap được đăng ký trong Global Requirement Registry:

- `M0-RDM-001`: Milestone có objective, scope, deliverables và exit criteria.
- `M0-RDM-002`: Dependency giữa milestone được khai báo rõ.
- `M0-RDM-003`: Milestone transition cần evidence và approval.
- `M0-RDM-004`: Change control bảo vệ baseline đã duyệt.
- `M0-RDM-005`: Phân biệt công nghệ triển khai PFS với công nghệ project đích.

## 14. Approval

| Vai trò | Trách nhiệm | Trạng thái |
|---|---|---|
| Project Owner | Phê duyệt roadmap và scope | Pending |
| Project Architect | Review dependency và architecture impact | Pending |
| Security Reviewer | Review security gates | Pending |
| Independent Auditor | Review evidence khi được chỉ định | Pending |

**Trạng thái tài liệu:** Proposed — Awaiting Owner Approval.
