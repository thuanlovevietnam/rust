# PFS-M1-DOC-022 — Data Privacy, Classification & Supply Chain Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-022 |
| Document Title | Data Privacy, Classification, AI Boundary Protection and Supply Chain Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.1.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect & Security Reviewer |
| Classification | Internal |
| Reference Framework | NIST SP 800-218 (SSDF), ISO/IEC 27001, OpenSSF Scorecard, STRIDE-AI |
| Related Decisions | ADR-012, ADR-013, ADR-014, ADR-019 |
| Parent Baseline | [PFS-M0-SPEC-012](file:///C:/Users/OK259/rust/docs/M0-foundation/12-SECURITY-AND-SUPPLY-CHAIN.md) |
| Invariant Reference | INV-06, INV-11, INV-12 |
| Audit Remediation | Resolved finding FND-M1-01 (Restricted Data Protection & Boundary Enforcement) |

---

## 1. Data Governance & Privacy Principles

Trong hệ sinh thái kỹ thuật số hiện đại, việc sử dụng các dịch vụ trí tuệ nhân tạo (AI/LLMs) đặt ra thách thức nghiêm trọng về an toàn quyền riêng tư, rò rỉ dữ liệu doanh nghiệp và nguy cơ vi phạm an ninh chuỗi cung ứng phần mềm.

Theo bất biến kiến trúc **INV-11**, **Project Foundation System (PFS)** thiết lập một khung quản trị dữ liệu chặt chẽ dựa trên 4 nguyên tắc cốt lõi:
1. **Data Minimization (Tối thiểu hóa dữ liệu):** Chỉ gửi những phần thông tin thực sự cần thiết để hoàn thành nhiệm vụ sang AI Provider; tuyệt đối không gửi toàn bộ mã nguồn hoặc tài liệu thô nếu không có yêu cầu.
2. **Metadata-Based Boundary Enforcement:** Phân loại bảo mật dựa trên metadata thực thể là chốt chặn bắt buộc; không bao giờ coi lọc Regex/Entropy là cơ chế duy nhất bảo vệ dữ liệu nhạy cảm.
3. **Zero Secret in Prompts / Logs / Manifests:** Mọi thông tin định danh bí mật (API keys, tokens, mật khẩu, private keys) tuyệt đối không bao giờ được xuất hiện trong prompt gửi sang LLM, nhật ký hệ thống (logs) hay manifest tệp tin.
4. **End-to-End Cryptographic Provenance:** Mọi thành phần mã nguồn, mẫu template và gói phân phối đều phải có nguồn gốc rõ ràng, được ký số và kiểm tra tính toàn vẹn độc lập.

---

## 2. Formal 4-Tier Data Classification Model (Preserved from M0)

PFS bảo toàn chính xác mô hình phân loại dữ liệu 4 cấp độ kế thừa từ M0:

| Cấp phân loại | Tên phân loại | Định nghĩa dữ liệu chuẩn M0 | Ví dụ thực tế | Chính sách chia sẻ với AI Provider | Quy tắc mặc định tại Gateway |
|---|---|---|---|---|---|
| **Tier 1** | **Public** | Dữ liệu công khai, không gây rủi ro nếu bị tiết lộ ra ngoài | Tài liệu mã nguồn mở, đặc tả tiêu chuẩn công cộng (RFCs), tài liệu hướng dẫn người dùng cuối. | Cho phép gửi sang bất kỳ AI Provider nào (bao gồm cả các mô hình công cộng). | **ALLOW** |
| **Tier 2** | **Internal** | Dữ liệu nội bộ dự án, không có giá trị bảo mật cao nhưng không công bố rộng rãi | Sơ đồ kiến trúc nội bộ, ghi chú cuộc họp nhóm, tài liệu phân tích kỹ thuật của dự án. | Cho phép gửi sang AI Provider đã ký thỏa thuận Enterprise Do-Not-Train Agreement. | **ALLOW with Enterprise Headers** |
| **Tier 3** | **Confidential** | Dữ liệu nhạy cảm của tổ chức, tiết lộ sẽ gây tổn hại tài chính hoặc pháp lý | Kế hoạch kinh doanh chiến lược, ước tính ngân sách chi tiết, thông tin đối tác thương mại. | Chỉ cho phép gửi sang AI Provider có chứng chỉ SOC 2 Type II và cấu hình Zero Data Retention. | **ALLOW with ZDR & Audit Log** |
| **Tier 4** | **Restricted** | Dữ liệu tối mật, vi phạm sẽ dẫn đến trách nhiệm hình sự hoặc thảm họa an ninh | Khóa bí mật (Private Keys), API Secrets, dữ liệu định danh cá nhân (PII), mã nguồn lõi độc quyền, hợp đồng mật. | **TUYỆT ĐỐI NGHIÊM CẤM GỬI RA BẤT KỲ AI PROVIDER BÊN NGOÀI NÀO!** Chỉ xử lý trên local air-gapped model khi có ngoại lệ được duyệt. | **STRICT DENY (Chặn đứng tại Context Builder & Gateway)** |

---

## 3. Data Protection Architecture across 10 Boundaries (Remediation FND-M1-01)

Để khắc phục triệt để lỗ hổng kiểm toán FND-M1-01, kiến trúc bảo vệ dữ liệu được tái cấu trúc thành một hệ thống chốt chặn xác định trên toàn bộ 10 ranh giới xử lý:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                 PFS 10-Boundary Data Protection Architecture & Enforcement Flow                 │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Data Entity Ingestion: Mandatory Metadata Classification (Tier 1..4, Provenance, Scope)     │
│                                │                                                                │
│  2. Classification Propagation: Downstream entities inherit max(input_tiers); Tool outputs tag  │
│                                │                                                                │
│  3. Context Builder Boundary: PEP queries PDP -> If Tier == Restricted -> REJECT Payload       │
│                                │                                                                │
│  4. AI Provider Gateway Boundary: Gatekeeper verifies Destination Type (External vs Local)      │
│     ├── External Cloud Provider (OpenAI/Anthropic) -> STRICT DENY if Restricted / Unclassified  │
│     └── Air-Gapped Local Model (vLLM/Ollama)       -> Allowed ONLY with L5 Owner Exception Waiver│
│                                │                                                                │
│  5. Tool Input/Output Boundary: Ephemeral Sandbox enforces egress block; Output inherits input  │
│                                │                                                                │
│  6. Embedding Ingestion Boundary: Vector DB stores vectors with classification & scope metadata  │
│                                │                                                                │
│  7. Logging & Telemetry Boundary: Masking filter strips payloads; Restricted NEVER logged       │
│                                │                                                                │
│  8. Cache & Storage Boundary: Scoped by Tenant/Project; Wiped on session termination            │
│                                │                                                                │
│  9. Artifact Export Boundary: CAS export bundle validates compliance before archive generation  │
│                                │                                                                │
│ 10. Audit Evidence Trail: Cryptographic audit ledger records every evaluation, deny & exception│
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Quy tắc Bất biến tại AI Context Boundary

> [!CRITICAL]
> **QUY TẮC BẤT BIẾN SỐ 1 (RESTRICTED DATA EXTERNAL DISPATCH FORBIDDEN):**  
> Dữ liệu được phân loại là **Restricted** tuyệt đối không bao giờ được gửi tới bất kỳ External AI Provider nào nếu không có một cơ chế cấp quyền ngoại lệ rõ ràng (Exception Waiver Record), được ký số mã hóa Ed25519 bởi **Project Owner (L5 Authority)** và chỉ gửi tới máy chủ xử lý cục bộ cô lập hoàn toàn (Air-gapped Local Model). Mọi vi phạm đều kích hoạt trạng thái dừng khẩn cấp (Emergency Halt).

**Chính sách mặc định (Fail-Secure Defaults):**
- **Restricted Data:** Mặc định từ chối gửi ngoại vi (`Deny External Dispatch`).
- **Không có metadata phân loại (Unclassified):** Xử lý theo chính sách an toàn nhất — coi như `Restricted`, tuyệt đối không mặc định là `Public`.
- **Không xác định được nguồn gốc (Provenance) hoặc quyền truy cập:** Mặc định `Deny`.
- **Tool Output Inheritance:** Đầu ra của công cụ tự động kế thừa mức phân loại cao nhất từ các tham số đầu vào và các nguồn dữ liệu được đọc.
- **Embedding Metadata Preservation:** Vector embeddings khi nạp vào Vector Database bắt buộc phải lưu kèm metadata về `scope_id`, `project_id`, `classification_tier`, `source_hash` và danh sách quyền truy cập (ACL). Khi truy vấn ngữ nghĩa, bộ lọc tiền xử lý (pre-filter) bắt buộc phải loại bỏ các vector vượt quá thẩm quyền của tác vụ trước khi tính khoảng cách cosine.
- **Logging Sanitization:** Logs và viễn trắc (telemetry) tuyệt đối không được trở thành kênh rò rỉ dữ liệu bị cấm. Payloads chứa dữ liệu `Confidential` hoặc `Restricted` bị cấm ghi vào log; chỉ ghi nhận metadata (mã băm, kích thước, mã kết quả).

---

## 4. Context Builder PEP/PDP Enforcement Engine

Trước khi bất kỳ một context snippet nào được tổng hợp vào prompt payload gửi đi, hệ thống thực thi quy trình kiểm soát truy cập thông qua mô hình **Policy Enforcement Point (PEP)** và **Policy Decision Point (PDP)**:

```rust
// Contract: Context Policy Enforcement
pub enum ClassificationTier {
    Public,
    Internal,
    Confidential,
    Restricted,
}

pub enum ProviderDestination {
    ExternalCloud { provider_name: String, zero_retention: bool },
    AirGappedLocal { host_ip: String, enclave_verified: bool },
}

pub struct ContextEnforcementRequest<'a> {
    pub project_id: &'a str,
    pub task_id: &'a str,
    pub entity_classification: ClassificationTier,
    pub destination: ProviderDestination,
    pub actor_authority: String,
    pub owner_waiver_signature: Option<&'a str>,
}

pub enum ContextDecision {
    Allow,
    Deny { reason_code: DenialReasonCode, detail: String },
}

pub enum DenialReasonCode {
    DenyRestrictedExternalDispatch,
    DenyUnclassifiedData,
    DenyInsufficientAuthority,
    DenyUnresolvedProvenance,
    DenyPolicyViolation,
    DenyZeroRetentionMissing,
}
```

### 4.1. Bảng Mã Lý Do Từ Chối (Denial Reason Codes)

Khi Context Builder hoặc Provider Gateway từ chối một yêu cầu gửi dữ liệu, mã lỗi xác định bắt buộc phải được trả về và ghi nhận vào Sổ cái Kiểm toán:

| Mã lý do (Reason Code) | Ý nghĩa nghiệp vụ | Hành động hệ thống |
|---|---|---|
| `DENY_RESTRICTED_EXTERNAL_DISPATCH` | Thực thể chứa dữ liệu Restricted cố gắng gửi tới External AI Provider. | Chặn đứng yêu cầu; emit cảnh báo an ninh; ghi log kiểm toán; dừng task. |
| `DENY_UNCLASSIFIED_DATA` | Dữ liệu đầu vào thiếu trường metadata `classification`. | Chặn đứng theo chính sách Fail-Secure; yêu cầu phân loại trước khi tiếp tục. |
| `DENY_INSUFFICIENT_AUTHORITY` | Actor không sở hữu cấp thẩm quyền tối thiểu để giải mã hoặc xử lý dữ liệu. | Trả mã lỗi 403 / Forbidden; yêu cầu nâng quyền hoặc người giám sát phê duyệt. |
| `DENY_UNRESOLVED_PROVENANCE` | Dữ liệu không có mã băm toàn vẹn SHA-256 hoặc nguồn gốc không rõ ràng. | Từ chối nạp vào context; yêu cầu xác thực tính toàn vẹn. |
| `DENY_ZERO_RETENTION_MISSING` | Dữ liệu Confidential yêu cầu Zero Data Retention nhưng provider không hỗ trợ. | Chặn dispatch; chuyển hướng sang fallback provider hỗ trợ ZDR. |
| `DENY_POLICY_VIOLATION` | Vi phạm các quy tắc nghiệp vụ khác của Organization hoặc Workspace. | Hủy bỏ tác vụ; thông báo lý do chi tiết cho người vận hành. |

---

## 5. Phân Định Rõ Ràng 4 Khái Niệm An Ninh

Hệ thống phân định rạch ròi 4 khái niệm an ninh để tránh nhầm lẫn trong thiết kế và thi công:

1. **Secret Redaction (Khử bí mật tự động):**
   - *Bản chất:* Cơ chế làm sạch bề mặt chuỗi văn bản (String sanitization) bằng biểu thức chính quy (Regex) và phân tích độ hỗn loạn thông tin (Shannon Entropy).
   - *Vai trò:* Lưới lọc phòng thủ theo chiều sâu (Defense-in-depth) để ngăn ngừa các API keys, SSH keys, passwords vô tình lọt vào văn bản.
   - *Giới hạn:* KHÔNG PHẢI là cơ chế kiểm soát truy cập và KHÔNG THỂ thay thế việc bảo vệ dữ liệu phân loại.
2. **Classification Enforcement (Thực thi phân loại dữ liệu):**
   - *Bản chất:* Chính sách điều khiển luồng dữ liệu dựa trên metadata được gán cho từng thực thể (Entity Attribute-Based Policy).
   - *Vai trò:* Ngăn chặn dữ liệu Restricted/Confidential rời khỏi ranh giới an toàn, kiểm soát điểm đến của dữ liệu.
3. **Authorization Engine (Mô hình phân quyền L0–L5):**
   - *Bản chất:* Xác thực quyền hạn của chủ thể (Principal: Human / Agent / Service) đối với hành động (Action) trên tài nguyên (Resource).
   - *Vai trò:* Bảo đảm nguyên tắc Least Privilege, Separation of Duties và kiểm tra chữ ký số Ed25519 cho các quyết định của Owner.
4. **Data Minimization (Tối thiểu hóa dữ liệu):**
   - *Bản chất:* Quy trình nghiệp vụ lược bỏ các trường thông tin không cần thiết trước khi tạo prompt context.
   - *Vai trò:* Giảm thiểu diện tích bề mặt rủi ro và tiết kiệm chi phí token.

---

## 6. Software Supply Chain Security Architecture

Để đáp ứng các tiêu chuẩn khắt khe của **NIST SP 800-218 (SSDF)** và bảo vệ PFS Core trước các cuộc tấn công chuỗi cung ứng:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Software Supply Chain Security Pipeline                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Third-Party Rust Crates Governance:                                     │
│     ├── Pinned Lockfile (Cargo.lock checked into Git)                       │
│     ├── Automated Vulnerability Scanning: cargo-audit (RustSec Advisory DB)│
│     └── License & Dependency Policy Enforcement: cargo-deny (MIT/Apache)   │
│                                                                             │
│  2. Template Provenance & Verification:                                     │
│     ├── Templates signed by Lead Architect (Ed25519 Signature)              │
│     └── Tampering detection: Verify SHA-256 against Template Ledger         │
│                                                                             │
│  3. Extension & Plugin Verification:                                        │
│     ├── Mandatory Code Signing Certificate for Third-Party Plugins          │
│     └── Isolation execution in WebAssembly (WASM) Sandbox                   │
│                                                                             │
│  4. Reproducible Builds & SBOM Emission:                                    │
│     ├── Deterministic Compilation (Fixed Rust toolchain via rust-toolchain) │
│     └── Software Bill of Materials (SBOM) generated in CycloneDX JSON format│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.1. Chính sách Quản lý Phụ thuộc Ngoại vi (Dependency Policy)
- **Cấm Crate Không Rõ Nguồn Gốc:** Mọi thư viện phụ thuộc trong Cargo.toml phải có mức độ tin cậy cao, có nhiều lượt tải về trên crates.io hoặc được kiểm toán bởi cộng đồng Rust uy tín (Tokyo, Serde, SQLx, Ring).
- **Giấy phép Bản quyền (License Compliance):** Chỉ cho phép các thư viện có giấy phép tương thích: `MIT`, `Apache-2.0`, `BSD-3-Clause`. Nghiêm cấm sử dụng các thư viện `GPL-3.0` hoặc `AGPL` có thể làm ảnh hưởng đến tính thương mại của PFS Core.
- **Tạo SBOM Tự động:** Mỗi bản phát hành nhị phân của PFS Core đều đi kèm một tệp **Software Bill of Materials (SBOM)** chuẩn định dạng CycloneDX JSON để phục vụ việc kiểm toán an ninh chuỗi cung ứng của khách hàng doanh nghiệp.

---

## 7. Security Test Cases & Implementation Evidence Plan

Toàn bộ các yêu cầu an ninh dữ liệu trên được lập thành kế hoạch kiểm thử xác thực:

| Test Case ID | Mục tiêu kiểm thử | Đầu vào thử nghiệm | Kết quả mong đợi | Cấp độ bằng chứng M1 | Milestone triển khai runtime |
|---|---|---|---|---|---|
| `SEC-TEST-01` | Chặn dữ liệu Restricted gửi sang External Provider | Entity có `classification: Restricted`, Provider: OpenAI | Context Builder trả về `DENY_RESTRICTED_EXTERNAL_DISPATCH`, không có HTTP request nào được gửi | `E2 — Specified` | M2 (`WP-M2-02`, `WP-M2-03`) |
| `SEC-TEST-02` | Chặn dữ liệu thiếu metadata phân loại | Entity thiếu field `classification`, Provider: Anthropic | Context Builder trả về `DENY_UNCLASSIFIED_DATA` | `E2 — Specified` | M2 (`WP-M2-02`) |
| `SEC-TEST-03` | Cho phép dữ liệu Restricted gửi sang Local Enclave khi có Owner Waiver | Entity `Restricted`, Provider: Local vLLM, kèm Ed25519 Owner Waiver | Context Builder xác thực chữ ký số hợp lệ và trả về `Allow` | `E2 — Specified` | M2 (`WP-M2-02`, `WP-M2-03`) |
| `SEC-TEST-04` | Kế thừa phân loại dữ liệu qua Tool Output | Tool đọc file `Confidential` -> sinh output | Tool output tự động được gán nhãn `Confidential` | `E2 — Specified` | M2 (`WP-M2-04`) |
| `SEC-TEST-05` | Ngăn chặn rò rỉ dữ liệu qua Logging | Context chứa chuỗi nhạy cảm đi qua Logger | Log record chỉ chứa sha256 digest, không chứa nội dung thô | `E2 — Specified` | M2 (`WP-M2-01`) |
| `SEC-TEST-06` | Bộ lọc Secret Redaction đa mẫu | Chuỗi chứa AWS Secret Key và Shannon entropy cao | Chuỗi đầu ra được thay thế bằng `[REDACTED_SECRET]` | `E2 — Specified` | M2 (`WP-M2-03`) |

> [!NOTE]
> **Ranh giới Bằng chứng M1:** Trong phạm vi Milestone M1, tài liệu này hoàn tất trọn vẹn đặc tả kiến trúc, ranh giới an ninh, contracts và test plan ở mức độ **E2 — Specified** và **E3 — Statically Validated**. Mã nguồn runtime enforcement và test suite thực thi sẽ được triển khai và nghiệm thu ở cấp độ **E4 — Executably Verified** trong Milestone M2.
