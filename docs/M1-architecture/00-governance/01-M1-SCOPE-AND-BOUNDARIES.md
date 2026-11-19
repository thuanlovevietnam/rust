# PFS-M1-DOC-001 — Scope, System Boundaries and Invariants

| Thuộc tính | Giá trị |
|---|---|
| Document ID | PFS-M1-DOC-001 |
| Document Title | Scope, System Boundaries and Invariants Specification |
| Project | Project Foundation System (PFS) |
| Milestone | M1 — Documentation & Architecture Foundation |
| Version | 1.0.0 |
| Status | Proposed — Ready for Owner Review |
| Authority | Principal Systems Architect |
| Classification | Internal |
| Parent Baseline | [PFS-M0-SPEC-002](file:///C:/Users/OK259/rust/docs/M0-foundation/02-PRODUCT-DEFINITION.md), [PFS-M0-SPEC-003](file:///C:/Users/OK259/rust/docs/M0-foundation/03-UNIVERSAL-PROJECT-MODEL.md) |

---

## 1. Product Identity and Core Mission

**Project Foundation System (PFS)** là một Universal Project Foundation Engine — hệ thống chuyên dụng tiếp nhận ý tưởng (Project Intent), phân tích mục tiêu, mô hình hóa miền nghiệp vụ, xác lập kiến trúc, thiết lập cơ chế quản trị và điều phối việc sinh ra **Project Foundation Package** hoàn chỉnh, có cấu trúc, có thể kiểm chứng và sẵn sàng cho việc triển khai dự án trong thực tế.

PFS giải quyết vấn đề cốt tử của các dự án hiện đại: khoảng trống giữa ý tưởng ban đầu và nền tảng kỹ thuật/quản trị có cấu trúc. Hầu hết các dự án thất bại hoặc phát sinh nợ kỹ thuật nghiêm trọng ngay từ giai đoạn khởi đầu do thiếu nền tảng chuẩn mực, thiếu sự tường minh về quyền hạn và không có khả năng truy vết yêu cầu.

### 1.1. Bất biến định vị sản phẩm (Product Non-Goals)

Để bảo đảm tính tập trung và chuẩn xác của kiến trúc, PFS xác định rõ các ranh giới phủ định:
- **KHÔNG PHẢI một trình quản lý tài liệu tĩnh:** PFS không đơn thuần lưu trữ Markdown hay wiki; mọi artifact trong PFS đều là thực thể có định danh, lược đồ (schema), nguồn gốc (provenance) và liên kết nghiệp vụ.
- **KHÔNG PHẢI một công cụ sinh Markdown hoặc AGENTS.md rời rạc:** Việc sinh tài liệu chỉ là một phần biểu diễn của Project Foundation Model.
- **KHÔNG PHẢI một công cụ chỉ dành riêng cho Software:** PFS là universal engine hỗ trợ cả dự án kinh doanh, nghiên cứu, vận hành và tổ chức. Software chỉ là một Profile ứng dụng.
- **KHÔNG PHẢI một chatbot tư vấn dự án tự do:** PFS vận hành theo quy trình kiểm soát trạng thái (State Machine), hợp đồng giao tiếp (Contracts) và kiểm định bằng chứng (Evidence-based Quality Gates).
- **KHÔNG PHẢI hệ thống phụ thuộc vào một nhà cung cấp AI:** PFS độc lập tuyệt đối với OpenAI, Anthropic, Google hay local models.
- **KHÔNG PHẢI hệ thống AI tự quyết (Uncontrolled Autonomy):** AI chỉ đóng vai trò phân tích, suy luận và dự thảo (L0–L2); mọi quyết định kiến trúc, thay đổi và phê duyệt bắt buộc phải qua cơ chế xác định (Deterministic Enforcement) và thẩm quyền con người (L3–L5).

---

## 2. Universal Scope and Multi-Domain Boundaries

PFS được thiết kế với kiến trúc trừu tượng hóa miền (Domain Abstraction), cho phép xử lý đa dạng các loại hình dự án mà không áp đặt định kiến kỹ thuật phần mềm lên các lĩnh vực phi phần mềm.

### 2.1. Phân định ranh giới theo Domain Types

```
                    ┌──────────────────────────────────────────────┐
                    │          PFS Universal Core Engine           │
                    │  (Intent, Profile, Capability, Governance,   │
                    │   Workflow, Quality, Artifacts, Traceability) │
                    └──────────────────────┬───────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
┌─────────────────┐┌─────────────────┐┌─────────────────────┐┌─────────────────┐
│ Software Domain ││ Business Domain ││   Research Domain   ││  Custom Domain  │
│ - Tech Stack    ││ - Business Model││ - Hypothesis/Method ││ - User-defined  │
│ - Architecture  ││ - Market/Finance││ - Literature/Data   ││   Capabilities  │
│ - Source Repo   ││ - Ops Strategy  ││ - Peer Review/Ethics││ - Schema Ext.   │
│ - CI/CD Pipeline││ - Compliance    ││ - Replication Study ││ - Custom Gates  │
└─────────────────┘└─────────────────┘└─────────────────────┘└─────────────────┘
```

1. **Software Product Projects:** Dự án phát triển hệ thống phần mềm, dịch vụ số, thư viện mã nguồn, nền tảng phân tán. Có các thuộc tính đặc thù: runtime stack, API, database, repository, security sandbox, deployment topology.
2. **Business Projects:** Dự án chiến lược kinh doanh, tung sản phẩm mới, M&A, chuyển đổi số doanh nghiệp. Trọng tâm: Value Proposition, Business Model Canvas, Market Analysis, Financial Projections, Legal Compliance, Stakeholder Governance. Tuyệt đối không sinh mã nguồn hay schema cơ sở dữ liệu nếu không có yêu cầu.
3. **Research Projects:** Dự án nghiên cứu khoa học, thử nghiệm học thuật, R&D. Trọng tâm: Research Hypothesis, Literature Survey, Methodology, Dataset Provenance, Ethical Approval, Reproducibility Criteria, Peer Review Gates.
4. **Operations & Organization Projects:** Dự án tái cấu trúc quy trình, thiết lập hệ thống vận hành, quản trị chất lượng ISO, diễn tập an toàn thông tin. Trọng tâm: Standard Operating Procedures (SOPs), RACI Matrix, Service Level Agreements (SLAs), Key Performance Indicators (KPIs).
5. **Custom User-Defined Domains:** Hệ sinh thái mở cho phép người dùng định nghĩa Domain Profile mới thông qua Dynamic Capability Registry và JSON Schema mở rộng mà không cần biên dịch lại PFS Core.

---

## 3. System Context Boundaries

### 3.1. Ranh giới hệ thống (Inside vs. Outside Boundary)

| Phân vùng | Thành phần Bên trong PFS (In-Scope) | Thành phần Bên ngoài PFS (Out-of-Scope) |
|---|---|---|
| **Lõi xử lý** | - Intent Ingestion & Parsing Engine<br>- Universal Domain Graph & Entity Lifecycle<br>- 11-Stage Foundation Workflow Engine<br>- Multi-Agent Task Planner & Orchestrator<br>- Deterministic L0–L5 Policy Enforcement<br>- Staged Idempotent Foundation Generator<br>- Quality Gates & Evidence Validation Engine | - Mã nguồn nghiệp vụ của ứng dụng đích sau khi sinh<br>- Trình biên dịch mã nguồn của dự án đích (vd: cargo, npm, gradle)<br>- Hạ tầng đám mây của dự án đích (AWS, GCP, Azure)<br>- Production Operations sau giai đoạn Foundation |
| **Giao diện & Tích hợp** | - CLI Tool (`pfs-cli`) cho developer & CI/CD<br>- Local Daemon & REST/WebSocket API (`pfsd`)<br>- Headless Agent Tool Interface (JSON-RPC)<br>- Web/Desktop Workspace UI Client | - Các AI IDEs bên ngoài (Cursor, Windsurf, VS Code)<br>- Các Git Hosting Providers (GitHub, GitLab, Bitbucket)<br>- Trình duyệt web bên ngoài |
| **Dịch vụ Ngoài** | - AI Provider Adapters & Gateway<br>- Tool Gateway & Execution Sandbox Boundary<br>- Storage Adapters (Filesystem, SQLite, Postgres)<br>- Telemetry & Audit Emitters | - Máy chủ LLM thực tế (OpenAI API, Anthropic API, vLLM)<br>- Hệ điều hành máy chủ và kernel sandbox (Docker daemon, WASM runtime host)<br>- Các dịch vụ nhận diện bên ngoài (OIDC, SAML, LDAP) |

### 3.2. Ranh giới tin cậy và kiểm soát an ninh (Trust Boundaries)

PFS xác lập 4 ranh giới tin cậy nghiêm ngặt:
1. **TB-1: User/Client Boundary:** Ranh giới giữa người dùng tương tác (CLI/UI) và PFS Application Service. Mọi dữ liệu đầu vào đều là untrusted, bắt buộc qua lược đồ xác thực (Schema Validation) và làm sạch (Sanitization).
2. **TB-2: Core Engine Boundary:** Ranh giới giữa Application Services và Domain Model. Chỉ có các Command/Query đã được xác thực danh tính và thẩm quyền (L0–L5 Authorization) mới được chạm vào Domain Entities.
3. **TB-3: External AI Boundary:** Ranh giới giữa PFS và các nhà cung cấp mô hình ngôn ngữ lớn (LLMs). Dữ liệu gửi sang LLM phải được lọc bí mật (Secret Redaction) và gắn nhãn phân loại dữ liệu. Phản hồi từ LLM được coi là untrusted proposal (L1), tuyệt đối không có quyền tự kích hoạt thao tác ghi đè hoặc thực thi hệ thống.
4. **TB-4: Tool Execution Sandbox Boundary:** Ranh giới giữa PFS Core và môi trường thực thi công cụ bên ngoài (shell command, file writer, external validator). Mọi thao tác I/O bắt buộc phải qua Sandbox cách ly với quyền tối thiểu (Least Privilege) và danh sách cho phép (Allowlist).

---

## 4. Architectural Invariants (Bất biến kiến trúc)

Toàn bộ các quyết định thiết kế và mã nguồn triển khai của PFS phải bảo toàn 12 bất biến sau:

- **INV-01 (Universal Domain Abstraction):** Core Domain không chứa bất kỳ khái niệm đặc thù nào của Software Engineering trừ khi được đóng gói trong một Capability Profile cụ thể.
- **INV-02 (Hybrid Separation):** AI Reasoning chỉ tạo ra suy luận và đề xuất; Deterministic Rust Engine kiểm soát trạng thái, phân quyền, thẩm định và thực thi I/O.
- **INV-03 (PFS Core Implementation Stack):** PFS Core Engine được hiện thực 100% bằng ngôn ngữ lập trình Rust để bảo đảm an toàn bộ nhớ, hiệu năng cao và tính tin cậy tuyệt đối.
- **INV-04 (Multi-Agent with Single Authority):** Nhiều agent có thể cộng tác và phản biện, nhưng không có khái niệm "đa số agent thắng thiểu số". Chỉ có thẩm quyền được ủy quyền hợp lệ mới có quyền ra quyết định.
- **INV-05 (Provider Independence):** Không sử dụng SDK độc quyền của bất kỳ AI Provider nào trong Domain Core. Toàn bộ giao tiếp qua abstraction traits chuẩn hóa.
- **INV-06 (Deny-by-Default Authorization):** Mọi hành động truy cập hoặc sửa đổi tài nguyên đều bị từ chối mặc định trừ khi có chính sách phân quyền L0–L5 rõ ràng.
- **INV-07 (Evidence-Based Gate):** Không một giai đoạn nào trong vòng đời dự án được đánh dấu hoàn thành nếu thiếu các bằng chứng kiểm chứng (Evidence Artifacts) tương ứng.
- **INV-08 (Safe & Idempotent Generation):** Quá trình sinh Foundation phải có tính lặp lại (idempotent), hỗ trợ xem trước (dry-run preview), phát hiện xung đột và có khả năng rollback/compensation.
- **INV-09 (Artifact Provenance & Immobility):** Mọi artifact đều có định danh toàn cầu bất biến, hash kiểm tra toàn vẹn và thông tin nguồn gốc (ai tạo, khi nào, từ prompt/dữ liệu nào).
- **INV-10 (Strict Versioning & Compatibility):** Áp dụng Semantic Versioning cho Core, Schemas, Templates, Capabilities và Foundation Packages; bảo đảm tính tương thích xuôi và ngược.
- **INV-11 (Data Classification Tiers):** Dữ liệu được phân loại thành 4 cấp độ (Public, Internal, Confidential, Restricted); dữ liệu Restricted tuyệt đối không được chuyển ra AI bên ngoài.
- **INV-12 (Auditability):** Mọi sự kiện nghiệp vụ, quyết định quản trị và thao tác sinh foundation đều được ghi nhận vào nhật ký kiểm toán bất biến (Append-only Audit Log).
