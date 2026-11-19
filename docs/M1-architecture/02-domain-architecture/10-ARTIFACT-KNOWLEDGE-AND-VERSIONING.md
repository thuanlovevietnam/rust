# PFS-M1-DOC-010 — Artifact, Knowledge and Versioning Architecture

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-010 |
| Document Title | Artifact, Knowledge and Versioning Architecture Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Content-Addressed Storage (CAS), Merkle Directed Acyclic Graph (Merkle DAG) |
| Related Diagrams | DIA-011-artifact-provenance-graph.mmd |
| Related Decisions | ADR-008, ADR-010 |
| Parent Baseline | [PFS-M0-SPEC-007](file:///C:/Users/OK259/rust/docs/M0-foundation/07-ARTIFACT-AND-TRACEABILITY-MODEL.md), [PFS-M0-SPEC-011](file:///C:/Users/OK259/rust/docs/M0-foundation/11-VERSION-AND-CHANGE-MANAGEMENT.md) |

---

## 1. Artifact Architectural Paradigm

Trong **Project Foundation System (PFS)**, **Artifact** không đơn giản chỉ là một tệp tin tĩnh (file) nằm trên đĩa cứng. Artifact là một **Thực thể Tạo tác có Cấu trúc (Structured Entity)** mang đầy đủ ngữ cảnh nghiệp vụ, định danh toàn cầu bất biến, lược đồ xác thực, phân loại an ninh và lịch sử nguồn gốc (Provenance) có thể kiểm chứng toán học.

PFS áp dụng nguyên lý **Content-Addressed Storage (CAS)** kết hợp với cấu trúc dữ liệu **Merkle Directed Acyclic Graph (Merkle DAG)** (tương tự như mô hình quản lý của Git và IPFS). Mã băm SHA-256 của nội dung tệp tin đóng vai trò là khóa xác thực tính toàn vẹn (Integrity Checksum):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Artifact Entity Metamodel                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Identity: Global ULID, Project Scope, Artifact Type, Path URI, Display Name│
│  Version & State: Semantic Version, Lifecycle State, Content Hash (SHA-256) │
│  Classification: Public | Internal | Confidential | Restricted              │
│  Provenance Manifest: Creator (Human/Agent), Provider/Model, Tool, Template │
│  Relations: DerivedFrom [Parents], Implements [Reqs], GovernedBy [Decisions]│
│  Storage: Structured Metadata (DB) + Raw Content (CAS Blob Store)           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Complete Artifact Metadata Specification

Mỗi Artifact được PFS quản lý bắt buộc phải có bản ghi siêu dữ liệu (Metadata) đầy đủ tuân thủ lược đồ JSON Schema tại `docs/M1-architecture/schemas/artifact-schema.json`:

| Trường siêu dữ liệu | Kiểu dữ liệu | Ý nghĩa và Ràng buộc kiến trúc |
|---|---|---|
| `artifact_id` | ULID / String | Định danh bất biến toàn cầu duy nhất của Artifact. |
| `project_id` | ULID / String | Định danh dự án sở hữu (Project Scope Isolation). |
| `name` | String | Tên hiển thị người dùng đọc được. |
| `path_uri` | String | Đường dẫn tương đối chuẩn hóa trong Foundation Package (vd: `docs/arch/c4.md`). |
| `artifact_type` | Enum | `Specification`, `ArchitectureDesign`, `SourceCode`, `Configuration`, `Schema`, `DecisionRecord`, `EvidenceReport`, `BinaryBlob`. |
| `format` | Enum | `Markdown`, `JSON`, `YAML`, `Mermaid`, `RustSource`, `Binary`. |
| `content_hash` | String (Hex) | Mã băm SHA-256 của nội dung tệp tin để kiểm tra tính toàn vẹn. |
| `size_bytes` | Integer | Dung lượng tệp tính bằng bytes. |
| `version` | SemVer String | Phiên bản logic của artifact (vd: `1.2.0`). |
| `lifecycle_state` | Enum | `Draft`, `InReview`, `Approved`, `Active`, `Superseded`, `Archived`. |
| `classification` | Enum | `Public`, `Internal`, `Confidential`, `Restricted`. |
| `created_by` | Principal ID | Danh tính chủ thể tạo (User ID hoặc Agent Profile ID). |
| `created_at` | RFC 3339 Time | Dấu thời gian tạo lập chính xác (UTC). |
| `provenance` | Object | Thông tin chi tiết về công cụ, template, model LLM và prompt hash. |
| `derived_from` | Array<ULID> | Danh sách các Artifact IDs tiền nhiệm (Merkle DAG parents). |
| `implements_reqs`| Array<String> | Danh sách các Requirement IDs mà artifact này hiện thực hóa. |
| `governed_by` | Array<String> | Danh sách các Decision IDs (ADRs) bảo trợ cho artifact này. |
| `retention_policy`| Object | Quy định thời gian lưu trữ và điều kiện hủy bỏ dữ liệu. |

---

## 3. Provenance Architecture (Nguồn gốc Tạo tác)

Khả năng kiểm chứng nguồn gốc (Provenance) là điều kiện bắt buộc để bảo đảm an toàn chuỗi cung ứng phần mềm và ngăn chặn rủi ro dữ liệu AI bị ô nhiễm (Poisoning). Mỗi khi một Artifact được tạo mới hoặc cập nhật, hệ thống ghi nhận một **Provenance Record**:

```json
{
  "provenance_type": "AIGeneratedWithDeterministicValidation",
  "agent_profile_id": "agent.arch.c4_designer",
  "llm_provider": "Anthropic",
  "llm_model": "claude-3-7-sonnet-20250219",
  "prompt_template_id": "tpl.arch.component.v2",
  "prompt_hash": "a8f3b9c1d2e4...sha256",
  "policy_version_in_effect": "pol.gov.l0_l5.v1.1",
  "execution_saga_id": "saga_01HQZ892K1...",
  "deterministic_validator": "tools/validation/validate_mermaid.py",
  "validation_result": "PASS",
  "human_reviewer": "user_principal_lead_architect",
  "approval_signature": "ed25519_sig_..."
}
```

### 3.1. Phân loại hình thức sinh tạo (Provenance Types)
1. **User Supplied:** Dữ liệu do người dùng đưa trực tiếp vào (tài liệu brief, file thiết kế gốc).
2. **Deterministic Generated:** Sinh ra hoàn toàn bằng thuật toán xác định trong Rust Core từ template và metadata (không dùng LLM).
3. **AI Generated:** Nội dung do mô hình AI đề xuất dựa trên prompt và context injection.
4. **Imported:** Dữ liệu nạp từ hệ sinh thái bên ngoài (Git repo, OpenAPI spec).
5. **Derived:** Tạo tác phái sinh được biên dịch hoặc chuyển đổi từ các artifacts khác.

---

## 4. Content Storage Architecture

Hệ thống lưu trữ nội dung Artifacts được thiết kế theo mô hình lai (Hybrid Storage Model):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Hybrid Storage Architecture                          │
├────────────────────────────────────────┬────────────────────────────────────┤
│ Metadata Store (Structured RDBMS)      │ Content-Addressed Blob Store (CAS) │
│ - SQLite (Local / Embedded mode)       │ - Local Directory: .pfs/cas/objects│
│ - PostgreSQL (Server / Cluster mode)   │ - S3-compatible Object Storage     │
│ - Lưu: Index, Relations, DAG, ACL      │ - Lưu: Tệp tin nén (Zstandard)     │
│ - Tra cứu: < 5ms                       │ - Đặt tên: .pfs/cas/ab/cd/abcdef...│
└────────────────────────────────────────┴────────────────────────────────────┘
```

- **Tính nguyên tử khi ghi (Atomic Write):** Tệp tin được ghi trước vào vùng tạm (Staging Directory) với tên tạm thời `.tmp.<ulid>`. Sau khi kiểm tra mã băm SHA-256 khớp với metadata, hệ thống thực hiện phép đổi tên nguyên tử (Atomic Rename / `renameat2`) vào vùng lưu trữ chính thức.
- **Deduplication (Chống trùng lặp dữ liệu):** Nhờ cơ chế CAS, các tệp tin có cùng nội dung ở các phiên bản hoặc các dự án khác nhau chỉ lưu trữ vật lý duy nhất một bản sao.

---

## 5. Knowledge Management Architecture

PFS phân định rõ ràng 6 phân vùng tri thức để bảo đảm an toàn dữ liệu và tối ưu hóa khả năng tái sử dụng:

| Phân vùng Tri thức | Phạm vi sở hữu (Scope) | Cơ chế chia sẻ & Ranh giới cách ly |
|---|---|---|
| **Project Knowledge** | Duy nhất trong một Project | Cách ly tuyệt đối; các dự án khác không thể truy cập trừ khi được xuất khẩu. |
| **Organization Knowledge** | Chia sẻ trong một Organization | Áp dụng cho các tiêu chuẩn doanh nghiệp, quy định pháp lý nội bộ, style guides. |
| **Global Reusable Knowledge** | Toàn bộ hệ sinh thái PFS | Thư viện mẫu chuẩn hóa (Templates, C4 profiles, Best practices) không chứa dữ liệu mật. |
| **Template Knowledge** | Thuộc về Generator Engine | Các bộ khung tạo tài liệu/mã nguồn đã qua kiểm định chất lượng nghiêm ngặt. |
| **Agent Knowledge** | Gắn liền với Agent Profile | System prompts, bộ nhớ ngữ cảnh ngắn hạn (Context Memory), lịch sử gọi công cụ. |
| **External Knowledge** | Tích hợp từ bên ngoài | Dữ liệu tra cứu tài liệu tiêu chuẩn kỹ thuật (RFCs, ISO standards) qua Tool Gateway. |

---

## 6. Multi-Level Versioning and Compatibility Rules

PFS áp dụng quy chuẩn Semantic Versioning (SemVer 2.0.0) phân tầng độc lập cho từng thành phần:

1. **Artifact Versioning:** `MAJOR.MINOR.PATCH` (vd: `1.0.0`).
   - `PATCH`: Sửa lỗi chính tả, làm rõ câu từ, cập nhật định dạng không làm thay đổi ngữ nghĩa.
   - `MINOR`: Bổ sung thêm phần mục, mở rộng nội dung nhưng tương thích với các tài liệu phụ thuộc.
   - `MAJOR`: Thay đổi cơ cấu nội dung, xóa bỏ phần mục, làm thay đổi hợp đồng giao tiếp hoặc quyết định nền tảng.
2. **Foundation Package Snapshot:** Mỗi lần hoàn tất một giai đoạn hoặc nghiệm thu một Milestone, PFS tạo một **Immutable Snapshot** được niêm phong bằng chữ ký số của người phê duyệt.
3. **Migration & Deprecation Strategy:** Khi một Artifact chuyển sang trạng thái `Superseded`, hệ thống duy trì đường dẫn tương thích cũ (Legacy Alias) trong tối thiểu 1 chu kỳ phiên bản chính tiếp theo và hiển thị cảnh báo chuyển tiếp (Deprecation Warning).
