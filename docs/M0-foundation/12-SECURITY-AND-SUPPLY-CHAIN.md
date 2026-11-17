# PFS-M0-SPEC-012 — Security and Supply Chain

**Document ID:** PFS-M0-SPEC-012  
**Document Type:** Data Security, Provenance and Supply Chain Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-003, PFS-M0-SPEC-005, PFS-M0-SPEC-007, PFS-M0-SPEC-008, PFS-M0-SPEC-009, PFS-M0-SPEC-010, PFS-M0-SPEC-011

---

## 1. Purpose

Tài liệu này xác định mô hình bảo mật dữ liệu và quản lý chuỗi cung ứng của PFS.

PFS sử dụng nhiều nguồn đầu vào:

- Project documents.
- External references.
- Templates.
- Agent skills.
- Workflows.
- Scripts.
- Plugins.
- Provider adapters.
- Dependencies.
- Generated artifacts.
- AI-generated content.

Các thành phần này có thể ảnh hưởng trực tiếp đến bảo mật, tính toàn vẹn và độ tin cậy của foundation.

Mục tiêu:

- Phân loại và bảo vệ dữ liệu.
- Kiểm soát nguồn gốc templates, skills và workflows.
- Ngăn đưa mã hoặc chỉ dẫn độc hại vào PFS.
- Kiểm soát dependency và external integrations.
- Bảo vệ secrets.
- Đảm bảo dữ liệu gửi đến AI providers đúng policy.
- Duy trì provenance và integrity.

## 2. Security Principles

PFS MUST áp dụng:

1. Data Classification.
2. Data Minimization.
3. Source Provenance.
4. Integrity Verification.
5. Explicit Trust.
6. Dependency Transparency.
7. License Awareness.
8. Least Privilege.
9. Secure Defaults.
10. Controlled Updates.
11. Reproducible Supply Chain.
12. Continuous Risk Assessment.

Không coi một template, skill hoặc package là an toàn chỉ vì nó có vẻ hữu ích hoặc được tải từ nguồn phổ biến.

## 3. Data Classification

PFS sử dụng bốn mức phân loại dữ liệu.

### 3.1. Public

Dữ liệu có thể công khai.

Ví dụ:

- Public project descriptions.
- Public documentation.
- Public specifications.
- Public source references.

Yêu cầu:

- Không chứa secrets.
- Có thể chia sẻ theo mục đích.
- Vẫn phải kiểm tra tính chính xác và license.

### 3.2. Internal

Dữ liệu chỉ dành cho phạm vi nội bộ được phép.

Ví dụ:

- Internal project notes.
- Internal architecture drafts.
- Non-public operational information.
- Internal workflow descriptions.

Yêu cầu:

- Chỉ chia sẻ với authorized actors.
- Không mặc định gửi đến external providers.
- Ghi nhận khi truyền ra ngoài nếu policy yêu cầu.

### 3.3. Confidential

Dữ liệu có thể gây thiệt hại đáng kể nếu tiết lộ trái phép.

Ví dụ:

- Commercial strategy.
- Non-public customer information.
- Proprietary business logic.
- Sensitive project architecture.
- Confidential contracts.

Yêu cầu:

- Restricted access.
- Purpose limitation.
- Explicit provider approval.
- Data minimization.
- Controlled storage and transfer.
- Appropriate audit.

### 3.4. Restricted

Dữ liệu có mức độ nhạy cảm hoặc hậu quả lộ lọt rất cao.

Ví dụ:

- Credentials.
- Private keys.
- Authentication secrets.
- Highly sensitive personal data.
- Critical infrastructure access material.
- Data subject to strict legal or contractual restrictions.

Yêu cầu:

- Strict access control.
- Strong protection at rest and in transit.
- Explicit authorization.
- No default external AI transfer.
- No exposure in prompts, logs or generated documentation.
- Auditable access.
- Retention and deletion controls.

### 3.5. Classification Rules

- Mỗi artifact SHOULD có classification.
- Classification của derived data không được tự động thấp hơn nguồn nếu chưa có declassification decision.
- Khi classification chưa rõ, áp dụng mức bảo vệ thận trọng cho đến khi được xác định.
- Classification phải xét cả nội dung và context.
- Public data không mặc nhiên được phép sử dụng cho mọi mục đích hoặc mọi provider.

## 4. Data Handling Lifecycle

PFS phải kiểm soát dữ liệu qua các giai đoạn:

