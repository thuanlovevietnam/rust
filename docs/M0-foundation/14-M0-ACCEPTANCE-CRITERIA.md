# PFS-M0-SPEC-014 — M0 Acceptance Criteria

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M0-SPEC-014 |
| Tên | M0 Acceptance Criteria and Verification Matrix |
| Version | 1.1.0 |
| Status | Proposed — Awaiting Owner Approval |
| Phase | M0 — Foundation Definition |
| Authority | Project Owner |
| Classification | Internal |
| Parent specification | PFS-M0-SPEC-001 |
| Related specifications | PFS-M0-SPEC-002..013, PFS-M0-SPEC-015 |

## 1. Mục đích

Tài liệu quy định các điều kiện để nghiệm thu M0. Mục đích là tạo một chuẩn kiểm tra khách quan, tránh việc chấp nhận M0 chỉ vì đã viết đủ tài liệu hoặc vì đánh giá chủ quan rằng thiết kế có vẻ hoàn chỉnh.

M0 là milestone xác định foundation methodology, product model, governance, security, quality và roadmap. M0 không đồng nghĩa với việc PFS đã được implement hoặc đã vượt qua kiểm thử production.

## 2. Nguyên tắc acceptance

1. Mỗi criterion phải có kết quả kiểm tra và evidence.
2. Mỗi requirement phải có ID duy nhất và có traceability.
3. Critical failure là điều kiện chặn acceptance.
4. Không dùng điểm trung bình để bù cho lỗi Critical.
5. Exception phải được người có thẩm quyền phê duyệt.
6. Tài liệu Proposed không được coi là policy đã có hiệu lực.
7. Review report không thay thế independent audit.
8. Acceptance phải có quyết định rõ ràng của Project Owner.
9. Không suy diễn rằng một tiêu chí đã đạt khi chưa có evidence.
10. Mọi finding còn mở phải được công khai trong acceptance report.

## 3. Acceptance states

| Trạng thái | Ý nghĩa |
|---|---|
| `Not Assessed` | Chưa đánh giá |
| `Pass` | Đáp ứng tiêu chí, có evidence |
| `Fail` | Không đáp ứng |
| `Blocked` | Chưa thể đánh giá do thiếu dependency/evidence |
| `Accepted with Exception` | Được chấp thuận ngoại lệ theo authority |
| `Not Applicable` | Không áp dụng, có rationale và approval khi cần |

Không được dùng `Not Assessed`, `Blocked` hoặc `Not Applicable` để giả định rằng tiêu chí đã Pass.

## 4. Mức độ nghiêm trọng

- **Critical:** vi phạm authority, security boundary, integrity, traceability nền tảng hoặc có thể dẫn đến hành động trái phép. Chặn acceptance.
- **High:** rủi ro đáng kể đối với khả năng triển khai, kiểm soát hoặc duy trì hệ thống. Phải xử lý hoặc có exception hợp lệ trước acceptance.
- **Medium:** thiếu sót có ảnh hưởng giới hạn, cần có remediation plan.
- **Low:** cải tiến hoặc thiếu sót nhỏ, không làm mất hiệu lực baseline.

Exception không được sử dụng để hợp thức hóa hành vi trái pháp luật, vượt qua yêu cầu bảo mật bắt buộc hoặc che giấu một Critical failure.

## 5. Acceptance criteria AC-01..AC-28

### Nhóm A — Product và Universal Project Model

**AC-01 — Universal product scope**

- Kiểm tra: PFS được định nghĩa là hệ thống có thể hỗ trợ nhiều loại project, không chỉ software project.
- Evidence: Product Vision, Product Definition.
- Requirement mapping: `M0-PROD-001`.
- Severity: Critical.

**AC-02 — Project profile và capability model**

- Kiểm tra: có Project Profile, Capability Model và cơ chế khai báo Required, Optional, Not Applicable.
- Evidence: Universal Project Model và ví dụ profile.
- Requirement mapping: `M0-UNI-001`, `M0-UNI-002`.
- Severity: High.

**AC-03 — Explicit N/A rationale**

- Kiểm tra: capability hoặc requirement được đánh dấu Not Applicable phải có lý do, phạm vi và authority phù hợp.
- Evidence: mẫu applicability record.
- Requirement mapping: `M0-UNI-003`.
- Severity: High.

