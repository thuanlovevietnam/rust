# PFS-M1-DOC-007 — Universal Domain Model & Domain Test Profiles

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-007 |
| Document Title | Universal Domain Model and Multi-Domain Test Profiles Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Reference Architecture | Domain-Driven Design (DDD), Entity-Relationship Metamodel |
| Related Diagrams | DIA-006-universal-domain-model.mmd |
| Related Decisions | ADR-004, ADR-005, ADR-006 |

---

## 1. Domain Modeling Philosophy & Universal Scope

Trọng tâm cốt lõi của **Project Foundation System (PFS)** là mô hình miền trừu tượng (Domain Abstraction). PFS bác bỏ định kiến rằng "mọi dự án công nghệ thông tin đều bắt đầu bằng mã nguồn phần mềm". Thay vào đó, PFS định nghĩa một **Universal Domain Metamodel** áp dụng thống nhất cho mọi loại hình dự án của con người và tổ chức: từ phát triển phần mềm, mở rộng kinh doanh, nghiên cứu khoa học hàn lâm, cho đến tái cấu trúc quy trình vận hành.

Mô hình miền của PFS được phân rã thành các khái niệm bản thể học (Ontological Concepts) không phụ thuộc vào công nghệ triển khai:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Universal Metamodel Graph                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Organization ──< Workspace ──< Project                                    │
│                                   ├── has ──> Project Intent                │
│                                   ├── has ──> Project Profile               │
│                                   ├── has ──> Capability Profile            │
│                                   ├── has ──> Requirement / Decision DAG    │
│                                   ├── runs ─> Foundation Workflow           │
│                                   │             └── executes ─> Agent Tasks │
│                                   ├── owns ─> Artifacts & Provenance Merkle │
│                                   └── guards─> Quality Gates & Evidence     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Domain Entities & Structural Definitions

Hệ thống quản lý 40 khái niệm thực thể nghiệp vụ cốt lõi, được phân loại thành các Aggregates theo chuẩn DDD (Domain-Driven Design):

### 2.1. Phân nhóm Thực thể Định danh & Không gian (Tenant & Workspace)
1. **Organization:** Đại diện cho tổ chức hoặc doanh nghiệp cấp cao nhất (Root Tenant).
2. **Workspace:** Không gian làm việc nhóm trực thuộc Organization, nhóm các dự án có chung nguồn lực hoặc chính sách bảo mật.
3. **Project:** Đơn vị công việc trung tâm của PFS, sở hữu toàn bộ vòng đời, tài nguyên và artifacts của một dự án cụ thể.

### 2.2. Phân nhóm Ý niệm & Cấu hình (Intent & Profiles)
4. **Project Intent:** Ý tưởng khởi nguyên hoặc yêu cầu thô được người dùng đưa vào hệ thống.
5. **Project Profile:** Hồ sơ phân loại dự án (Domain type, mức độ phức tạp, rủi ro, thời hạn, ngân sách token, phân loại bảo mật).
6. **Project Context:** Tập hợp các tham số môi trường, ràng buộc kỹ thuật và dữ liệu bối cảnh đầu vào.
7. **Capability:** Đặc tả trừu tượng về một năng lực mà dự án có thể sở hữu (Xem `06-CAPABILITY-ARCHITECTURE.md`).
8. **Capability Profile:** Bộ cấu hình năng lực đã giải quyết riêng cho một dự án cụ thể.

### 2.3. Phân nhóm Quy chuẩn & Ra quyết định (Requirements & Decisions)
9. **Requirement:** Đặc tả yêu cầu chức năng hoặc phi chức năng của dự án.
10. **Constraint:** Ràng buộc bất di bất dịch (ngân sách, thời gian, công nghệ bắt buộc, luật định).
11. **Assumption:** Giả định được đưa ra khi thiếu thông tin; bắt buộc phải có chủ sở hữu và điều kiện kiểm chứng.
12. **Risk:** Rủi ro đã nhận diện, kèm xác suất, mức độ tác động và phương án giảm thiểu.
13. **Decision (ADR):** Quyết định chiến lược được ghi nhận kèm lý do, các lựa chọn thay thế và hệ quả.
14. **Policy:** Quy tắc quản trị hệ thống có tính bắt buộc (ví dụ: Deny-by-default, L0–L5).

