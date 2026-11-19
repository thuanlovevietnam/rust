# PFS-M1-DOC-006 — Capability Architecture & Dynamic Registry

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-006 |
| Document Title | Capability Architecture and Dynamic Registry Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Related Decisions | ADR-006, ADR-011 |
| Parent Baseline | [PFS-M0-SPEC-003](file:///C:/Users/OK259/rust/docs/M0-foundation/03-UNIVERSAL-PROJECT-MODEL.md) §5 |

---

## 1. Capability Concept & Product Rationale

Trong **Project Foundation System (PFS)**, **Capability** (Năng lực) là đơn vị đóng gói mô-đun hóa độc lập đại diện cho một khả năng kỹ thuật, quản trị hoặc nghiệp vụ mà một dự án có thể sở hữu hoặc yêu cầu.

Khác với các hệ thống cứng nhắc chỉ sinh ra một bộ tài liệu cố định, PFS sử dụng **Capability-Driven Architecture**. Một dự án (Project) được cấu hình thông qua một **Capability Profile**, xác định tập hợp các năng lực được kích hoạt, các năng lực không áp dụng (Not Applicable) và các điều kiện kích hoạt động. Nhờ đó, PFS có thể sinh ra một Project Foundation tối ưu cho một dự án Phần mềm vi dịch vụ, một dự án Nghiên cứu khoa học sinh học, hoặc một Chiến dịch mở rộng thị trường mà không làm ô nhiễm cấu trúc bằng những artifact không liên quan.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Capability Structural Model                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Metadata: Stable ID, Name, Category, Semantic Version, Provider (Core/Ext) │
│  Applicability: Required | Optional | Conditional | Not Applicable          │
│  Dependencies: Requires [Cap_A, Cap_B] | ConflictsWith [Cap_X]             │
│  Contracts: Inputs Schema | Outputs Schema | Required Artifacts Manifest   │
│  Assurance: Validation Rules | Quality Gate Criteria | Evidence Reqs        │
│  Extensibility: Hook Points | Template Mappings | Tool Allowlist            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Formal Capability Specification Schema

Mỗi Capability được đăng ký trong hệ thống bắt buộc phải thỏa mãn cấu trúc đặc tả chuẩn hóa (được định nghĩa bằng JSON Schema tại `docs/M1-architecture/schemas/capability-schema.json`):

| Thuộc tính | Kiểu dữ liệu | Bắt buộc | Mô tả ngữ nghĩa |
|---|---|---|---|
| `capability_id` | String (ULID/URN) | Có | Định danh ổn định duy nhất, ví dụ: `cap.core.architecture.modular` |
| `name` | String | Có | Tên hiển thị người dùng đọc được |
| `description` | String | Có | Mô tả chi tiết mục đích và phạm vi giải quyết của năng lực |
| `category` | Enum | Có | Phân nhóm: `Governance`, `Domain`, `Architecture`, `Quality`, `Security`, `Operations`, `Extension` |
| `version` | SemVer String | Có | Phiên bản năng lực tuân thủ SemVer 2.0.0 (vd: `1.2.0`) |
| `provider_type` | Enum | Có | `CoreProvided` (nằm trong PFS Core) hoặc `ExtensionProvided` (plugin bên ngoài) |
| `dependencies` | Array<String> | Không | Danh sách các `capability_id` bắt buộc phải được kích hoạt trước |
| `conflicts_with`| Array<String> | Không | Danh sách các `capability_id` loại trừ lẫn nhau (không thể cùng kích hoạt) |
| `input_schemas` | Map<String, Ref> | Có | Lược đồ JSON Schema xác thực dữ liệu đầu vào cần thiết để khởi tạo |
| `required_artifacts`| Array<ArtifactSpec> | Có | Danh mục các loại tài liệu/mã nguồn mà năng lực này bắt buộc phải sinh ra |
| `validation_rules` | Array<RuleSpec> | Có | Bộ quy tắc logic xác định để kiểm tra tính hoàn thiện của năng lực |
| `quality_criteria` | Array<QualitySpec>| Có | Tiêu chuẩn chất lượng và bằng chứng tối thiểu cần nộp cho Quality Gates |
| `lifecycle_state` | Enum | Có | `Draft`, `Active`, `Deprecated`, `Retired` |

---

## 3. Applicability States & Decision Rules

Khi thiết lập một dự án cụ thể, mỗi Capability trong danh mục tổng thể sẽ được giải quyết (resolved) thành một trong các trạng thái áp dụng sau:

1. **Required (Bắt buộc):**
   - Năng lực cốt lõi không thể thiếu đối với loại hình dự án này.
   - Nếu thiếu hoặc thất bại, toàn bộ Foundation Workflow sẽ bị chặn tại Quality Gate tương ứng.
2. **Optional (Tùy chọn):**
   - Năng lực mang tính gia tăng giá trị, người dùng có thể chủ động bật hoặc tắt tùy thuộc vào nguồn lực và mục tiêu dự án.
3. **Conditional (Có điều kiện):**
   - Năng lực tự động được kích hoạt nếu thỏa mãn một biểu thức điều kiện dựa trên Project Profile (ví dụ: nếu `data_classification == 'Restricted'`, tự động kích hoạt `cap.core.security.airgap`).
4. **Not Applicable (Không áp dụng) — Kèm Rationale bắt buộc:**
   - Năng lực được chủ động loại trừ khỏi phạm vi dự án.
   - **BẤT BIẾN NGHIÊM NGẶT:** Việc đánh dấu *Not Applicable* bắt buộc phải đi kèm với một **Lý do giải trình (Rationale)** được ghi nhận vào quyết định kiến trúc và lưu vết trong Project Profile. Không được phép âm thầm bỏ qua một năng lực tiêu chuẩn.
5. **Extension-Provided (Do tiện ích mở rộng cung cấp):**
   - Năng lực được nạp động từ các bên thứ ba qua Plugin/Extension Interface của PFS.

---

## 4. Canonical Core Capability Catalog

PFS Core cung cấp sẵn một Danh mục Năng lực chuẩn hóa mở rộng (Open Catalog):

```
                                  CAPABILITY CATALOG
    ┌──────────────────────────────┬──────────────────────────────┐
    │     Governance & Quality     │    Architecture & Security   │
    ├──────────────────────────────┼──────────────────────────────┤
    │ cap.core.gov.authority       │ cap.core.arch.universal      │
    │ cap.core.gov.decisions       │ cap.core.arch.c4_model       │
    │ cap.core.qlt.evidence_gates  │ cap.core.sec.stride_threat   │
    │ cap.core.qlt.traceability    │ cap.core.sec.secret_redact   │
    ├──────────────────────────────┼──────────────────────────────┤
    │     Domain Specifics         │    Operations & Delivery     │
    ├──────────────────────────────┼──────────────────────────────┤
    │ cap.domain.software.rust_core│ cap.core.ops.container_deploy│
    │ cap.domain.software.api_spec │ cap.core.ops.telemetry_otlp  │
    │ cap.domain.business.canvas   │ cap.core.gen.idempotent_safe │
    │ cap.domain.research.dataset  │ cap.ext.custom.user_defined  │
    └──────────────────────────────┴──────────────────────────────┘
```

### 4.1. Chi tiết một số Core Capabilities tiêu biểu
- **`cap.core.gov.authority` (Authority & Decision Control):** Cung cấp mô hình phân quyền L0–L5, quản lý danh sách phê duyệt và chữ ký số. Bắt buộc cho 100% các loại dự án.
- **`cap.core.qlt.traceability` (Bidirectional Requirement Traceability):** Duy trì ma trận truy vết hai chiều từ Intent đến Artifact. Bắt buộc cho 100% các loại dự án.
- **`cap.domain.software.rust_core` (Rust Modular Engine):** Chỉ áp dụng cho dự án Software Product yêu cầu hiệu năng cao và an toàn bộ nhớ. Đánh dấu *Not Applicable* cho Business và Research Projects kèm rationale.
- **`cap.domain.business.canvas` (Business Model Architecture):** Cung cấp các cấu trúc phân tích thị trường, mô hình doanh thu, cơ cấu chi phí. Áp dụng cho Business Projects; đánh dấu *Not Applicable* cho Software Libraries thuần túy.

---

## 5. Capability Resolution Algorithm & Conflict Detection

Trước khi khởi động Foundation Workflow, PFS Core thực thi thuật toán giải quyết đồ thị phụ thuộc (Topological Sort & Dependency Resolution) để xác định tính hợp lệ của Capability Profile:

```rust
// Mã giả thuật toán giải quyết năng lực trong PFS Core (Rust)
pub fn resolve_capabilities(
    catalog: &CapabilityCatalog,
    profile: &ProjectProfile,
) -> Result<ResolvedCapabilitySet, CapabilityResolutionError> {
    let mut resolved = HashSet::new();
    let mut conflict_graph = ConflictGraph::new();

    // 1. Nạp tất cả Required capabilities cho domain
    for cap_id in profile.required_capabilities() {
        resolved.insert(catalog.get(cap_id)?);
    }

    // 2. Đánh giá các Conditional capabilities dựa trên Context
    for cap in catalog.conditional_capabilities() {
        if cap.eval_condition(&profile.context)? {
            resolved.insert(cap);
        }
    }

    // 3. Giải quyết đồ thị phụ thuộc đệ quy (Dependencies Resolution)
    for cap in &resolved {
        for dep_id in &cap.dependencies {
            if !resolved.contains(dep_id) {
                return Err(CapabilityResolutionError::MissingDependency(cap.id, dep_id));
            }
        }
    }

    // 4. Phát hiện xung đột (Conflict Detection)
    for cap in &resolved {
        for conflict_id in &cap.conflicts_with {
            if resolved.contains(conflict_id) {
                return Err(CapabilityResolutionError::MutuallyExclusiveConflict(cap.id, conflict_id));
            }
        }
    }

    // 5. Kiểm tra tính hợp lệ của các mục Not Applicable
    for na_item in profile.not_applicable_items() {
        if na_item.rationale.trim().is_empty() {
            return Err(CapabilityResolutionError::MissingNARationale(na_item.cap_id));
        }
    }

    Ok(ResolvedCapabilitySet::new(resolved))
}
```