**AC-04 — Tailorable foundation**

- Kiểm tra: foundation có thể điều chỉnh theo project profile nhưng không làm mất các invariant và mandatory controls.
- Evidence: tailoring rules và ví dụ.
- Requirement mapping: `M0-UNI-004`.
- Severity: High.

### Nhóm B — Architecture và methodology

**AC-05 — Architecture View Model**

- Kiểm tra: xác định đủ tám view: Context, Structure, Behavior, Data, Security, Interface, Deployment, Operations.
- Evidence: Architecture View Model.
- Requirement mapping: `M0-UNI-005`.
- Severity: High.

**AC-06 — Foundation lifecycle**

- Kiểm tra: lifecycle có các stage, input, output, gate, owner và transition rõ ràng.
- Evidence: Foundation Methodology.
- Requirement mapping: `M0-MTH-001`.
- Severity: High.

**AC-07 — Hybrid execution boundary**

- Kiểm tra: phân biệt AI reasoning với deterministic execution; AI không tự tạo authority.
- Evidence: Hybrid Execution Model.
- Requirement mapping: `M0-HYB-001`, `M0-HYB-002`.
- Severity: Critical.

### Nhóm C — Governance và authority

**AC-08 — Governance roles**

- Kiểm tra: các vai trò và trách nhiệm được định nghĩa, bao gồm Project Owner, Decision Approver, Project Architect, Security Reviewer, Operator, AI Agent, Independent Auditor và Observer.
- Evidence: Governance Model.
- Requirement mapping: `M0-GOV-001`.
- Severity: High.

**AC-09 — Separation of duties**

- Kiểm tra: proposal, approval, execution và verification được phân tách phù hợp; không mặc định một agent được tự phê duyệt hành động của mình.
- Evidence: role/authority matrix.
- Requirement mapping: `M0-GOV-002`, `M0-AUT-002`.
- Severity: Critical.

**AC-10 — Explicit authority**

- Kiểm tra: mỗi domain có authority owner, approval status và quy tắc giải quyết xung đột.
- Evidence: Authority Registry design và Decision Model.
- Requirement mapping: `M0-AUT-001`, `M0-AUT-003`.
- Severity: Critical.

**AC-11 — Decision traceability**

- Kiểm tra: quyết định có ID, rationale, alternatives, impact, approver và trạng thái.
- Evidence: Decision Record template.
- Requirement mapping: `M0-AUT-004`.
- Severity: High.

### Nhóm D — Artifact và traceability

**AC-12 — Stable artifact identity**

- Kiểm tra: artifact có định danh ổn định, loại, version, owner/authority và trạng thái.
- Evidence: Artifact Model.
- Requirement mapping: `M0-ART-001`.
- Severity: High.

**AC-13 — Global requirement registry**

- Kiểm tra: tất cả requirement ID duy nhất, có domain namespace và authoritative registry; không còn ID mơ hồ hoặc trùng.
- Evidence: Global Requirement Registry và uniqueness report.
- Requirement mapping: `M0-ART-002`.
- Severity: Critical.

**AC-14 — End-to-end traceability**

- Kiểm tra: requirement liên kết được với source document, decision, artifact, acceptance criterion và evidence tương ứng.
- Evidence: Traceability Matrix.
- Requirement mapping: `M0-ART-003`.
- Severity: High.

**AC-15 — Source-of-truth by domain**

- Kiểm tra: xác định nguồn có thẩm quyền theo từng domain/artifact; xử lý được trường hợp xung đột và tài liệu dẫn chiếu.
- Evidence: Authority/Artifact Registry design.
- Requirement mapping: `M0-AUT-005`, `M0-ART-004`.
- Severity: Critical.

### Nhóm E — Execution và agent security

**AC-16 — Deterministic policy enforcement**

- Kiểm tra: quyền và policy quan trọng được kiểm tra bằng enforcement mechanism xác định, không dựa riêng vào prompt hoặc lời cam kết của agent.
- Evidence: Hybrid Execution và Agent Security Model.
- Requirement mapping: `M0-HYB-003`, `M0-SEC-AG-001`.
- Severity: Critical.

**AC-17 — Permission levels**