### 2.4. Phân nhóm Vận hành & Tự động hóa (Workflow & Multi-Agent)
15. **Foundation:** Thực thể đóng gói kết quả toàn vẹn của một dự án nền tảng.
16. **Foundation Stage:** Một trong 11 giai đoạn của vòng đời Foundation Lifecycle.
17. **Workflow:** Quy trình điều phối luồng công việc của dự án.
18. **Workflow Execution:** Thể hiện thực thi cụ thể của một workflow tại thời điểm thực tế.
19. **Task:** Đơn vị công việc cụ thể được phân bổ cho Agent hoặc con người.
20. **Agent:** Thực thể nhân tạo có hồ sơ năng lực thực hiện nhiệm vụ.
21. **Agent Profile:** Định nghĩa vai trò, công cụ được phép, giới hạn ngữ cảnh của một Agent.
22. **Role, Authority, Permission:** Mô hình phân quyền L0–L5 xác định thẩm quyền của từng chủ thể.

### 2.5. Phân nhóm Tạo tác & Tri thức (Artifacts & Knowledge)
23. **Artifact:** Đơn vị tạo tác có cấu trúc (tài liệu, mã nguồn, schema, config).
24. **Artifact Version:** Phiên bản bất biến của một artifact, được định danh theo mã băm nội dung.
25. **Template:** Mẫu tạo tác chuẩn hóa dùng để sinh tài liệu/mã nguồn.
26. **Template Version:** Phiên bản cụ thể của một template.
27. **Knowledge Item:** Tri thức nghiệp vụ có thể tái sử dụng xuyên dự án.

### 2.6. Phân nhóm Đảm bảo Chất lượng & Kiểm toán (Quality & Audit)
28. **Quality Gate:** Cổng kiểm định chất lượng bắt buộc trước khi chuyển giai đoạn.
29. **Evidence:** Bằng chứng kiểm chứng độc lập (kết quả test, log, chữ ký số).
30. **Finding:** Phát hiện vi phạm hoặc điểm lưu ý trong quá trình kiểm toán.
31. **Exception / Waiver:** Ngoại lệ được cấp phép có thời hạn bởi thẩm quyền hợp lệ.
32. **Approval:** Quyết định phê duyệt chính thức được ký bởi thẩm quyền được ủy quyền.
33. **Execution Record & Audit Record:** Nhật ký thực thi và kiểm toán bất biến (Append-only).

---

## 3. Universal Domain Identity Model (ULID / UUIDv7)

PFS sử dụng mô hình định danh toàn cầu bất biến dựa trên chuẩn **ULID (Universally Unique Lexicographically Sortable Identifier)** hoặc **UUIDv7**:
- **Tính sắp xếp theo thời gian (Time-sortable):** Cho phép lập chỉ mục hiệu năng cao trong cơ sở dữ liệu.
- **Tính duy nhất tuyệt đối:** Phân biệt rạch ròi giữa **Hệ thống Identity (ULID)**, **Đường dẫn tệp tin (File Path)** và **Tên hiển thị (Display Name)**.
- **Cấu trúc URN chuẩn hóa:**
  `pfs:<entity_type>:<workspace_id>:<project_id>:<ulid>`
  *Ví dụ:* `pfs:artifact:ws_corp:prj_alpha:01HQZ9G8K5E7B9A3F1M4R2V0W8`

---

## 4. Multi-Domain Validation: Four Universal Test Profiles

Để chứng minh tính Universal thực tế của PFS và bảo đảm mô hình không bị "thiên vị mã nguồn", dưới đây là 4 Hồ sơ Kiểm chứng Điển hình (Domain Test Profiles) cùng hoạt động trên cùng một PFS Metamodel:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      4 Universal Domain Test Profiles                       │
├─────────────────────┬─────────────────────┬─────────────────────────────────┤
│ Profile 1: Software │ Profile 2: Business │ Profile 3: Research             │
│ Cloud Distributed DB│ Market Expansion    │ Genomic Cancer Sequencing       │
│ - Tech Stack: Rust  │ - Canvas: Value Prop│ - Hypothesis: Mutation Marker   │
│ - C4 Architecture   │ - Financial Forecast│ - Literature Provenance         │
│ - CI/CD & Sandboxes │ - Legal Compliance  │ - Double-Blind Peer Review Gate │
├─────────────────────┴─────────────────────┴─────────────────────────────────┤
│ Profile 4: Custom User-Defined Domain                                       │
│ Smart City Environmental Sensor Network & Governance                        │
│ - Custom Schema: Sensor Topology, IoT Frequency, Urban Zoning Compliance   │
│ - Dynamic Capabilities: LoRaWAN Specs, Air Quality Thresholds               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1. Profile 1 — Software Product: "Distributed High-Throughput Storage Engine"
- **Project Type:** `SoftwareProduct`
- **Project Intent:** Xây dựng công cụ lưu trữ phân tán hiệu năng cao, độ trễ thấp bằng ngôn ngữ Rust, hỗ trợ giao thức S3-compatible.
- **Active Capabilities:**
  - `cap.core.arch.c4_model` (Required)
  - `cap.domain.software.rust_core` (Required)
  - `cap.domain.software.api_spec` (Required - OpenAPI & Protobuf)
  - `cap.core.sec.stride_threat` (Required)
