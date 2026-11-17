# PFS-M0-SPEC-009 — Agent Security Model

**Document ID:** PFS-M0-SPEC-009  
**Document Type:** Agent Security and Permission Specification  
**Project:** Project Foundation System (PFS)  
**Version:** 1.1.0  
**Status:** Accepted  
**Target Milestone:** M0 — Foundation Methodology  
**Related Documents:** PFS-M0-SPEC-003, PFS-M0-SPEC-005, PFS-M0-SPEC-006, PFS-M0-SPEC-007, PFS-M0-SPEC-008, PFS-M0-SPEC-010, PFS-M0-SPEC-012

---

## 1. Purpose

Tài liệu này xác định mô hình bảo mật cho AI agents, automation workers, provider adapters và các thành phần có khả năng đọc, tạo, sửa, thực thi hoặc truyền dữ liệu trong PFS.

Mục tiêu:

- Ngăn agent vượt quyền.
- Giới hạn phạm vi truy cập.
- Bảo vệ project data và secrets.
- Ngăn prompt injection và instruction hijacking.
- Kiểm soát tool execution và external side effects.
- Ngăn truy cập chéo project hoặc tenant.
- Duy trì auditability.
- Hỗ trợ multi-agent trong một security boundary thống nhất.

Bảo mật phải được thiết kế như một thuộc tính xuyên suốt, không phải một bước kiểm tra bổ sung sau khi agent đã thực thi.

## 2. Security Principles

PFS MUST tuân thủ các nguyên tắc:

1. Least Privilege.
2. Explicit Authorization.
3. Default Deny.
4. Project and Resource Isolation.
5. Separation of Duties.
6. No Implicit Trust.
7. Data Minimization.
8. Defense in Depth.
9. Auditable Operations.
10. Fail Secure.
11. Human Authority Preservation.
12. Revocable Access.

Không được coi AI model, agent, plugin, template hoặc provider là trusted chỉ vì chúng thuộc hệ thống PFS.

## 3. Security Boundary

PFS phải xác định boundary giữa:

- Project Owner.
- Human Operators.
- AI Agents.
- Agent Coordinator.
- Tool Executors.
- Rust Core.
- Provider Adapters.
- External AI Providers.
- Plugins and Connectors.
- Filesystem.
- Network Services.
- Project Data.
- Secrets and Credentials.

Mỗi boundary phải có quy tắc xác thực, authorization, data flow và audit phù hợp.

### 3.1. Trusted Core

Rust Core là nơi thực thi các policy và permission rules có tính quyết định.

AI agent không được tự quyết định permission của chính nó.

Một permission request do agent tạo ra chỉ là đề xuất, không phải authorization.

### 3.2. Untrusted Inputs

Các nguồn sau mặc định phải được coi là untrusted:

- User-provided documents.
- External websites.
- Retrieved files.
- Code repositories.
- Templates từ nguồn bên ngoài.
- Agent-generated content.
- Tool output.
- Provider response.
- Plugin response.
- Imported project configuration.

Nội dung untrusted không được phép tự thay đổi system policy hoặc grant permission.

## 4. Identity Model

PFS SHOULD phân biệt:

- Human Identity.
- Project Identity.
- Agent Identity.
- Provider Identity.
- Tool Identity.
- Execution Identity.
- Resource Identity.

Mỗi identity phải có định danh phù hợp với phạm vi hoạt động.

### 4.1. Agent Identity

Agent identity SHOULD bao gồm:

- Agent ID.
- Agent role.
- Agent configuration version.
- Project scope.
- Session scope.
- Authorized capabilities.
- Status.
- Provenance.

Agent identity không đồng nghĩa với human identity.

Agent không được sử dụng danh tính của Project Owner để vượt quyền.

### 4.2. Session Identity

Mỗi execution session SHOULD có định danh riêng.

Session phải xác định:

- Initiating actor.
- Project.
- Agent.
- Task.
- Permission context.
- Start time.
- Expiration.
- Status.

Không sử dụng một session vô thời hạn làm quyền mặc định cho các task tương lai.

## 5. Authentication and Authorization

Authentication trả lời: actor là ai?

Authorization trả lời: actor được phép thực hiện thao tác nào trên resource nào trong điều kiện nào?

Hai khái niệm này MUST được phân biệt.

### 5.1. Authorization Attributes

Quyết định authorization SHOULD xét:

- Actor.
- Role.
- Permission.
- Project.
- Resource.
- Operation.
- Environment.
- Data classification.
- Session.
- Time constraints.
- Approval reference.
- Policy conditions.

Không cấp quyền chỉ dựa trên tên agent hoặc tên model.

### 5.2. Default Deny

Nếu không xác định được quyền:

- Từ chối operation.
- Không tự suy diễn rằng operation được phép.
- Ghi nhận authorization failure.
- Yêu cầu authority phù hợp xem xét nếu cần.

## 6. Logical Permission Levels

PFS sử dụng logical permission levels sau làm mô hình khái niệm:

| Level | Capability | Allowed Behavior |
|---|---|---|
| L0 | Read-only | Đọc resource được cấp quyền |
| L1 | Analyze / Propose | Phân tích và đề xuất |
| L2 | Draft Artifacts | Tạo bản nháp trong vùng cho phép |
| L3 | Modify Authorized Files | Sửa file được cấp quyền |
| L4 | Execute Approved Operations | Chạy script, test và operation đã được phép |
| L5 | Privileged / Destructive | Thao tác đặc quyền hoặc có nguy cơ phá hủy |

### 6.1. Permission Constraints

Level không phải quyền truy cập toàn cục.

Ví dụ: agent L3 trong project A không mặc nhiên có L3 trong project B.

Permission phải giới hạn theo:

- Resource.
- Operation.
- Scope.
- Environment.
- Session.
- Conditions.

L5 không được hiểu là quyền vô hạn hoặc bỏ qua security policy.

### 6.2. Permission Escalation

Agent không được tự nâng permission.

Quy trình đề xuất:

1. Agent xác định cần thêm quyền.
2. Agent tạo permission request.
3. PFS đánh giá scope và risk.
4. Authority phù hợp phê duyệt nếu policy yêu cầu.
5. Core cấp quyền có giới hạn.
6. Operation được ghi audit.
7. Quyền hết hạn hoặc bị thu hồi theo policy.

## 7. Separation of Duties

PFS SHOULD tách các vai trò:

- Proposer.
- Approver.
- Executor.
- Verifier.
- Auditor.

Đối với operation critical hoặc destructive, SHOULD tránh để cùng một actor tự đề xuất, tự phê duyệt, tự thực thi và tự xác nhận thành công.

Nếu dự án nhỏ không có đủ người cho mọi vai trò, phải áp dụng compensating controls như independent validation, explicit owner approval và immutable audit records.

## 8. Project and Tenant Isolation

PFS MUST ngăn truy cập trái phép giữa:

- Projects.
- Tenants.
- Environments.
- Sessions.
- Data classifications.
- Restricted resource scopes.

Mọi operation phải được kiểm tra project context và resource scope.

Không tin project ID do agent tự khai báo nếu không được xác thực bởi execution context.

Một agent được cấp quyền trên project không mặc nhiên có quyền trên PFS global configuration hoặc các project khác.

## 9. Tool Security

Mọi tool có khả năng đọc hoặc thay đổi trạng thái phải được đăng ký và kiểm soát.

Tool registration SHOULD bao gồm:

- Tool ID.
- Tool version.
- Description.
- Input schema.
- Output schema.
- Required permissions.
- Data access scope.
- Side-effect declaration.
- Execution environment.
- Risk classification.
- Timeout.
- Resource limits.
- Provenance.

### 9.1. Tool Invocation

Trước khi gọi tool, PFS MUST kiểm tra:

- Agent có được phép gọi tool không?
- Tool có được phép trong task hiện tại không?
- Input có hợp lệ không?
- Resource có nằm trong scope không?
- Side effect có cần approval không?
- Output có thể chứa untrusted content không?

### 9.2. Arbitrary Execution

Không mặc định cho agent quyền:

- Chạy shell tùy ý.
- Thực thi mã native tùy ý.
- Cài phần mềm tùy ý.
- Truy cập toàn bộ filesystem.
- Đọc toàn bộ environment variables.
- Truy cập network không giới hạn.
- Sử dụng credentials tùy ý.

Các năng lực này phải được cấp riêng, cô lập và kiểm soát.

## 10. Prompt Injection and Instruction Integrity

PFS MUST phân biệt trusted instructions và untrusted content.

Untrusted content có thể chứa câu lệnh giả mạo như:

- Yêu cầu bỏ qua policy.
- Yêu cầu tiết lộ secrets.
- Yêu cầu thay đổi quyền.
- Yêu cầu gửi dữ liệu ra ngoài.
- Yêu cầu chạy lệnh phá hoại.
- Giả danh system hoặc developer instruction.

PFS không được coi nội dung lấy từ tài liệu, website, repository hoặc tool output là policy có thẩm quyền.

### 10.1. Instruction Hierarchy

Thứ tự authority phải được xác định trong governance model và execution context.

Nội dung untrusted không được nâng cấp thành trusted instruction chỉ vì agent trích dẫn hoặc sao chép nó.

### 10.2. Prompt Injection Controls

PFS SHOULD áp dụng:

- Input classification.
- Source labeling.
- Context isolation.
- Tool permission checks.
- Output validation.
- Sensitive action confirmation.
- External content sanitization phù hợp.
- Audit of suspicious instructions.

Không thể đảm bảo phát hiện mọi prompt injection bằng một bộ lọc từ khóa đơn giản.

## 11. Secrets Management

Secrets bao gồm:

- API keys.
- Access tokens.
- Passwords.
- Private keys.
- Signing credentials.
- Database credentials.
- Session tokens.
- Other authentication material.

PFS MUST:

- Không hardcode secrets trong source code hoặc templates.
- Không ghi secrets vào logs.
- Không đưa secrets vào agent prompts nếu không cần thiết.
- Không đưa secrets vào generated documentation.
- Không lưu secrets trong artifact manifests.
- Hạn chế thời gian và phạm vi sử dụng credentials.
- Hỗ trợ revoke và rotate credentials.
- Bảo vệ secret storage theo platform capability.

Agent chỉ nên nhận capability hoặc credential handle cần thiết, không nhận toàn bộ secret store.

## 12. Data Access and Exfiltration Controls

Trước khi gửi dữ liệu cho AI provider, plugin hoặc external service, PFS phải đánh giá:

- Data classification.
- Provider approval.
- Data residency requirements.
- Retention policy.
- Training/data-use policy.
- Contractual restrictions.
- Purpose limitation.
- User authorization.

Không được gửi Confidential hoặc Restricted data tới provider chưa được cho phép.

PFS SHOULD hỗ trợ:

- Data minimization.
- Redaction.
- Field-level filtering.
- Scoped context retrieval.
- Egress policy.
- External destination allowlists khi phù hợp.

## 13. Network and Filesystem Security

### 13.1. Filesystem

Agent SHOULD hoạt động trong workspace được giới hạn.

Filesystem policy phải xác định:

- Allowed roots.
- Read permissions.
- Write permissions.
- Protected files.
- Excluded paths.
- Symlink handling.
- File size limits.
- File type restrictions.
- Overwrite policy.

Không cho phép path traversal vượt workspace.

### 13.2. Network

Network access phải được giới hạn theo task và environment.

PFS SHOULD kiểm soát:

- Destination.
- Protocol.
- Port.
- Authentication.
- Request size.
- Timeout.
- Redirect behavior.
- Data classification.
- Egress policy.

Không cho phép network access vô hạn chỉ vì agent cần tìm thông tin.

## 14. Security Events and Audit

Các sự kiện cần audit gồm:

- Authentication failure.
- Authorization denial.
- Permission grant/revoke.
- Privilege escalation request.
- Tool invocation.
- External data transfer.
- Secret access.
- Protected file modification.
- Destructive operation.
- Policy violation.
- Suspicious prompt injection.
- Security incident.
- Recovery action.

Audit records phải tránh lưu secret hoặc dữ liệu nhạy cảm không cần thiết.

## 15. Revocation and Incident Handling

PFS phải có khả năng:

- Thu hồi agent permission.
- Vô hiệu hóa agent.
- Thu hồi session.
- Thu hồi provider credentials.
- Chặn tool.
- Cô lập project hoặc environment.
- Dừng operation chưa hoàn tất nếu an toàn.
- Ghi incident record.
- Đánh giá ảnh hưởng.
- Khôi phục theo recovery policy.

Khi xảy ra security incident, ưu tiên containment trước khi tiếp tục công việc.

## 16. Security Requirements

| ID | Requirement |
|---|---|
| M0-SEC-AG-001 | PFS MUST enforce least privilege. |
| M0-SEC-AG-002 | PFS MUST use default-deny authorization. |
| M0-SEC-AG-003 | Agent MUST NOT grant or escalate its own permission. |
| M0-SEC-AG-004 | PFS MUST isolate project and tenant scopes. |
| M0-SEC-AG-005 | PFS MUST validate tool permissions before invocation. |
| M0-SEC-AG-006 | PFS MUST distinguish trusted instructions from untrusted content. |
| M0-SEC-AG-007 | PFS MUST protect secrets from unauthorized access and disclosure. |
| M0-SEC-AG-008 | PFS MUST enforce data egress policy. |
| M0-SEC-AG-009 | PFS MUST audit privileged and security-sensitive operations. |
| M0-SEC-AG-010 | PFS MUST support permission revocation. |
| M0-SEC-AG-011 | PFS MUST prevent unauthorized filesystem scope expansion. |
| M0-SEC-AG-012 | PFS MUST define network access boundaries. |
| M0-SEC-AG-013 | PFS MUST support security incident containment. |
| M0-SEC-AG-014 | PFS MUST NOT trust AI output as authorization evidence. |
| M0-SEC-AG-015 | Critical operations MUST have explicit authorization and appropriate separation of duties. |

## 17. M1 and M2 Design Dependencies

M1 phải xác định:

- Security Principal Model.
- Permission Schema.
- Authorization Contract.
- Resource Scope Model.
- Data Classification Contract.
- Audit Event Contract.
- Secret Reference Contract.
- Tool Registration Schema.

M2 phải hiện thực hóa:

- Agent Identity.
- Agent Permission Profiles.
- Tool Access Policies.
- Prompt and Context Security.
- Multi-Agent Isolation.
- Agent Session Lifecycle.
- Revocation Workflow.

M3 phải kiểm chứng các security controls bằng tests và audit scenarios.

M4 chỉ thực thi automation trong phạm vi đã được cấp quyền.

---

**End of Document — PFS-M0-SPEC-009 v1.1.0**