1. Collection.
2. Classification.
3. Storage.
4. Processing.
5. Retrieval.
6. Transformation.
7. External Transfer.
8. Retention.
9. Archival.
10. Deletion.

Mỗi giai đoạn phải có controls phù hợp.

### 4.1. Data Collection

Khi tiếp nhận dữ liệu, PFS SHOULD ghi nhận:

- Source.
- Purpose.
- Owner.
- Classification.
- Consent hoặc legal basis khi cần.
- Provenance.
- Integrity information.

Không thu thập dữ liệu vượt quá nhu cầu của project.

### 4.2. Data Storage

PFS SHOULD hỗ trợ:

- Encryption at rest khi phù hợp.
- Encryption in transit.
- Access control.
- Storage isolation.
- Backup protection.
- Integrity checks.
- Retention policy.

### 4.3. Data Transformation

Khi chuyển đổi dữ liệu:

- Giữ provenance.
- Ghi nhận transformation.
- Giữ classification phù hợp.
- Không làm mất các constraints quan trọng.
- Kiểm tra integrity của output.

### 4.4. External Transfer

Trước khi chuyển dữ liệu đến provider, plugin hoặc external service, phải kiểm tra:

- Destination.
- Purpose.
- Classification.
- Authorization.
- Provider policy.
- Contractual constraints.
- Data minimization.
- Retention implications.

## 5. AI Provider Data Governance

Mỗi AI provider SHOULD có provider data profile.

Profile có thể chứa:

- Provider ID.
- Approved purposes.
- Supported data classifications.
- Data retention characteristics.
- Training/data-use policy.
- Processing region nếu được công bố.
- Security commitments.
- Contractual restrictions.
- Required user consent.
- Adapter version.
- Last reviewed date.

Không được giả định mọi provider có cùng chính sách lưu trữ hoặc sử dụng dữ liệu.

### 5.1. Provider Eligibility

Provider chỉ được sử dụng cho một task khi đáp ứng policy của project và data classification.

Ví dụ:

- Public: Có thể dùng provider được phê duyệt cho public data.
- Internal: Cần đánh giá điều kiện xử lý.
- Confidential: Cần explicit approval và kiểm tra data handling.
- Restricted: Mặc định không external transfer; chỉ cho phép theo một policy riêng đã được phê duyệt và đáp ứng yêu cầu pháp lý, hợp đồng, bảo mật.

### 5.2. Context Minimization

Agent chỉ được gửi phần context cần thiết.

Không tự động gửi:

- Toàn bộ project repository.
- Toàn bộ document library.
- Secrets.
- Không liên quan đến task.
- Restricted data không được phép.

### 5.3. Provider Changes

Khi provider thay đổi policy, model behavior hoặc retention conditions, PFS SHOULD đánh giá lại provider eligibility.

Không coi provider approval là vĩnh viễn.

## 6. Template Supply Chain

Templates có thể chứa:

- Content.
- Instructions.
- Scripts.
- Placeholders.
- Configuration.
- External references.
- Dependencies.

PFS phải coi templates bên ngoài là untrusted cho đến khi được kiểm tra.

### 6.1. Template Registry

Mỗi template SHOULD có:

- Template ID.
- Name.
- Version.
- Publisher.
- Source.
- License.
- Content hash.
- Supported project types.
- Compatibility range.
- Required capabilities.
- Dependencies.
- Security classification.
- Review status.
- Validation status.
- Provenance.

### 6.2. Template Review

Trước khi đưa vào trusted template catalog, cần xem xét:

- Instruction integrity.
- Embedded scripts.
- External references.
- File overwrite behavior.
- Data access.
- Dependencies.
- License.
- Compatibility.
- Security risks.

### 6.3. Template Trust States

- Unreviewed.
- Under Review.
- Approved.
- Restricted.
- Rejected.
- Deprecated.
- Revoked.

Không tự động thực thi script chỉ vì template đã được Approved.

Template approval và execution permission là hai quyết định riêng biệt.

## 7. Agent Skill and Workflow Supply Chain

Skills và workflows có thể làm thay đổi hành vi agent.

Mỗi skill/workflow SHOULD có:

- Stable ID.
- Version.
- Author/publisher.
- Source.
- License.
- Content hash.
- Required capabilities.
- Tool dependencies.
- Data access requirements.
- Side-effect declaration.
- Compatibility.
- Security review.
- Approval status.

### 7.1. Skill Installation