- **Not Applicable Capabilities (kèm rationale):**
  - `cap.domain.business.canvas`: *Không áp dụng vì đây là thư viện hạ tầng kỹ thuật nội bộ, không có mô hình kinh doanh bán lẻ thương mại.*
  - `cap.domain.research.dataset_provenance`: *Không áp dụng vì không xử lý tập dữ liệu nghiên cứu y sinh học.*
- **Output Artifacts:** Crate definitions, Cargo workspace, trait contracts, API schemas, benchmark harness, CI/CD pipeline.

### 4.2. Profile 2 — Business Project: "Southeast Asia Fintech Expansion Strategy"
- **Project Type:** `BusinessStrategy`
- **Project Intent:** Xây dựng kế hoạch chiến lược mở rộng dịch vụ thanh toán kỹ thuật số sang 3 quốc gia Đông Nam Á trong 24 tháng.
- **Active Capabilities:**
  - `cap.domain.business.canvas` (Required)
  - `cap.domain.business.financial_model` (Required)
  - `cap.domain.business.regulatory_compliance` (Required - Ngân hàng trung ương sở tại)
  - `cap.core.gov.authority` (Required)
- **Not Applicable Capabilities (kèm rationale):**
  - `cap.domain.software.rust_core`: *Không áp dụng vì dự án thuộc lĩnh vực chiến lược kinh doanh và pháp lý, không trực tiếp sản xuất mã nguồn phần mềm.*
  - `cap.core.arch.c4_model`: *Không áp dụng vì không có hệ thống phần mềm cần mô hình hóa; thay thế bằng sơ đồ cấu trúc tổ chức và luồng vốn.*
- **Output Artifacts:** Business Model Canvas, Market TAM/SAM Analysis, Financial Cash Flow Forecasts, Legal Opinion Registry, Executive Presentation Deck.

### 4.3. Profile 3 — Research Project: "AI-Assisted CRISPR Targeted Gene Mutation Analysis"
- **Project Type:** `AcademicResearch`
- **Project Intent:** Nghiên cứu và mô hình hóa tác động đột biến gen mục tiêu bằng thuật toán Transformer trên tập dữ liệu tế bào ung thư.
- **Active Capabilities:**
  - `cap.domain.research.hypothesis_tracking` (Required)
  - `cap.domain.research.dataset_provenance` (Required - Chuẩn hoá nguồn gốc dữ liệu sinh học)
  - `cap.domain.research.ethical_review` (Required - Institutional Review Board Approval)
  - `cap.domain.research.reproducibility_protocol` (Required)
- **Not Applicable Capabilities (kèm rationale):**
  - `cap.domain.software.rust_core`: *Không áp dụng vì mã thử nghiệm nghiên cứu chạy trên Python/Jupyter sandbox độc lập, không yêu cầu production software architecture.*
  - `cap.domain.business.financial_model`: *Không áp dụng vì dự án được tài trợ toàn phần bằng quỹ khoa học phi lợi nhuận.*
- **Output Artifacts:** Formal Research Protocol, Literature Survey Matrix, Dataset Hash Manifest, Ethical Committee Waivers, Replication Checklist.

