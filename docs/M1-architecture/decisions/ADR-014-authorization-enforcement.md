# ADR-014 — Authorization Enforcement: Deterministic L0–L5 Deny-by-Default Engine

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-014 |
| Title | Authorization Enforcement: Deterministic L0–L5 Deny-by-Default Engine with Classification Integration |
| Status | Proposed — Ready for Owner Review |
| Decision Authority | Principal Systems Architect & Security Reviewer |
| Date | 2026-11-17 |
| Target Milestone | M1 — Documentation & Architecture Foundation |
| Related Modules | `MOD-11-POL`, `MOD-10-GOV`, `pfs-governance` |
| Related Requirements | M1-SEC-001, M1-DOM-001, M0-GOV-001, M0-AUT-001 |
| Related Diagrams | DIA-010-governance-approval-sequence.mmd |
| Parent Baseline | [PFS-M0-SPEC-006](file:///C:/Users/OK259/rust/docs/M0-foundation/06-AUTHORITY-AND-DECISION-MODEL.md) |
| Invariant Reference | INV-06, INV-11 |
| Audit Remediation | Resolved finding FND-M1-01 (Classification-Aware Authorization Matrix) and FND-M1-08 (Concrete Revisit Conditions) |

---

## 1. Context & Problem Statement

Trong các hệ sinh thái AI kết hợp phần mềm, rủi ro lớn nhất là việc cấp quyền mập mờ hoặc dựa trên sự tự kiểm soát của AI (Prompt-based access control). Nếu để AI tự xác định "tôi có quyền sửa file này hay không", một prompt độc hại hoặc ảo giác có thể dễ dàng vượt qua cơ chế bảo vệ.

Hệ thống đòi hỏi một động cơ phân quyền xác định (Deterministic Authorization Engine) hoạt động độc lập ở tầng lõi Rust, bảo đảm quyền hạn tối thiểu (Least Privilege), từ chối mặc định (Deny-by-Default), kết hợp chặt chẽ với phân loại bảo mật dữ liệu và kiểm tra chữ ký số cho các quyết định của Project Owner.

---

## 2. Decision Drivers

- **Bảo toàn bất biến M0:** Hiện thực hóa chính xác mô hình phân cấp thẩm quyền 6 mức L0–L5 đã được phê duyệt tại M0.
- **Thực thi xác định (Deterministic Enforcement):** Kiểm tra phân quyền bằng mã nguồn tĩnh trong Rust trước khi bất kỳ Command nào được chuyển đến Domain Aggregates.
- **Cách ly tuyệt đối AI Agents:** AI Agents mặc định không bao giờ sở hữu quyền hạn từ L3 trở lên; không bao giờ tự phê duyệt quyết định của con người hoặc tự vượt qua Quality Gates.
- **Tích hợp Phân loại Dữ liệu (Classification Integration):** Đánh giá quyền hạn kết hợp mức độ bảo mật dữ liệu: `(Actor, Action, Resource, AuthorityLevel, ClassificationTier)`.

---

## 3. Options Considered

- **Option A: Traditional Role-Based Access Control (RBAC) Only:**
  - Gán quyền đơn giản theo tên Role (Admin, Editor, Viewer).
  - *Nhược điểm:* Quá thô sơ; không kiểm soát được theo ngữ cảnh (Context), ranh giới dự án (Scope) hay mức độ can thiệp (L0–L5).
- **Option B: Prompt-Guided Agent Authorization:**
  - Nhắc nhở Agent trong system prompt: "Bạn chỉ được phép đọc, không được phép sửa".
  - *Nhược điểm:* Hoàn toàn không có giá trị bảo mật; bị vô hiệu hóa 100% khi gặp Prompt Injection.
- **Option C (Được chọn): Policy Enforcement Point (PEP) & Policy Decision Point (PDP) với Mô hình L0–L5 Deny-by-Default:**
  - Áp dụng chuẩn kiến trúc an ninh XACML/Zero Trust: Mọi Command đều phải đi qua `PolicyEnforcementPoint` (PEP).
  - PEP chuyển yêu cầu tới `PolicyDecisionPoint` (PDP) trong Crate `pfs-governance` để đánh giá theo bộ luật L0–L5 kết hợp ngữ cảnh (Subject, Role, AuthorityLevel, ResourceScope, Action, DataTier).

---

## 4. Decision & Rationale

**QUYẾT ĐỊNH:** Áp dụng **Option C: Policy Enforcement Point với Mô hình L0–L5 Deny-by-Default**.
- Các cấp độ thẩm quyền được định nghĩa bằng Rust Enum có kiểu dữ liệu mạnh:
  - `L0`: Chỉ đọc (Read-only).
  - `L1`: Phân tích và đề xuất (Analyze / Propose).
  - `L2`: Tạo bản nháp trong thư mục tạm Staging (Draft Artifacts).
  - `L3`: Sửa đổi tệp tin được ủy quyền (Modify Authorized Files - Bắt buộc con người).
  - `L4`: Thực thi các tác vụ được phê duyệt (Execute Approved Operations - Bắt buộc con người).
  - `L5`: Thao tác đặc quyền hoặc phá hủy / Nghiệm thu Baseline (Chỉ Project Owner, bắt buộc chữ ký số Ed25519).

### 4.1. Ma trận Thẩm quyền Đa chiều (Actor × Action × Resource × Level × Data Tier)

| Actor Type | Resource Scope | Action Permitted | Max Level | Data Tier Allowed | Cơ chế kiểm tra |
|---|---|---|---|---|---|
| **Anonymous / External** | None | Read Public Docs | L0 | Public | Mặc định chặn mọi thao tác ghi |
| **AI Agent (Worker)** | Assigned Task Context | Analyze, Propose, Draft to Stage | L1–L2 | Public, Internal | Chặn lệnh ghi đè trực tiếp; cấm dữ liệu Restricted |
| **Software Engineer** | Workspace Directory | Modify files, run build, test | L3 | Public, Internal, Confidential | Xác thực Token phiên làm việc |
| **Lead Architect** | Project Baseline, ADRs | Approve designs, sign-off gates | L4 | Public, Internal, Confidential | Xác thực phiên và vai trò Lead |
| **Project Owner** | Entire System, Organization | Accept Milestone, Grant Waivers | L5 | All Tiers (including Restricted) | Bắt buộc chữ ký số Ed25519 |

- Nguyên tắc **Deny-by-Default**: Nếu không tìm thấy một `AuthorityGrant` hợp lệ khớp chính xác với `(Subject, Resource, Action, Scope, Tier)`, hành động lập tức bị từ chối với lỗi `PermissionDenied`.
- Nguyên tắc **Maker-Checker & Separation of Duties (SoD)**: Người tạo đề xuất (Maker) tuyệt đối không được phép tự phê duyệt (Checker) đề xuất của chính mình.

---

## 5. Consequences & Trade-offs

### 5.1. Tích cực (Positive Consequences)
- An toàn an ninh tuyệt đối; AI Agent không thể tự nâng quyền; kiểm toán phân quyền minh bạch 100%.
- Ngăn ngừa tình trạng rò rỉ dữ liệu Restricted nhờ tích hợp kiểm tra classification tier ngay tại PDP.

### 5.2. Thách thức (Negative Consequences)
- Đòi hỏi thiết kế chi tiết các grant rules và chính sách kiểm soát trong Crate `pfs-governance`.

---

## 6. Security & Operational Implications

- **Chữ ký số Ed25519 cho quyền L5:** Không có thao tác L5 nào (như nghiệm thu M0/M1, cấp exception waiver) được coi là hợp lệ nếu thiếu chữ ký số xác thực với Public Key của Project Owner.
- **Ghi nhật ký kiểm toán bất biến:** Mọi quyết định cấp quyền (`Allow`) hoặc từ chối (`Deny`) đều được ghi nhận vào Sổ cái Kiểm toán với đầy đủ thông tin định danh và mốc thời gian.

---

## 7. Dependencies & Compatibility

- **Phụ thuộc:** `MOD-01-IAM` (Identity and Access), `MOD-10-GOV` (Governance), `pfs-governance` crate.

---

## 8. Status & Owner Governance

- **Trạng thái:** `Proposed — Ready for Owner Review`.
- **Thẩm quyền phê duyệt:** Project Owner (Nguyễn Thế Thuận) — Bảo lưu cho quyết định OD-M1-01.
- **Bằng chứng kiến trúc:** `E2 — Specified` (Đặc tả chi tiết tại `docs/M1-architecture/05-trust-and-quality/19-GOVERNANCE-AND-AUTHORIZATION-ARCHITECTURE.md` và `DIA-010-governance-approval-sequence.mmd`).

---

## 9. Revisit Conditions

Mô hình phân quyền L0–L5 và Policy Engine sẽ được xem xét điều chỉnh khi và chỉ khi xuất hiện một trong các điều kiện đo lường được sau:
1. **Mở rộng sang liên minh đa tổ chức (Cross-Organizational Federation):** Khi hệ thống mở rộng hỗ trợ chia sẻ tài nguyên giữa nhiều tập đoàn độc lập đòi hỏi các chính sách kiểm soát truy cập dựa trên thuộc tính nâng cao (Full Attribute-Based Access Control - ABAC) với hàng trăm thuộc tính động của môi trường mà bộ 6 cấp thẩm quyền L0–L5 tĩnh không thể phân giải trực tiếp mà không cần luật phụ trợ.
2. **Tiêu chuẩn an ninh công nghiệp mới:** Khi xuất hiện chuẩn an ninh công nghiệp bắt buộc về phân quyền đại lý AI (AI Agent Delegation Standard) được IETF hoặc NIST phê chuẩn chính thức, làm thay đổi mô hình Maker-Checker hiện tại giữa con người và agent.
3. **Độ trễ đánh giá chính sách:** Khi thời gian đánh giá PDP vượt quá 10ms cho một command đơn lẻ do quy mô ma trận phân quyền vượt quá 10.000 rules, đòi hỏi phải biên dịch ma trận thành cây quyết định nhị phân (Binary Decision Diagram / eBPF rules).