Trước khi cài đặt:

- Validate identity.
- Verify provenance.
- Inspect instructions.
- Inspect referenced tools.
- Inspect scripts.
- Check license.
- Check compatibility.
- Review permissions.
- Identify external communications.

### 7.2. Workflow Execution

Workflow MUST NOT tự cấp quyền vượt policy.

Workflow không được thực thi privileged operations chỉ vì instructions của workflow yêu cầu.

PFS Core phải kiểm tra authorization độc lập.

### 7.3. Revocation

Khi skill hoặc workflow có vấn đề:

- Mark Restricted hoặc Revoked.
- Ngăn sử dụng mới.
- Xác định projects bị ảnh hưởng.
- Xác định artifacts được tạo từ nó.
- Đánh giá có cần revalidation không.
- Ghi incident hoặc supply-chain finding.

## 8. Software Dependency Supply Chain

PFS Core được triển khai bằng Rust, nhưng dependency policy phải áp dụng cho mọi thành phần liên quan.

### 8.1. Dependency Inventory

PFS SHOULD ghi nhận:

- Package name.
- Version.
- Source registry.
- Publisher.
- License.
- Integrity hash hoặc checksum.
- Direct/transitive dependency.
- Compatibility.
- Security advisories.
- Update status.

### 8.2. Dependency Policy

Dependencies phải được đánh giá theo:

- Necessity.
- Maintenance status.
- Security history.
- License compatibility.
- Provenance.
- Transitive dependencies.
- Platform compatibility.
- Reproducibility.

Không thêm dependency chỉ vì thuận tiện nếu có thể đáp ứng yêu cầu bằng capability hiện có mà không làm tăng rủi ro đáng kể.

### 8.3. Dependency Pinning

Production/reproducible builds SHOULD pin dependency versions và xác minh lockfiles.

Không sử dụng floating dependencies trong một baseline cần tái tạo mà không có policy kiểm soát.

### 8.4. Vulnerability Handling

Khi phát hiện vulnerability:

1. Xác định affected components.
2. Xác định severity và exploitability.
3. Xác định project scope.
4. Đánh giá exposure.
5. Xây dựng remediation plan.
6. Validate fix.
7. Ghi evidence.
8. Cập nhật baseline nếu cần.

Không chỉ dựa vào severity score mà bỏ qua context thực tế.

## 9. Script and Executable Supply Chain

Scripts có thể gây tác động lớn hơn tài liệu thông thường.

Trước khi thực thi script bên ngoài, PFS SHOULD:

- Identify source.
- Inspect content.
- Verify integrity.
- Review permissions.
- Review network access.
- Review filesystem access.
- Review external side effects.
- Define execution environment.
- Define timeout and resource limits.
- Define recovery strategy.

Script không được tự động chạy trong môi trường privileged chỉ vì được tham chiếu từ một workflow đã được phê duyệt.

## 10. License and Intellectual Property

PFS phải hỗ trợ license awareness cho:

- Templates.
- Skills.
- Workflows.
- Source code.
- Documentation.
- Dependencies.
- Imported assets.
- Generated artifacts khi có nguồn có điều kiện license.

License metadata SHOULD ghi:

- License identifier.
- Source.
- Copyright holder nếu biết.
- Attribution requirements.
- Redistribution restrictions.
- Modification conditions.
- Commercial use conditions.
- Compatibility concerns.

Không được tự kết luận một tài sản không có license là tài sản public domain.

License compatibility phải được đánh giá theo cách sử dụng và phân phối thực tế.

## 11. Provenance and Integrity

PFS SHOULD hỗ trợ:

- Content hash.
- Source reference.
- Publisher identity.
- Version.
- Signature verification khi có.
- Import timestamp.
- Review record.
- Validation evidence.
- Dependency graph.

### 11.1. Hash Limitations

Hash hỗ trợ phát hiện nội dung thay đổi.

Hash không chứng minh:

- Publisher là đáng tin.
- Nội dung an toàn.
- License hợp lệ.
- Instructions không độc hại.

### 11.2. Signature Limitations

Signature chỉ có giá trị khi signing identity và trust policy được xác minh.

Không được coi mọi chữ ký hợp lệ về mặt kỹ thuật là bằng chứng tuyệt đối về độ an toàn.

## 12. Updates and Revocation

Supply-chain updates phải có kiểm soát.

PFS SHOULD:

- Track new versions.
- Track security advisories.
- Detect changed hashes.
- Detect revoked publishers or packages.
- Assess compatibility.
- Assess license changes.
- Require approval when policy demands.
- Revalidate affected outputs.

Không tự động cập nhật một trusted component sang version mới mà chưa đánh giá compatibility và security impact.

## 13. Generated Artifact Supply Chain

Generated artifacts phải giữ được nguồn gốc:

- Generation task.
- Generator version.
- Template version.
- Input artifacts.
- Agent instruction version nếu liên quan.
- Tool versions.
- Relevant provider metadata.
- Transformation history.
- Validation results.
- Approval state.

Generated artifact không tự động trở thành trusted chỉ vì được tạo bởi PFS.

## 14. Backup, Retention and Deletion

PFS SHOULD có chính sách cho:

- Backup.
- Restore.
- Retention.
- Archival.
- Secure deletion.
- Audit history.
- Legal hold.

Backup phải có classification và access controls tương ứng với dữ liệu gốc.

Deletion phải xem xét:

- Retention obligations.
- Baseline references.
- Audit requirements.
- Backup copies.
- External provider copies.
- Legal requirements.

Không tuyên bố dữ liệu đã bị xóa hoàn toàn nếu PFS không kiểm soát tất cả bản sao và external retention systems.

## 15. Supply Chain Incident Response

Các tình huống cần xử lý:

- Malicious template.
- Compromised dependency.
- Malicious skill.
- Prompt injection embedded in workflow.
- Compromised provider credential.
- Unexpected data transfer.
- Tampered package.
- License violation.
- Unauthorized script execution.

Quy trình:

1. Detect.
2. Classify.
3. Contain.
4. Identify affected components.
5. Identify affected projects and artifacts.
6. Revoke or quarantine.
7. Assess impact.
8. Remediate.
9. Validate.
10. Record evidence.
11. Review lessons learned.

## 16. Security and Supply Chain Requirements

| ID | Requirement |
|---|---|
| M0-SC-001 | PFS MUST support four data classification levels. |
| M0-SC-002 | PFS MUST preserve classification through transformations unless authorized declassification occurs. |
| M0-SC-003 | PFS MUST control external data transfer. |
| M0-SC-004 | PFS MUST define provider data handling profiles. |
| M0-SC-005 | PFS MUST maintain template provenance. |
| M0-SC-006 | PFS MUST review external templates before trusted use. |
| M0-SC-007 | PFS MUST maintain skill and workflow provenance. |
| M0-SC-008 | PFS MUST enforce permissions independently of skill instructions. |
| M0-SC-009 | PFS MUST maintain dependency inventory. |
| M0-SC-010 | PFS MUST support dependency version pinning for reproducible builds. |
| M0-SC-011 | PFS MUST track license information where available and applicable. |
| M0-SC-012 | PFS MUST control execution of external scripts. |
| M0-SC-013 | PFS MUST support integrity verification for imported components. |
| M0-SC-014 | PFS MUST support component revocation or quarantine. |
| M0-SC-015 | PFS MUST preserve generation provenance. |
| M0-SC-016 | PFS MUST define supply-chain incident response. |
| M0-SC-017 | PFS MUST NOT treat hashes as proof of trustworthiness. |
| M0-SC-018 | PFS MUST NOT assume that unlicensed assets are free to use. |
| M0-SC-019 | PFS MUST NOT send Restricted data externally by default. |
| M0-SC-020 | PFS MUST identify affected artifacts when a trusted source is revoked. |

## 17. M1, M2 and M4 Design Dependencies

M1 phải định nghĩa:

- Data Classification Schema.
- Provider Data Profile.
- Template Registry Contract.
- Skill/Workflow Registry Contract.
- Dependency Inventory Schema.
- Provenance Contract.
- Integrity Verification Contract.
- License Metadata Schema.
- Supply Chain Incident Contract.

M2 phải áp dụng các controls cho:

- Agent skills.
- Workflows.
- Tool integrations.
- Provider adapters.
- Agent context and data access.

M4 phải áp dụng controls cho:

- Template import.
- Dependency verification.
- File generation.
- Script execution.
- Artifact provenance.
- Integrity manifest.

M3 phải kiểm tra:

- Data classification enforcement.
- External transfer controls.
- Provenance completeness.
- Dependency integrity.
- License metadata.
- Revocation behavior.
- Incident response scenarios.

---

**End of Document — PFS-M0-SPEC-012 v1.1.0**