### 4.4. Profile 4 — Custom User-Defined Domain: "Smart City Environmental IoT Network"
- **Project Type:** `CustomDomain` (User-defined via JSON Schema Extension)
- **Project Intent:** Thiết lập hệ thống cảm biến môi trường quan trắc chất lượng không khí đô thị, tích hợp quy định quy hoạch đô thị.
- **Active Capabilities:**
  - `cap.ext.smartcity.sensor_topology` (Extension-Provided)
  - `cap.ext.smartcity.urban_zoning_rules` (Extension-Provided)
  - `cap.core.sec.stride_threat` (Required - An toàn hạ tầng trọng yếu)
- **Output Artifacts:** Sensor Hardware Placement Grid, Urban Zoning Compliance Cert, Environmental Metric Schemas.

---

## 5. Domain Relationship Model & Constraints

Mỗi quan hệ giữa các thực thể trong mô hình miền PFS đều được định nghĩa rõ ràng về Ngữ nghĩa (Semantics), Bản số (Cardinality) và Ràng buộc toàn vẹn (Integrity Rules):

| Quan hệ nghiệp vụ | Bản số | Ràng buộc toàn vẹn & Quy tắc vòng đời |
|---|---|---|
| `Project` **has** `Intent` | 1 : 1..* | Project bắt buộc phải có ít nhất 1 Intent khởi nguyên; Intent mới làm phát sinh phiên bản dự án mới. |
| `Project` **resolves** `CapabilityProfile` | 1 : 1 | Mỗi dự án có duy nhất 1 Capability Profile hiện hành; mọi thay đổi phải qua approval. |
| `Requirement` **derives-from** `Requirement` | * : * | Tạo thành đồ thị Directed Acyclic Graph (DAG); cấm tuyệt đối quan hệ chu trình (Cyclic Dependency). |
| `Requirement` **conflicts-with** `Requirement` | * : * | Khi có xung đột, hệ thống chặn Quality Gate cho đến khi có Decision hòa giải từ thẩm quyền hợp lệ. |
| `Decision` **governs** `Requirement` | 1..* : 1..* | Một quyết định có thể chi phối nhiều yêu cầu; yêu cầu quan trọng bắt buộc phải có quyết định bảo trợ. |
| `Decision` **supersedes** `Decision` | 0..1 : 0..1 | Quyết định mới thay thế quyết định cũ; toàn bộ yêu cầu phụ thuộc phải được đánh giá lại tác động. |
| `Artifact` **derived-from** `Artifact` | * : * | Tạo thành Merkle DAG; mã băm của artifact con phụ thuộc vào mã băm của artifact cha. |
| `Evidence` **supports** `Requirement/Decision` | 1..* : 1 | Bằng chứng kiểm chứng khách quan là điều kiện tiên quyết để nghiệm thu tiêu chí chất lượng. |
| `Finding` **blocks** `QualityGate` | 1..* : 1 | Phát hiện loại Critical/High sẽ lập tức khóa cổng chuyển giai đoạn của Workflow. |

---

## 6. Comprehensive Data Lifecycle

Mọi thực thể dữ liệu trong PFS đều tuân thủ vòng đời trạng thái 11 bước tiêu chuẩn:
1. **Creation:** Khởi tạo thực thể với định danh duy nhất ULID và metadata ban đầu.
2. **Draft:** Giai đoạn soạn thảo, dữ liệu có thể sửa đổi tự do bởi chủ thể có quyền L2.
3. **In Review:** Thực thể được gửi đi xem xét, trạng thái khóa sửa đổi tạm thời.
4. **Approval:** Được ký xác nhận bởi thẩm quyền con người L3–L5 tương ứng.
5. **Active / In Effect:** Thực thể chính thức có hiệu lực chi phối các thành phần khác.
6. **Superseded:** Thực thể bị thay thế bởi một phiên bản mới hơn; vẫn lưu giữ lịch sử.
7. **Archived:** Chuyển vào trạng thái lưu trữ lâu dài khi dự án hoàn thành.
8. **Retention Hold:** Đóng băng trạng thái do yêu cầu thanh tra pháp lý hoặc kiểm toán.
9. **Export:** Đóng gói xuất khẩu dữ liệu sang định dạng tiêu chuẩn (ZIP, Tarball, JSON).
10. **Soft Deletion:** Đánh dấu xóa logic (`deleted_at`), ẩn khỏi giao diện nhưng bảo tồn toàn vẹn dữ liệu cho kiểm toán.
11. **Physical Deletion:** Xóa vật lý khỏi cơ sở dữ liệu chỉ khi có lệnh trực tiếp từ Project Owner (L5) và không có Retention Hold.