- Kiểm tra: L0–L5 được định nghĩa, phân biệt và có điều kiện cấp quyền; quyền không được mặc định tăng theo độ tự chủ của agent.
- Evidence: Permission Matrix.
- Requirement mapping: `M0-SEC-AG-002`.
- Severity: Critical.

**AC-18 — Least privilege và scope isolation**

- Kiểm tra: permission giới hạn theo resource, operation, project, environment và session khi thích hợp; có ranh giới cách ly dữ liệu.
- Evidence: Agent Security Model và threat model.
- Requirement mapping: `M0-SEC-AG-003`, `M0-SEC-AG-004`.
- Severity: Critical.

**AC-19 — Tool, prompt injection và secret safety**

- Kiểm tra: có policy đối với tool execution, untrusted input, prompt injection, secret handling và data egress.
- Evidence: Security controls và threat scenarios.
- Requirement mapping: `M0-SEC-AG-005..010`.
- Severity: Critical.

### Nhóm F — Safe generation và recovery

**AC-20 — Safe generation**

- Kiểm tra: generation model có dry-run, preview, ownership, conflict detection, overwrite authorization và operation manifest.
- Evidence: Generation safety specification.
- Requirement mapping: `M0-HYB-004`, `M0-MTH-002`.
- Severity: Critical.

**AC-21 — Recovery và operation history**

- Kiểm tra: có staging, operation records, validation và recovery strategy; không tuyên bố rollback tuyệt đối nếu không bảo đảm được.
- Evidence: Recovery model và failure scenarios.
- Requirement mapping: `M0-HYB-005`.
- Severity: High.

### Nhóm G — Quality và acceptance

**AC-22 — Quality dimensions và critical gates**

- Kiểm tra: quality dimensions được xác định; critical gate có quyền chặn acceptance độc lập với aggregate score.
- Evidence: Quality Model.
- Requirement mapping: `M0-QLT-001..004`.
- Severity: Critical.

**AC-23 — Evidence-based verification**

- Kiểm tra: phân biệt verification với validation; evidence có nguồn, thời điểm, phạm vi và liên kết requirement.
- Evidence: Evidence Model.
- Requirement mapping: `M0-QLT-005..008`.
- Severity: High.

**AC-24 — Finding và exception lifecycle**

- Kiểm tra: finding có severity, owner, disposition và trạng thái; exception có approver, rationale, scope và thời hạn/review.
- Evidence: Finding/Exception templates.
- Requirement mapping: `M0-QLT-009..012`.
- Severity: High.

### Nhóm H — Version và supply chain

**AC-25 — Version domains và compatibility**

- Kiểm tra: phân biệt version của PFS, specification, project profile, template, agent, provider adapter và generated baseline; compatibility/migration được khai báo.
- Evidence: Version and Change Management.
- Requirement mapping: `M0-VER-001..008`.
- Severity: High.

**AC-26 — Change control**

- Kiểm tra: thay đổi có classification, impact analysis, authority, approval, migration và verification.
- Evidence: Change Management Model.
- Requirement mapping: `M0-VER-009..014`.
- Severity: High.

**AC-27 — Data classification và supply chain**

- Kiểm tra: có classification Public/Internal/Confidential/Restricted; provenance và kiểm soát nguồn đối với template, skill, workflow, dependency và script.
- Evidence: Security and Supply Chain Model.
- Requirement mapping: `M0-SC-001..014`.
- Severity: Critical.

**AC-28 — Final package integrity và owner approval**

- Kiểm tra: đủ 16 tài liệu; ID và cross-reference hợp lệ; requirement traceable; findings được xử lý; review/evidence package có thật; Project Owner phê duyệt rõ ràng.
- Evidence: package manifest, link validation, registry validation, review report, approval record.
- Requirement mapping: `M0-REV-001..020` và các requirement domain liên quan.
- Severity: Critical.

## 6. Requirement registry và mapping

### 6.1 Quy tắc định danh

Document ID và Requirement ID là hai loại định danh khác nhau.

- Document ID: `PFS-M0-SPEC-001` đến `PFS-M0-SPEC-016`.
- Review requirement: namespace `M0-REV`.
- Các domain requirement dùng namespace riêng.

Các namespace dự kiến:

| Namespace | Domain |
|---|---|
| `M0-PROD` | Product definition |
| `M0-UNI` | Universal Project Model |
| `M0-MTH` | Methodology |
| `M0-GOV` | Governance |
| `M0-AUT` | Authority and decisions |
| `M0-ART` | Artifact and traceability |
| `M0-HYB` | Hybrid execution |
| `M0-SEC-AG` | Agent security |
| `M0-QLT` | Quality |
| `M0-VER` | Version and change |
| `M0-SC` | Security and supply chain |
| `M0-RDM` | Roadmap |
| `M0-REV` | Review amendments and cross-document controls |

### 6.2 Quy tắc registry

Global Requirement Registry phải lưu ít nhất:

- Requirement ID.
- Requirement statement.
- Domain.
- Source Document ID.
- Requirement owner.
- Priority/severity.
- Status.
- Applicable project profile/capability.
- Related decisions.
- Acceptance criteria.
- Verification method.
- Evidence reference.
- Supersedes/superseded by, nếu có.

Registry là nguồn quản lý định danh và trạng thái requirement. Nội dung chi tiết của requirement được duy trì tại tài liệu domain có thẩm quyền. Registry không thay thế domain specification.

### 6.3 Quy tắc xử lý ID cũ

Các ID dạng `M0-REQ-001..020` trong review draft cũ không được tiếp tục dùng như ID chính thức vì không xác định domain và có nguy cơ trùng.

Phải:
1. Đối chiếu từng requirement cũ với requirement domain tương ứng.
2. Cấp ID mới theo namespace phù hợp.
3. Nếu là amendment xuyên tài liệu, cấp `M0-REV-xxx`.
4. Ghi mapping `legacy_id → canonical_id`.
5. Không tái sử dụng ID cũ cho requirement mới.
6. Không tuyên bố registry đã được kiểm tra uniqueness nếu chưa thực hiện kiểm tra thực tế.

## 7. Evidence requirements

Mỗi evidence record tối thiểu phải có:

- Evidence ID.
- Criterion ID.
- Requirement ID.
- Artifact/source reference.
- Verification method.
- Result.
- Execution date/time.
- Executor/reviewer.
- Tool/version hoặc điều kiện kiểm tra.
- Evidence location/hash nếu phù hợp.
- Limitations và assumptions.

Evidence phải đủ để reviewer khác hiểu điều gì đã được kiểm tra và kết quả có thể được tái lập đến mức phù hợp.

## 8. Điều kiện nghiệm thu tổng thể

M0 chỉ có thể được đề nghị `Accepted` khi:

1. AC-01..AC-28 đã được đánh giá.
2. Không còn Critical criterion ở trạng thái Fail hoặc Blocked.
3. Critical finding đã được xử lý hoặc có disposition hợp lệ không làm vi phạm mandatory control.
4. Mọi Not Applicable có rationale.
5. Global Requirement Registry được kiểm tra uniqueness.
6. Cross-reference và traceability được kiểm tra.
7. Evidence package được lưu và liên kết.
8. Review report nêu rõ limitations.
9. Project Owner đưa ra approval record.

High findings phải được đóng hoặc có exception được phê duyệt và có remediation plan trước khi acceptance.

## 9. Acceptance report template

### M0 Acceptance Summary

- Project: PFS
- Baseline version:
- Review date:
- Reviewer:
- Project Owner:
- Total criteria:
- Pass:
- Fail:
- Blocked:
- Accepted with Exception:
- Not Applicable:
- Open Critical findings:
- Open High findings:
- Evidence package:
- Recommendation:
- Owner decision:

### Owner decision

- `Accepted`
- `Accepted with Exception`
- `Rejected`
- `Deferred`

Approval record phải ghi người phê duyệt, thời điểm, baseline được phê duyệt, phạm vi, exception và các điều kiện kèm theo.

## 10. Trạng thái hiện tại

Tại thời điểm phát hành bản tài liệu này:

- Các acceptance criteria được định nghĩa ở mức specification.
- Chưa có bằng chứng rằng toàn bộ AC-01..AC-28 đã được thực thi.
- Chưa có kết quả kiểm tra tự động uniqueness của toàn bộ requirement IDs.
- Chưa có independent audit thực thi hoàn chỉnh.
- Chưa có Owner Approval Record.

Vì vậy, không được tuyên bố M0 đã Accepted.

**Trạng thái tài liệu:** Proposed — Awaiting Owner Approval.
